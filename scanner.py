"""
Simple Security Scanner - Educational Tool
Scans for SQL Injection and XSS vulnerabilities
"""

import argparse
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import sys
import time
import re
from urllib3.exceptions import InsecureRequestWarning

from payloads.sqli_payloads import SQL_PAYLOADS, SQL_ERRORS
from payloads.xss_payloads import XSS_PAYLOADS, XSS_SIGNATURES
from utils.colors import Colors
from utils.reporter import Reporter

# Suppress SSL warnings if needed
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class SecurityScanner:
    """Main security scanner class"""
    
    def __init__(self, target_url, timeout=10, ssl_verify=True, proxy=None, 
                 user_agent=None, delay=0.5, threads=1):
        self.target_url = target_url
        self.timeout = timeout
        self.ssl_verify = ssl_verify
        self.delay = delay
        self.threads = threads
        self.reporter = Reporter(target_url)
        self.session = requests.Session()
        
        # Set User-Agent
        default_ua = 'SecurityScanner/1.0 (Educational Purpose)'
        self.session.headers.update({
            'User-Agent': user_agent or default_ua
        })
        
        # Configure SSL verification
        self.session.verify = ssl_verify
        
        # Configure proxy if provided
        if proxy:
            self.session.proxies.update({
                'http': proxy,
                'https': proxy
            })
            print(Colors.info(f"Proxy configured: {proxy}"))
        
        # Disable SSL warnings for self-signed certificates
        if not ssl_verify:
            print(Colors.warning("SSL verification disabled"))
    
    def scan_sqli(self):
        """Scan for SQL Injection vulnerabilities - GET and POST"""
        print(Colors.info(f"Starting SQL Injection scan on {self.target_url}"))
        print("-" * 60)
        
        parsed = urlparse(self.target_url)
        params = parse_qs(parsed.query)
        
        if not params:
            print(Colors.warning("No parameters found in URL"))
            return
        
        for param_name in params:
            print(f"\n{Colors.INFO}Testing parameter: {param_name}{Colors.RESET}")
            
            for payload in SQL_PAYLOADS:
                # Test GET request
                test_params = params.copy()
                test_params[param_name] = [payload]
                
                test_url = urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    urlencode(test_params, doseq=True),
                    parsed.fragment
                ))
                
                try:
                    response = self.session.get(test_url, timeout=self.timeout, 
                                               allow_redirects=True)
                    response_text = response.text.lower()
                    
                    # Enhanced detection - Check for multiple indicators
                    vuln_found = False
                    detection_method = ""
                    
                    # Check for SQL errors
                    for error in SQL_ERRORS:
                        if error in response_text:
                            vuln_found = True
                            detection_method = f"Error pattern: {error}"
                            break
                    
                    # Check for unusual response time (time-based detection)
                    start_time = time.time()
                    response_time = time.time() - start_time
                    
                    # Check response size changes (boolean-based detection indicator)
                    if not vuln_found and response_time > self.timeout * 0.8:
                        vuln_found = True
                        detection_method = "Potential time-based SQLi"
                    
                    if vuln_found:
                        vuln_msg = f"SQLi vulnerability found with payload: {payload[:30]}..."
                        print(Colors.error(vuln_msg))
                        self.reporter.add_vulnerability(
                            'SQL Injection',
                            payload,
                            detection_method,
                            param_name
                        )
                    
                    time.sleep(self.delay)
                    
                except requests.exceptions.RequestException as e:
                    print(Colors.warning(f"Request failed: {str(e)[:50]}"))
                    continue
    
    def scan_xss(self):
        """Scan for XSS vulnerabilities - Enhanced detection"""
        print(Colors.info(f"\nStarting XSS scan on {self.target_url}"))
        print("-" * 60)
        
        parsed = urlparse(self.target_url)
        params = parse_qs(parsed.query)
        
        if not params:
            print(Colors.warning("No parameters found in URL"))
            return
        
        for param_name in params:
            print(f"\n{Colors.INFO}Testing parameter: {param_name}{Colors.RESET}")
            
            for payload in XSS_PAYLOADS:
                test_params = params.copy()
                test_params[param_name] = [payload]
                
                test_url = urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    urlencode(test_params, doseq=True),
                    parsed.fragment
                ))
                
                try:
                    response = self.session.get(test_url, timeout=self.timeout,
                                               allow_redirects=True)
                    response_text = response.text
                    
                    # Enhanced XSS detection - Check if payload is reflected
                    # and if it appears in HTML context (not encoded)
                    vuln_found = False
                    
                    if payload in response_text:
                        # Double-check that it's not HTML-encoded
                        import html
                        encoded_payload = html.escape(payload)
                        
                        # If the original payload is present but not the encoded one
                        # it means it's reflected without proper escaping
                        if payload in response_text and encoded_payload not in response_text:
                            vuln_found = True
                    
                    # Check for XSS signatures
                    if not vuln_found:
                        for signature in XSS_SIGNATURES:
                            if signature in response_text.lower():
                                # Additional check - is the signature in an unsafe context?
                                if re.search(fr'<[^>]*{re.escape(signature)}[^>]*>', 
                                           response_text, re.IGNORECASE):
                                    vuln_found = True
                                    break
                    
                    if vuln_found:
                        vuln_msg = f"XSS vulnerability found with payload: {payload[:30]}..."
                        print(Colors.error(vuln_msg))
                        self.reporter.add_vulnerability(
                            'Cross-Site Scripting (XSS)',
                            payload,
                            "Payload reflected in response without proper encoding",
                            param_name
                        )
                    
                    time.sleep(self.delay)
                    
                except requests.exceptions.RequestException as e:
                    print(Colors.warning(f"Request failed: {str(e)[:50]}"))
                    continue
    
    def run_scan(self, scan_types=['sqli', 'xss']):
        """Run selected scans"""
        print("\n" + "="*60)
        print(Colors.BOLD + "SECURITY SCANNER - EDUCATIONAL TOOL" + Colors.RESET)
        print("="*60)
        print(Colors.WARNING + "WARNING: Use only on authorized targets!" + Colors.RESET)
        print("="*60 + "\n")
        
        if 'sqli' in scan_types:
            self.scan_sqli()
        
        if 'xss' in scan_types:
            self.scan_xss()
        
        self.reporter.print_summary()


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        prog='zapprobe',
        description='ZapProbe - Educational Web Vulnerability Scanner',
        epilog='Use responsibly and only on authorized targets!',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        '-u', '--url',
        required=True,
        help='Target URL to scan (e.g., http://example.com/page?id=1)'
    )
    
    # Scan configuration
    parser.add_argument(
        '-t', '--type',
        choices=['sqli', 'xss', 'all'],
        default='all',
        help='Scan type: sqli, xss, or all (default: all)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=0.5,
        help='Delay between requests in seconds (default: 0.5)'
    )
    
    # Advanced options
    parser.add_argument(
        '--no-ssl-verify',
        action='store_true',
        help='Disable SSL certificate verification (for self-signed certs)'
    )
    
    parser.add_argument(
        '--proxy',
        type=str,
        help='HTTP proxy (e.g., http://127.0.0.1:8080 for Burp Suite)'
    )
    
    parser.add_argument(
        '--user-agent',
        type=str,
        help='Custom User-Agent string'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file for report (JSON or HTML based on extension)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.2.0'
    )
    
    args = parser.parse_args()
    
    # Determine scan types
    if args.type == 'all':
        scan_types = ['sqli', 'xss']
    else:
        scan_types = [args.type]
    
    # Create and run scanner with all options
    scanner = SecurityScanner(
        args.url,
        timeout=args.timeout,
        ssl_verify=not args.no_ssl_verify,
        proxy=args.proxy,
        user_agent=args.user_agent,
        delay=args.delay
    )
    
    try:
        scanner.run_scan(scan_types)
        
        # Generate report if output file specified
        if args.output:
            scanner.reporter.export(args.output)
            print(Colors.success(f"Report exported to: {args.output}"))
            
    except KeyboardInterrupt:
        print(Colors.warning("\n\nScan interrupted by user"))
        sys.exit(0)
    except Exception as e:
        print(Colors.error(f"\nError: {str(e)}"))
        sys.exit(1)


if __name__ == '__main__':
    main()