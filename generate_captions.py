#!/usr/bin/env python3
"""
Generate multiple SRT caption files for beach stories.
"""

import os
from pathlib import Path
from story_generator import GreekStoryGenerator
from caption_generator import GreekCaptionGenerator

def get_next_number(directory, prefix, suffix):
    """Get the next available number for a file."""
    existing_files = []
    for f in os.listdir(directory):
        if f.startswith(prefix) and f.endswith(suffix):
            try:
                num = int(f[len(prefix):-len(suffix)])
                existing_files.append(num)
            except ValueError:
                continue
    return max(existing_files, default=0) + 1

def generate_story_captions(num_variations=10, duration=60):
    """Generate multiple story variations and their caption files."""
    
    # Initialize generators
    story_gen = GreekStoryGenerator()
    caption_gen = GreekCaptionGenerator()
    
    # Create output directories
    output_dir = Path("output")
    stories_dir = output_dir / "stories"
    captions_dir = output_dir / "captions"
    output_dir.mkdir(exist_ok=True)
    stories_dir.mkdir(exist_ok=True)
    captions_dir.mkdir(exist_ok=True)
    
    # Story prompt
    story_prompt = "Μια γυναίκα που πάλευε με την εικόνα του σώματός της στην παραλία, αλλά τελικά βρήκε την αυτοπεποίθησή της"
    
    # Generate variations
    for _ in range(num_variations):
        # Get next available numbers
        story_num = get_next_number(stories_dir, "story_variation_", ".txt")
        caption_num = get_next_number(captions_dir, "captions_", ".srt")
        
        print(f"\n📝 Generating story and captions variation {story_num}")
        
        try:
            # Generate story
            story = story_gen.generate_story(
                topic=story_prompt,
                duration=duration
            )
            
            if not story:
                print(f"❌ Failed to generate story for variation {story_num}")
                continue
            
            # Save story to text file
            story_path = stories_dir / f"story_variation_{story_num}.txt"
            with open(story_path, 'w', encoding='utf-8') as f:
                f.write(f"Story Variation {story_num}\n")
                f.write("=" * 50 + "\n\n")
                f.write(story)
            print(f"📄 Story saved to: {story_path}")
            
            # Generate captions
            caption_path = captions_dir / f"captions_{caption_num}.srt"
            caption_gen.create_captions(
                text=story,
                duration=duration,
                output_filename=str(caption_path)
            )
            
            if not caption_path.exists():
                print(f"❌ Failed to generate captions for variation {caption_num}")
                continue
                
            print(f"✅ Captions created: {caption_path}")
            
        except Exception as e:
            print(f"❌ Error processing variation: {e}")
            continue

if __name__ == "__main__":
    generate_story_captions() 