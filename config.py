import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID')
    
    # Default video settings
    DEFAULT_VIDEO_DURATION = 60  # Changed to 60 seconds (1 minute)
    AUDIO_FORMAT = "mp3"
    VIDEO_FORMAT = "mp4"
    
    # Paths
    OUTPUT_DIR = "output"
    ASSETS_DIR = "assets"
    FONTS_DIR = "fonts"
    
    # Caption settings
    CAPTION_FONT_SIZE = 20  # Changed from 24 to 20
    CAPTION_FONT_COLOR = "white"
    CAPTION_OUTLINE_COLOR = "black"
    CAPTION_OUTLINE_WIDTH = 2 