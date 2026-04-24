"""
Report generator for scan results
"""

from datetime import datetime
import json
import os
from .colors import Colors


class Reporter:
    """Generate scan reports"""
    
    # CVSS v3.1 Severity Ratings
    CVSS_RATINGS = {
        'SQL Injection': 9.8,           # Critical
        'Cross-Site Scripting (XSS)': 7.1,  # High
        'Remote Code Execution': 10.0,  # Critical
        'Authentication Bypass': 8.8,   # High
    }
    
    def __init__(self, target_url):
        self.target_url = target_url
        self.vulnerabilities = []
        self.scan_start_time = datetime.now()
    
    def add_vulnerability(self, vuln_type, payload, response_info, param_name=None):
        """Add found vulnerability to report"""
        cvss_score = self.CVSS_RATINGS.get(vuln_type, 7.5)
        
        self.vulnerabilities.append({
            'type': vuln_type,
            'payload': payload,
            'response': response_info,
            'parameter': param_name or 'N/A',
            'timestamp': datetime.now().isoformat(),
            'cvss_score': cvss_score,
            'severity': self._get_severity(cvss_score)
        })
    
    def _get_severity(self, cvss_score):
        """Get severity level based on CVSS score"""
        if cvss_score >= 9.0:
            return 'Critical'
        elif cvss_score >= 7.0:
            return 'High'
        elif cvss_score >= 4.0:
            return 'Medium'
        else:
            return 'Low'
    
    def print_summary(self):
        """Print scan summary to terminal"""
        scan_duration = datetime.now() - self.scan_start_time
        
        print("\n" + "="*60)
        print(Colors.BOLD + "SCAN SUMMARY" + Colors.RESET)
        print("="*60)
        print(f"Target URL: {self.target_url}")
        print(f"Scan Start: {self.scan_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Scan Duration: {str(scan_duration).split('.')[0]}")
        print(f"Total Vulnerabilities Found: {len(self.vulnerabilities)}")
        
        if self.vulnerabilities:
            # Group by severity
            by_severity = {}
            for vuln in self.vulnerabilities:
                sev = vuln['severity']
                by_severity[sev] = by_severity.get(sev, 0) + 1
            
            print("\nVulnerabilities by Severity:")
            for severity in ['Critical', 'High', 'Medium', 'Low']:
                count = by_severity.get(severity, 0)
                if count > 0:
                    if severity == 'Critical':
                        print(Colors.error(f"  {severity}: {count}"))
                    elif severity == 'High':
                        print(Colors.warning(f"  {severity}: {count}"))
                    else:
                        print(f"  {severity}: {count}")
        
        print("="*60 + "\n")
        
        if self.vulnerabilities:
            for i, vuln in enumerate(self.vulnerabilities, 1):
                severity_color = self._get_severity_color(vuln['severity'])
                print(severity_color + f"Vulnerability #{i}:" + Colors.RESET)
                print(f"  Type: {vuln['type']}")
                print(f"  Severity: {vuln['severity']} (CVSS: {vuln['cvss_score']})")
                print(f"  Parameter: {vuln['parameter']}")
                print(f"  Payload: {vuln['payload'][:60]}...")
                print(f"  Detection: {vuln['response']}")
                print(f"  Time: {vuln['timestamp']}")
                print("-"*60)
        else:
            print(Colors.success("✓ No vulnerabilities found!"))
    
    def _get_severity_color(self, severity):
        """Get color code for severity level"""
        if severity == 'Critical':
            return Colors.ERROR
        elif severity == 'High':
            return Colors.WARNING
        else:
            return Colors.INFO
    
    def export(self, output_file):
        """Export report to file (JSON or HTML based on extension)"""
        file_ext = os.path.splitext(output_file)[1].lower()
        
        if file_ext == '.json':
            self._export_json(output_file)
        elif file_ext == '.html':
            self._export_html(output_file)
        else:
            # Default to JSON
            self._export_json(output_file)
    
    def _export_json(self, output_file):
        """Export report to JSON file"""
        report_data = {
            'metadata': {
                'tool': 'ZapProbe',
                'version': '0.2.0',
                'scan_start': self.scan_start_time.isoformat(),
                'scan_end': datetime.now().isoformat(),
                'target_url': self.target_url
            },
            'summary': {
                'total_vulnerabilities': len(self.vulnerabilities),
                'critical': sum(1 for v in self.vulnerabilities if v['severity'] == 'Critical'),
                'high': sum(1 for v in self.vulnerabilities if v['severity'] == 'High'),
                'medium': sum(1 for v in self.vulnerabilities if v['severity'] == 'Medium'),
                'low': sum(1 for v in self.vulnerabilities if v['severity'] == 'Low'),
            },
            'vulnerabilities': self.vulnerabilities
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    def _export_html(self, output_file):
        """Export report to HTML file"""
        scan_duration = datetime.now() - self.scan_start_time
        
        # Count by severity
        critical_count = sum(1 for v in self.vulnerabilities if v['severity'] == 'Critical')
        high_count = sum(1 for v in self.vulnerabilities if v['severity'] == 'High')
        medium_count = sum(1 for v in self.vulnerabilities if v['severity'] == 'Medium')
        low_count = sum(1 for v in self.vulnerabilities if v['severity'] == 'Low')
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZapProbe Scan Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .metadata {{
            font-size: 14px;
            opacity: 0.9;
            margin-top: 15px;
        }}
        
        .metadata p {{
            margin: 5px 0;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #ddd;
        }}
        
        .summary-card.critical {{
            border-left-color: #dc3545;
        }}
        
        .summary-card.critical .count {{
            color: #dc3545;
        }}
        
        .summary-card.high {{
            border-left-color: #fd7e14;
        }}
        
        .summary-card.high .count {{
            color: #fd7e14;
        }}
        
        .summary-card.medium {{
            border-left-color: #ffc107;
        }}
        
        .summary-card.medium .count {{
            color: #ffc107;
        }}
        
        .summary-card.low {{
            border-left-color: #28a745;
        }}
        
        .summary-card.low .count {{
            color: #28a745;
        }}
        
        .count {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .label {{
            font-size: 14px;
            color: #666;
        }}
        
        .vulnerabilities {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .vuln-item {{
            padding: 20px;
            border-bottom: 1px solid #eee;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .vuln-item:last-child {{
            border-bottom: none;
        }}
        
        .vuln-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        
        .vuln-type {{
            font-weight: bold;
            font-size: 16px;
        }}
        
        .severity-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }}
        
        .severity-critical {{
            background: #dc3545;
        }}
        
        .severity-high {{
            background: #fd7e14;
        }}
        
        .severity-medium {{
            background: #ffc107;
            color: #333;
        }}
        
        .severity-low {{
            background: #28a745;
        }}
        
        .vuln-details {{
            font-size: 13px;
            color: #666;
        }}
        
        .vuln-details p {{
            margin: 8px 0;
        }}
        
        .payload {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            word-break: break-all;
            margin: 10px 0;
            font-size: 12px;
        }}
        
        footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 ZapProbe Security Scan Report</h1>
            <div class="metadata">
                <p><strong>Target:</strong> {self.target_url}</p>
                <p><strong>Scan Date:</strong> {self.scan_start_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Scan Duration:</strong> {str(scan_duration).split('.')[0]}</p>
            </div>
        </header>
        
        <div class="summary">
            <div class="summary-card critical">
                <div class="count">{critical_count}</div>
                <div class="label">Critical</div>
            </div>
            <div class="summary-card high">
                <div class="count">{high_count}</div>
                <div class="label">High</div>
            </div>
            <div class="summary-card medium">
                <div class="count">{medium_count}</div>
                <div class="label">Medium</div>
            </div>
            <div class="summary-card low">
                <div class="count">{low_count}</div>
                <div class="label">Low</div>
            </div>
            <div class="summary-card">
                <div class="count">{len(self.vulnerabilities)}</div>
                <div class="label">Total Issues</div>
            </div>
        </div>
        
        <h2 style="margin-bottom: 20px;">Vulnerabilities</h2>
        <div class="vulnerabilities">
"""
        
        if self.vulnerabilities:
            for i, vuln in enumerate(self.vulnerabilities, 1):
                severity_class = vuln['severity'].lower()
                html_content += f"""
            <div class="vuln-item">
                <div>
                    <div class="vuln-header">
                        <span class="vuln-type">#{i} {vuln['type']}</span>
                        <span class="severity-badge severity-{severity_class}">{vuln['severity']}</span>
                    </div>
                    <div class="vuln-details">
                        <p><strong>Parameter:</strong> {vuln['parameter']}</p>
                        <p><strong>CVSS Score:</strong> {vuln['cvss_score']}/10</p>
                        <p><strong>Detection Method:</strong> {vuln['response']}</p>
                    </div>
                </div>
                <div>
                    <p><strong>Payload:</strong></p>
                    <div class="payload">{vuln['payload']}</div>
                    <p><strong>Timestamp:</strong> {vuln['timestamp']}</p>
                </div>
            </div>
"""
        else:
            html_content += """
            <div style="padding: 30px; text-align: center; color: #28a745;">
                <p style="font-size: 18px; font-weight: bold;">✓ No vulnerabilities found!</p>
            </div>
"""
        
        html_content += """
        </div>
        
        <footer>
            <p>Generated by ZapProbe v0.2.0 - Educational Web Vulnerability Scanner</p>
            <p>⚠️ Use responsibly and only on authorized targets!</p>
        </footer>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
