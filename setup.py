#!/usr/bin/env python3
"""
Setup script for the Local AI Agent Test
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def check_env_file():
    """Check if .env file is properly configured"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        return False
    
    with open('.env', 'r') as f:
        content = f.read().strip()
    
    if 'PASTE_YOUR_API_KEY_HERE' in content:
        print("⚠️  Please update your .env file with your actual Google AI API key!")
        print("   Go to https://aistudio.google.com/ to get your API key.")
        return False
    
    print("✅ .env file is configured!")
    return True

def main():
    print("🚀 Setting up Local AI Agent Test Environment")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Check environment
    if not check_env_file():
        print("\n📝 Next steps:")
        print("1. Get your API key from https://aistudio.google.com/")
        print("2. Update the .env file with your actual API key")
        print("3. Run: python agent.py")
        return
    
    print("\n🎉 Setup complete! You can now run:")
    print("   python agent.py")

if __name__ == "__main__":
    main() 