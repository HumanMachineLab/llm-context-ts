#!/usr/bin/env python3
"""
Setup script for LLM-based Text Segmentation project.

This setup script helps with:
1. Installing dependencies
2. Setting up the development environment
3. Downloading required NLTK data
4. Checking system requirements
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors gracefully."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True

def install_requirements():
    """Install Python requirements."""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def setup_nltk_data():
    """Download required NLTK data."""
    print("📚 Setting up NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ NLTK setup failed: {e}")
        return False

def check_ollama():
    """Check if Ollama is installed and accessible."""
    print("🤖 Checking Ollama installation...")
    try:
        result = subprocess.run("ollama --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed")
            return True
        else:
            print("⚠️  Ollama not found. Install from: https://ollama.ai/")
            return False
    except Exception:
        print("⚠️  Ollama not found. Install from: https://ollama.ai/")
        return False

def setup_environment_file():
    """Create a template .env file if it doesn't exist."""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env template file...")
        with open(env_file, 'w') as f:
            f.write("# OpenAI API Key (optional, for GPT models)\n")
            f.write("# OPENAI_API_KEY=your_api_key_here\n")
            f.write("\n")
            f.write("# Other configuration options\n")
            f.write("# MAX_CONTEXT_WINDOW=5\n")
        print("✅ .env template created. Add your API keys if needed.")
        return True
    else:
        print("✅ .env file already exists")
        return True

def create_directories():
    """Create necessary directories."""
    directories = ['data', 'outputs', 'logs']
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"📁 Created directory: {dir_name}")
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up LLM-Based Text Segmentation Project")
    print("=" * 60)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Install requirements
    if success and not install_requirements():
        success = False
    
    # Setup NLTK data
    if success and not setup_nltk_data():
        success = False
    
    # Check Ollama (optional)
    check_ollama()  # Don't fail if Ollama is not installed
    
    # Setup environment file
    if success and not setup_environment_file():
        success = False
    
    # Create directories
    if success and not create_directories():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Install Ollama from https://ollama.ai/ (if not already installed)")
        print("   2. Pull required models: ollama pull mistral")
        print("   3. Add OpenAI API key to .env file (optional)")
        print("   4. Run example: python example.py")
        print("   5. Explore notebooks in the notebooks/ directory")
    else:
        print("❌ Setup encountered some issues. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 