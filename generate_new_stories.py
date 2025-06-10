#!/usr/bin/env python3
"""
Generate 10 new longer Greek stories for 50-60 seconds of narration.
"""

import os
from story_generator import GreekStoryGenerator

def main():
    """Generate 10 new longer stories."""
    generator = GreekStoryGenerator()
    
    # Create output directory
    os.makedirs("output/stories", exist_ok=True)
    
    # Beach/body confidence theme - the one we've been working on
    theme = "γυναίκα που δεν ένιωθε καλά να πάει στην θάλασσα σκεφτόταν για το σώμα της αλλά τελικά το ξεπέρασε"
    
    # Generate 10 new longer beach stories
    for i in range(1, 11):
        print(f"\n🎬 Generating story {i}: {theme}")
        
        story = generator.generate_story(theme, duration=60)
        if story:
            # Save to file
            story_file = f"output/stories/story_{30+i}.txt"
            with open(story_file, 'w', encoding='utf-8') as f:
                f.write(story)
            print(f"✅ Saved: {story_file}")
            print(f"📝 Preview: {story[:100]}...")
        else:
            print(f"❌ Failed to generate story {i}")

if __name__ == "__main__":
    main() 