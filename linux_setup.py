#!/usr/bin/env python3
"""
ZapProbe - Linux Installation and Usage Guide
Guide: Installing and using ZapProbe on Linux
"""

# This file is executable - it automates the steps

import subprocess
import sys
import os
import platform

class LinuxSetup:
    """Installation and setup for Linux systems"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.is_linux = self.os_type == "Linux"
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    
    def check_python(self):
        """Check for Python 3.8+"""
        print("🔍 Checking Python version...")
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ is required")
            print(f"   You have: Python {self.python_version}")
            return False
        print(f"✅ Python {self.python_version} found")
        return True
    
    def check_pip(self):
        """Check for pip"""
        print("🔍 Checking pip...")
        try:
            result = subprocess.run(
                ["pip", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ pip found: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            pass
        
        print("❌ pip not found")
        if self.os_type == "Linux":
            print("   Installation command:")
            print("   • Ubuntu/Debian: sudo apt-get install python3-pip")
            print("   • Fedora: sudo dnf install python3-pip")
            print("   • Arch: sudo pacman -S python-pip")
        return False
    
    def install_dependencies(self, with_gui=False):
        """Install dependencies"""
        print("\n📦 Installing dependencies...")
        
        try:
            subprocess.run(
                ["pip", "install", "-r", "requirements.txt"],
                check=True
            )
            print("✅ Core dependencies installed")
            
            if with_gui:
                print("📦 Installing PySimpleGUI...")
                subprocess.run(
                    ["pip", "install", "PySimpleGUI"],
                    check=True
                )
                print("✅ GUI installed")
            
            return True
        except subprocess.CalledProcessError:
            print("❌ Installation failed")
            return False
    
    def install_package(self, with_gui=False):
        """Install ZapProbe package"""
        print("\n📦 Installing ZapProbe package...")
        
        try:
            if with_gui:
                subprocess.run(
                    ["pip", "install", "-e", ".[gui]"],
                    check=True
                )
                print("✅ ZapProbe installed with GUI support")
            else:
                subprocess.run(
                    ["pip", "install", "-e", "."],
                    check=True
                )
                print("✅ ZapProbe installed")
            
            return True
        except subprocess.CalledProcessError:
            print("❌ Package installation failed")
            return False
    
    def test_installation(self):
        """Test that the installation was successful"""
        print("\n🧪 Testing installation...")
        
        try:
            result = subprocess.run(
                ["zapprobe", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ ZapProbe is working: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            pass
        
        print("⚠️  zapprobe command not found")
        print("   Solution:")
        print("   • Check pip install path: which pip")
        print("   • Or run directly: python -m cli_runner --version")
        return False
    
    def run_setup(self, with_gui=False):
        """Run the full installation"""
        print("=" * 60)
        print("🐧 ZapProbe - Linux Installation")
        print("=" * 60)
        
        # Checks
        if not self.check_python():
            return False
        
        if not self.check_pip():
            return False
        
        # Installation
        if not self.install_dependencies(with_gui):
            return False
        
        if not self.install_package(with_gui):
            return False
        
        # Test
        if not self.test_installation():
            return False
        
        print("\n" + "=" * 60)
        print("✅ Installation complete!")
        print("=" * 60)
        print("\n🚀 Usage:")
        print("   zapprobe --help                    # Help")
        print("   zapprobe --gui                     # Open GUI")
        print("   zapprobe http://localhost:5000/s   # Quick scan")
        print("\n")
        return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ZapProbe Linux Setup")
    parser.add_argument("--gui", action="store_true", help="Also install GUI support")
    args = parser.parse_args()
    
    setup = LinuxSetup()
    success = setup.run_setup(with_gui=args.gui)
    
    sys.exit(0 if success else 1)