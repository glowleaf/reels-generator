#!/usr/bin/env python3
"""
🇬🇷 Greek Social Story Video Generator
=====================================

Automated tool for creating Greek-captioned story videos using:
- OpenAI GPT-4 for story generation
- ElevenLabs for Greek text-to-speech
- FFmpeg for video processing

Author: AI Assistant
"""

import sys
import os
import argparse
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from story_generator import GreekStoryGenerator
from audio_generator import GreekAudioGenerator
from caption_generator import GreekCaptionGenerator
from video_processor import VideoProcessor
from config import Config

class GreekVideoCreator:
    def __init__(self):
        self.story_generator = GreekStoryGenerator()
        self.audio_generator = GreekAudioGenerator()
        self.caption_generator = GreekCaptionGenerator()
        self.video_processor = VideoProcessor()
        
        # Create output directory if it doesn't exist
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    def create_complete_video(self, topic, background_video, duration=60, output_file=None):
        """Create a complete video with story, audio, and captions"""
        print("\n🇬🇷 Starting Greek Video Creation")
        print("=" * 50 + "\n")
        
        try:
            # 1. Generate story
            print(f"1️⃣ Creating story for topic: '{topic}'")
            story = self.story_generator.generate_story(topic=topic, duration=duration)
            if not story:
                print("❌ Failed to generate story")
                return None
            print(f"✅ Story generated ({len(story)} characters)")
            print(f"📝 Content: {story[:100]}...")
            
            # 2. Generate audio
            print("\n2️⃣ Generating audio")
            audio_path = self.audio_generator.generate_audio(story)
            if not audio_path:
                print("❌ Failed to generate audio")
                return None
            
            # 3. Generate captions
            print("\n3️⃣ Generating captions")
            captions_path = self.caption_generator.generate_captions(story)
            if not captions_path:
                print("❌ Failed to generate captions")
                return None
            
            # 4. Prepare background video
            print("\n4️⃣ Preparing background video")
            if not os.path.exists(background_video):
                print(f"❌ Background video not found: {background_video}")
                return None
            print(f"📹 Using existing video: {background_video}")
            
            # Create output filename if not provided
            if not output_file:
                topic_slug = "_".join(topic.split()[:5])  # Take first 5 words
                output_file = os.path.join(Config.OUTPUT_DIR, f"greek_story_{topic_slug}.mp4")
            
            # 5. Create final video
            print("\n5️⃣ Creating final video")
            # First create the looped background
            temp_bg = self.video_processor.prepare_background_video(
                background_video,
                duration,
                os.path.join(Config.OUTPUT_DIR, "temp_looped_bg.mp4")
            )
            if not temp_bg:
                print("❌ Failed to prepare background video")
                return None
            
            # Then create the final video with the looped background
            final_video = self.video_processor.create_final_video(
                temp_bg,
                audio_path,
                captions_path,
                output_file
            )
            
            if not final_video:
                print("❌ Failed to create final video")
                return None
            
            print(f"\n🎉 SUCCESS! Video created:")
            print(f"📁 Location: {output_file}")
            print(f"📝 Story: {story}")
            
            return {
                "video_path": output_file,
                "story": story,
                "audio_path": audio_path,
                "captions_path": captions_path
            }
            
        except Exception as e:
            print(f"❌ Error creating video: {e}")
            return None

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Greek Social Story Video Generator')
    parser.add_argument('prompt', type=str, help='The story prompt/topic')
    parser.add_argument('--duration', type=int, default=180, help='Video duration in seconds (default: 180)')
    parser.add_argument('--background', type=str, help='Path to background video file')
    parser.add_argument('--output', type=str, help='Output video filename')
    
    args = parser.parse_args()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Αρχείο .env δεν βρέθηκε!")
        print("📝 Παρακαλώ δημιουργήστε αρχείο .env με βάση το .env.example")
        print("🔑 Χρειάζεστε API keys από OpenAI και ElevenLabs")
        return
    
    # Check API keys
    if not Config.OPENAI_API_KEY or not Config.ELEVENLABS_API_KEY:
        print("⚠️  Λείπουν API keys!")
        print("🔑 Ελέγξτε το αρχείο .env σας")
        return
    
    creator = GreekVideoCreator()
    
    # Create video with command line arguments
    result = creator.create_complete_video(
        topic=args.prompt,
        background_video=args.background,
        duration=args.duration,
        output_file=args.output
    )
    
    if result:
        print(f"\n🎬 Video created: {result['video_path']}")

if __name__ == "__main__":
    main() 