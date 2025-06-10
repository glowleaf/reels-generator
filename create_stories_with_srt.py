#!/usr/bin/env python3
"""
Generate Greek beach stories and create SRT files with proper timing.
"""

import os
import re
from story_generator import GreekStoryGenerator

def estimate_narration_time(text):
    """Estimate narration time based on Greek text length and complexity."""
    # Average Greek speaking rate: ~3-4 characters per second for natural narration
    # Adjust for punctuation and pauses
    chars = len(text)
    words = len(text.split())
    
    # Base time: 3.5 chars per second
    base_time = chars / 3.5
    
    # Add pause time for punctuation
    commas = text.count(',')
    periods = text.count('.')
    pause_time = (commas * 0.3) + (periods * 0.5)
    
    return base_time + pause_time

def create_srt_from_story(story_text, target_duration=55):
    """Create SRT content from story text with proper timing."""
    # Split story into sentences
    sentences = [s.strip() for s in story_text.split('.') if s.strip()]
    
    if not sentences:
        return None
    
    # Calculate timing for each sentence
    total_estimated_time = sum(estimate_narration_time(sentence) for sentence in sentences)
    
    # Scale to target duration if needed
    time_scale = target_duration / total_estimated_time if total_estimated_time > 0 else 1
    
    srt_content = []
    current_time = 0.0
    
    for i, sentence in enumerate(sentences):
        sentence_duration = estimate_narration_time(sentence) * time_scale
        start_time = current_time
        end_time = current_time + sentence_duration
        
        # Convert to SRT time format
        start_h = int(start_time // 3600)
        start_m = int((start_time % 3600) // 60)
        start_s = int(start_time % 60)
        start_ms = int((start_time % 1) * 1000)
        
        end_h = int(end_time // 3600)
        end_m = int((end_time % 3600) // 60)
        end_s = int(end_time % 60)
        end_ms = int((end_time % 1) * 1000)
        
        srt_content.append(f"{i + 1}")
        srt_content.append(f"{start_h:02d}:{start_m:02d}:{start_s:02d},{start_ms:03d} --> {end_h:02d}:{end_m:02d}:{end_s:02d},{end_ms:03d}")
        srt_content.append(sentence)
        srt_content.append("")
        
        current_time = end_time
    
    return "\n".join(srt_content)

def get_next_story_number():
    """Get the next available story number."""
    i = 1
    while os.path.exists(f"output/stories/story_{i}.txt") or os.path.exists(f"output/captions/captions_{i}.srt"):
        i += 1
    return i

def main():
    """Generate 10 beach stories with SRT files."""
    generator = GreekStoryGenerator()
    
    # Create output directories
    os.makedirs("output/stories", exist_ok=True)
    os.makedirs("output/captions", exist_ok=True)
    
    # Beach theme
    theme = "γυναίκα που δεν ένιωθε καλά να πάει στην θάλασσα σκεφτόταν για το σώμα της αλλά τελικά το ξεπέρασε"
    
    # Find next available number and generate 10 stories
    start_num = get_next_story_number()
    for i in range(start_num, start_num + 10):
        print(f"\n🎬 Generating story {i}: Beach confidence story")
        
        story = generator.generate_story(theme, duration=60)
        if story:
            # Save story
            story_file = f"output/stories/story_{i}.txt"
            with open(story_file, 'w', encoding='utf-8') as f:
                f.write(story)
            print(f"✅ Saved story: {story_file}")
            
            # Create SRT file
            srt_content = create_srt_from_story(story, target_duration=55)
            if srt_content:
                srt_file = f"output/captions/captions_{i}.srt"
                with open(srt_file, 'w', encoding='utf-8') as f:
                    f.write(srt_content)
                print(f"✅ Saved SRT: {srt_file}")
                print(f"📝 Preview: {story[:100]}...")
            else:
                print(f"❌ Failed to create SRT for story {i}")
        else:
            print(f"❌ Failed to generate story {i}")

if __name__ == "__main__":
    main() 