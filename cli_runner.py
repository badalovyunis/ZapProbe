"""
ZapProbe CLI Runner - Easy User Interface
Users can initiate a scan via GUI or simple CLI
"""

import sys
import argparse
import os
from pathlib import Path

try:
    import PySimpleGUI as sg
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

from scanner import SecurityScanner, Colors


class ZapProbeRunner:
    """ZapProbe CLI Runner - Easy User Interface"""
    
    def __init__(self):
        self.gui_available = GUI_AVAILABLE
    
    def run_gui(self):
        """Graphical interface with PySimpleGUI"""
        if not GUI_AVAILABLE:
            print(Colors.error("PySimpleGUI is not installed. To install:"))
            print("  pip install PySimpleGUI")
            return
        
        # Configure theme
        sg.theme('DarkBlue3')
        
        # GUI layout
        layout = [
            [sg.Text('🔍 ZapProbe - Web Vulnerability Scanner', 
                    font=('Arial', 16, 'bold'))],
            
            [sg.Text('_' * 50)],
            
            # Target URL
            [sg.Text('Target URL:', font=('Arial', 11, 'bold')),
             sg.Input(key='-URL-', size=(40, 1), 
                     default_text='http://localhost:5000/search?id=1',
                     tooltip='e.g., http://localhost:5000/search?id=1')],
            
            # Scan Type
            [sg.Text('Scan Type:', font=('Arial', 11, 'bold')),
             sg.Radio('SQL Injection', 'SCAN_TYPE', default=True, key='-SQLI-'),
             sg.Radio('XSS', 'SCAN_TYPE', key='-XSS-'),
             sg.Radio('All', 'SCAN_TYPE', key='-ALL-')],
            
            # Timeout
            [sg.Text('Timeout (seconds):', font=('Arial', 11, 'bold')),
             sg.Input(default_text='10', size=(5, 1), key='-TIMEOUT-', 
                     tooltip='Request timeout duration'),
             sg.Text('Delay (seconds):', font=('Arial', 11, 'bold')),
             sg.Input(default_text='0.5', size=(5, 1), key='-DELAY-',
                     tooltip='Delay between requests')],
            
            # SSL Verification
            [sg.Checkbox('Verify SSL Certificate', 
                        default=True, key='-SSL-VERIFY-',
                        tooltip='Reject self-signed certificates')],
            
            # Proxy
            [sg.Text('Proxy (optional):', font=('Arial', 11, 'bold')),
             sg.Input(key='-PROXY-', size=(40, 1),
                     tooltip='e.g., http://127.0.0.1:8080 (Burp Suite)')],
            
            # Output
            [sg.Text('Output File (optional):', font=('Arial', 11, 'bold')),
             sg.Input(key='-OUTPUT-', size=(40, 1),
                     tooltip='e.g., report.json or report.html')],
            
            [sg.Text('_' * 50)],
            
            # Buttons
            [sg.Button('🚀 Start Scan', size=(20, 2), key='-SCAN-'),
             sg.Button('❌ Exit', size=(15, 2))],
            
            # Status/Output
            [sg.Multiline(size=(60, 15), key='-OUTPUT-TEXT-', 
                         disabled=True, background_color='black',
                         text_color='white', font=('Courier', 10))]
        ]
        
        # Create window
        window = sg.Window('ZapProbe Scanner', layout, finalize=True)
        
        # Event loop
        while True:
            event, values = window.read()
            
            if event == sg.WINDOW_CLOSED or event == '❌ Exit':
                break
            
            if event == '-SCAN-':
                url = values['-URL-'].strip()
                timeout = int(values['-TIMEOUT-'])
                delay = float(values['-DELAY-'])
                ssl_verify = values['-SSL-VERIFY-']
                proxy = values['-PROXY-'].strip() or None
                output_file = values['-OUTPUT-'].strip() or None
                
                if values['-SQLI-']:
                    scan_types = ['sqli']
                elif values['-XSS-']:
                    scan_types = ['xss']
                else:
                    scan_types = ['sqli', 'xss']
                
                if not url.startswith(('http://', 'https://')):
                    sg.popup_error('Error', 'Please enter a valid URL (http:// or https://)')
                    continue
                
                window['-OUTPUT-TEXT-'].update('')
      
                try:
                    window['-OUTPUT-TEXT-'].print(
                        f"🔄 Scan starting...\n"
                        f"📍 Target: {url}\n"
                        f"🎯 Type: {', '.join(scan_types)}\n"
                        f"{'=' * 60}\n"
                    )
                    window.refresh()
                    
                    scanner = SecurityScanner(
                        url,
                        timeout=timeout,
                        ssl_verify=ssl_verify,
                        proxy=proxy,
                        delay=delay
                    )
                    
                    scanner.run_scan(scan_types)
                    
                    window['-OUTPUT-TEXT-'].print(
                        f"\n✅ Scan completed!\n"
                        f"Vulnerabilities found: {len(scanner.reporter.vulnerabilities)}\n"
                    )
                    
                    if output_file:
                        scanner.reporter.export(output_file)
                        window['-OUTPUT-TEXT-'].print(
                            f"📄 Report saved: {output_file}\n"
                        )
                    
                except Exception as e:
                    window['-OUTPUT-TEXT-'].print(
                        f"❌ Error: {str(e)}\n"
                    )
        
        window.close()
    
    def run_quick_cli(self, url, scan_type='all', timeout=10, 
                      delay=0.5, ssl_verify=True, proxy=None, output=None):
        """Fast CLI - single line browsing"""
        
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            print(Colors.error("Please enter a valid URL (http:// or https://)"))
            return False
        
        if scan_type == 'all':
            scan_types = ['sqli', 'xss']
        else:
            scan_types = [scan_type]
        
        try:
            scanner = SecurityScanner(
                url,
                timeout=timeout,
                ssl_verify=ssl_verify,
                proxy=proxy,
                delay=delay
            )
            
            scanner.run_scan(scan_types)
            
            if output:
                scanner.reporter.export(output)
                print(Colors.success(f"Report saved: {output}"))
            
            return True
            
        except Exception as e:
            print(Colors.error(f"Error: {str(e)}"))
            return False


def main():
    """Home access point"""
    parser = argparse.ArgumentParser(
        prog='zapprobe',
        description='ZapProbe - Web Vulnerability Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start with GUI
  zapprobe --gui
  
  # Fast scan
  zapprobe http://localhost:5000/search?id=1
  
  # XSS scan only
  zapprobe http://localhost:5000/comment?text=test -t xss
  
  # Generate report
  zapprobe http://localhost:5000/search?id=1 -o report.html
        """
    )
    
    # GUI mode
    parser.add_argument(
        '--gui',
        action='store_true',
        help='GUI mode (PySimpleGUI required)'
    )
    
    # Target URL
    parser.add_argument(
        'url',
        nargs='?',
        default=None,
        help='Target URL (e.g., http://localhost:5000/search?id=1)'
    )
    
    # Scan type
    parser.add_argument(
        '-t', '--type',
        choices=['sqli', 'xss', 'all'],
        default='all',
        help='Scan type (default: all)'
    )
    
    # Timeout
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout (seconds, default: 10)'
    )
    
    # Delay
    parser.add_argument(
        '--delay',
        type=float,
        default=0.5,
        help='Delay between requests (seconds, default: 0.5)'
    )
    
    # SSL verification
    parser.add_argument(
        '--no-ssl-verify',
        action='store_true',
        help='Disable SSL certificate verification'
    )
    
    # Proxy
    parser.add_argument(
        '--proxy',
        type=str,
        help='HTTP proxy (e.g., http://127.0.0.1:8080)'
    )
    
    # Output
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file (JSON or HTML)'
    )
    
    # Version
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.2.0'
    )
    
    args = parser.parse_args()
    
    runner = ZapProbeRunner()
    
    # GUI mode
    if args.gui:
        print(Colors.info("Starting GUI mode..."))
        runner.run_gui()
        return
    
    # URL required
    if not args.url:
        if len(sys.argv) == 1:
            if runner.gui_available:
                print(Colors.info("Starting GUI mode..."))
                runner.run_gui()
            else:
                parser.print_help()
        else:
            parser.print_help()
        return
    
    # Quick CLI mode
    runner.run_quick_cli(
        url=args.url,
        scan_type=args.type,
        timeout=args.timeout,
        delay=args.delay,
        ssl_verify=not args.no_ssl_verify,
        proxy=args.proxy,
        output=args.output
    )


if __name__ == '__main__':
    main()
