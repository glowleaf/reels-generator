#!/usr/bin/env python3
"""
Demo script for Greek Social Story Video Generator
Shows how to use the individual components and create videos programmatically.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from story_generator import GreekStoryGenerator
from audio_generator import GreekAudioGenerator
from caption_generator import GreekCaptionGenerator
from video_processor import GreekVideoProcessor

def demo_story_generation():
    """Demo the story generation functionality."""
    print("🇬🇷 Demo: Story Generation")
    print("-" * 30)
    
    generator = GreekStoryGenerator()
    
    # Generate a story
    story = generator.generate_story("διατροφή και αυτοπεποίθηση", 30)
    
    if story:
        print(f"✅ Generated story:")
        print(f"📝 {story}")
        print(f"📊 Length: {len(story)} characters")
    else:
        print("❌ Failed to generate story")
    
    return story

def demo_audio_generation(text):
    """Demo the audio generation functionality."""
    print("\n🎙️ Demo: Audio Generation")
    print("-" * 30)
    
    generator = GreekAudioGenerator()
    
    # Test voice first
    print("Testing voice...")
    test_result = generator.test_voice()
    
    if test_result:
        print("✅ Voice test successful")
        
        # Generate audio for the story
        audio_file = generator.generate_audio(text, "demo_audio.mp3")
        if audio_file:
            print(f"✅ Audio generated: {audio_file}")
            return audio_file
    
    print("❌ Audio generation failed")
    return None

def demo_caption_generation(text):
    """Demo the caption generation functionality."""
    print("\n📝 Demo: Caption Generation")
    print("-" * 30)
    
    generator = GreekCaptionGenerator()
    
    # Create captions
    caption_file = generator.create_captions(text, 30, "demo_captions.srt")
    
    if caption_file:
        print(f"✅ Captions created: {caption_file}")
        
        # Preview captions
        generator.preview_captions(caption_file)
        return caption_file
    
    print("❌ Caption generation failed")
    return None

def demo_video_processing():
    """Demo the video processing functionality."""
    print("\n🎬 Demo: Video Processing")
    print("-" * 30)
    
    processor = GreekVideoProcessor()
    
    # Create a background video
    bg_video = processor.create_background_video("black", 30, "demo_background.mp4")
    
    if bg_video:
        print(f"✅ Background video created: {bg_video}")
        return bg_video
    
    print("❌ Video processing failed")
    return None

def run_complete_demo():
    """Run a complete demo of all functionality."""
    print("🚀 Running Complete Greek Video Generator Demo")
    print("=" * 50)
    
    # Check environment
    if not os.path.exists('.env'):
        print("⚠️ .env file not found. Please create it with your API keys.")
        return
    
    # Step 1: Generate story
    story = demo_story_generation()
    if not story:
        return
    
    # Step 2: Generate audio
    audio_file = demo_audio_generation(story)
    if not audio_file:
        print("⚠️ Skipping audio demo - check your ElevenLabs API key")
    
    # Step 3: Generate captions
    caption_file = demo_caption_generation(story)
    if not caption_file:
        return
    
    # Step 4: Create background video
    bg_video = demo_video_processing()
    if not bg_video:
        return
    
    # Step 5: Combine everything (if audio was successful)
    if audio_file:
        print("\n🎬 Demo: Complete Video Creation")
        print("-" * 30)
        
        processor = GreekVideoProcessor()
        final_video = processor.create_video_with_captions(
            background_video=bg_video,
            audio_file=audio_file,
            caption_file=caption_file,
            output_filename="demo_final_video.mp4"
        )
        
        if final_video:
            print(f"🎉 Complete demo video created: {final_video}")
        else:
            print("❌ Final video creation failed")
    
    print("\n✨ Demo completed!")

if __name__ == "__main__":
    run_complete_demo() 