"""
Report generator for scan results
"""

from datetime import datetime
from .colors import Colors


class Reporter:
    """Generate scan reports"""
    
    def __init__(self, target_url):
        self.target_url = target_url
        self.vulnerabilities = []
        self.scan_time = datetime.now()
    
    def add_vulnerability(self, vuln_type, payload, response_info):
        """Add found vulnerability to report"""
        self.vulnerabilities.append({
            'type': vuln_type,
            'payload': payload,
            'response': response_info,
            'timestamp': datetime.now()
        })
    
    def print_summary(self):
        """Print scan summary"""
        print("\n" + "="*60)
        print(Colors.BOLD + "SCAN SUMMARY" + Colors.RESET)
        print("="*60)
        print(f"Target URL: {self.target_url}")
        print(f"Scan Time: {self.scan_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Vulnerabilities Found: {len(self.vulnerabilities)}")
        print("="*60 + "\n")
        
        if self.vulnerabilities:
            for i, vuln in enumerate(self.vulnerabilities, 1):
                print(Colors.error(f"Vulnerability #{i}:"))
                print(f"  Type: {vuln['type']}")
                print(f"  Payload: {vuln['payload'][:50]}...")
                print(f"  Time: {vuln['timestamp'].strftime('%H:%M:%S')}")
                print("-"*60)
        else:
            print(Colors.success("No vulnerabilities found!"))