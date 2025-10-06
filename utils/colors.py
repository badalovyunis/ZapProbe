"""
Color codes for terminal output
"""

from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class Colors:
    """Terminal color codes"""
    
    # Basic colors
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    
    # Styles
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL
    
    # Status colors
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    INFO = Fore.CYAN
    
    @staticmethod
    def success(text):
        """Print success message"""
        return f"{Colors.SUCCESS}[✓] {text}{Colors.RESET}"
    
    @staticmethod
    def error(text):
        """Print error message"""
        return f"{Colors.ERROR}[✗] {text}{Colors.RESET}"
    
    @staticmethod
    def warning(text):
        """Print warning message"""
        return f"{Colors.WARNING}[!] {text}{Colors.RESET}"
    
    @staticmethod
    def info(text):
        """Print info message"""
        return f"{Colors.INFO}[i] {text}{Colors.RESET}"