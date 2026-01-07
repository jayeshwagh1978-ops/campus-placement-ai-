"""
Package management utilities for the Campus Placement AI Platform
"""

import subprocess
import sys

def install_packages():
    """Install required packages with proper version handling"""
    packages = [
        "streamlit==1.52.2",
        "pandas==2.2.0",
        "numpy==1.26.0",
        "plotly==5.18.0",
        "altair==5.2.0",
        "sqlalchemy==2.0.23",
        "pymongo==4.5.0",
        "python-dotenv==1.0.0",
        "pyjwt==2.8.0",
        "requests==2.31.0",
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ Installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install: {package}")
            print(f"Error: {e}")

if __name__ == "__main__":
    install_packages()
