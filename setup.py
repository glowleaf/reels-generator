#!/usr/bin/env python3
"""
Setup script for Greek Social Story Video Generator
Helps users configure the environment and check dependencies.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, check=True)
        print("✅ FFmpeg is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found")
        print("📥 Download from: https://ffmpeg.org/download.html")
        return False

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_path = Path('.env')
    
    if env_path.exists():
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    
    # Get API keys from user
    openai_key = input("🔑 Enter your OpenAI API key: ").strip()
    elevenlabs_key = input("🔑 Enter your ElevenLabs API key: ").strip()
    voice_id = input("🎙️ Enter your Greek voice ID (optional): ").strip()
    
    env_content = f"""# Greek Social Story Video Generator - Environment Variables
# Get your OpenAI API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY={openai_key}

# Get your ElevenLabs API key from: https://elevenlabs.io/api
ELEVENLABS_API_KEY={elevenlabs_key}

# Find a Greek voice ID in your ElevenLabs dashboard
ELEVENLABS_VOICE_ID={voice_id}
"""
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ .env file created")
    return True

def create_directories():
    """Create necessary directories."""
    directories = ['output', 'assets', 'fonts']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}/")
    
    return True

def download_greek_font():
    """Optionally download a Greek-compatible font."""
    fonts_dir = Path('fonts')
    dejavu_font = fonts_dir / 'DejaVuSans.ttf'
    
    if dejavu_font.exists():
        print("✅ Greek font already available")
        return True
    
    download = input("📝 Download DejaVu Sans font for Greek support? (y/n): ").strip().lower()
    
    if download in ['y', 'yes']:
        try:
            import requests
            url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf"
            
            print("📥 Downloading DejaVu Sans font...")
            response = requests.get(url)
            response.raise_for_status()
            
            with open(dejavu_font, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Font downloaded: {dejavu_font}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to download font: {e}")
            print("💡 You can manually place a Greek font in the fonts/ directory")
            return False
    
    return True

def test_setup():
    """Test the setup by running a simple demo."""
    test = input("🧪 Run setup test? (y/n): ").strip().lower()
    
    if test in ['y', 'yes']:
        print("🚀 Running setup test...")
        try:
            from story_generator import GreekStoryGenerator
            generator = GreekStoryGenerator()
            print("✅ Story generator works")
            
            from caption_generator import GreekCaptionGenerator
            caption_gen = GreekCaptionGenerator()
            print("✅ Caption generator works")
            
            from video_processor import GreekVideoProcessor
            video_proc = GreekVideoProcessor()
            print("✅ Video processor works")
            
            print("🎉 Setup test completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Setup test failed: {e}")
            return False
    
    return True

def main():
    """Main setup function."""
    print("🇬🇷 Greek Social Story Video Generator - Setup")
    print("=" * 50)
    
    # Check system requirements
    print("\n1️⃣ Checking system requirements...")
    if not check_python_version():
        return False
    
    ffmpeg_ok = check_ffmpeg()
    
    # Install dependencies
    print("\n2️⃣ Installing dependencies...")
    if not install_dependencies():
        return False
    
    # Create environment file
    print("\n3️⃣ Configuring environment...")
    if not create_env_file():
        return False
    
    # Create directories
    print("\n4️⃣ Creating directories...")
    create_directories()
    
    # Download Greek font
    print("\n5️⃣ Setting up Greek font...")
    download_greek_font()
    
    # Test setup
    print("\n6️⃣ Testing setup...")
    test_setup()
    
    # Final instructions
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("  1. Run: python main.py --interactive")
    print("  2. Or try: python demo.py")
    
    if not ffmpeg_ok:
        print("\n⚠️  Don't forget to install FFmpeg for video processing!")
    
    return True

if __name__ == "__main__":
    main() 