"""
Simple Security Scanner - Educational Tool
Scans for SQL Injection and XSS vulnerabilities
"""

import argparse
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import sys
import time

from payloads.sqli_payloads import SQL_PAYLOADS, SQL_ERRORS
from payloads.xss_payloads import XSS_PAYLOADS, XSS_SIGNATURES
from utils.colors import Colors
from utils.reporter import Reporter


class SecurityScanner:
    """Main security scanner class"""
    
    def __init__(self, target_url, timeout=10):
        self.target_url = target_url
        self.timeout = timeout
        self.reporter = Reporter(target_url)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SecurityScanner/1.0 (Educational Purpose)'
        })
    
    def scan_sqli(self):
        """Scan for SQL Injection vulnerabilities"""
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
                    response = self.session.get(test_url, timeout=self.timeout)
                    response_text = response.text.lower()
                    
                    # Check for SQL errors
                    for error in SQL_ERRORS:
                        if error in response_text:
                            vuln_msg = f"SQLi vulnerability found with payload: {payload[:30]}..."
                            print(Colors.error(vuln_msg))
                            self.reporter.add_vulnerability(
                                'SQL Injection',
                                payload,
                                f"Error pattern: {error}"
                            )
                            break
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except requests.exceptions.RequestException as e:
                    print(Colors.warning(f"Request failed: {str(e)[:50]}"))
                    continue
    
    def scan_xss(self):
        """Scan for XSS vulnerabilities"""
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
                    response = self.session.get(test_url, timeout=self.timeout)
                    response_text = response.text
                    
                    # Check if payload is reflected
                    if payload in response_text:
                        vuln_msg = f"XSS vulnerability found with payload: {payload[:30]}..."
                        print(Colors.error(vuln_msg))
                        self.reporter.add_vulnerability(
                            'Cross-Site Scripting (XSS)',
                            payload,
                            "Payload reflected in response"
                        )
                    
                    time.sleep(0.5)  # Rate limiting
                    
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
    
    parser.add_argument(
        '-u', '--url',
        required=True,
        help='Target URL to scan (e.g., http://example.com/page?id=1)'
    )
    
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
        '-v', '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    # Determine scan types
    if args.type == 'all':
        scan_types = ['sqli', 'xss']
    else:
        scan_types = [args.type]
    
    # Create and run scanner
    scanner = SecurityScanner(args.url, timeout=args.timeout)
    
    try:
        scanner.run_scan(scan_types)
    except KeyboardInterrupt:
        print(Colors.warning("\n\nScan interrupted by user"))
        sys.exit(0)
    except Exception as e:
        print(Colors.error(f"\nError: {str(e)}"))
        sys.exit(1)


if __name__ == '__main__':
    main()