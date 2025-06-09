from main import GreekVideoCreator
import os
import shutil
from pathlib import Path

def create_multiple_beach_stories(num_variations=10):
    creator = GreekVideoCreator()
    
    # Story parameters
    story_prompt = "Μια γυναίκα που πάλευε με την εικόνα του σώματός της στην παραλία, αλλά τελικά βρήκε την αυτοπεποίθησή της"
    background_video = "assets/daphnebeach.mp4"
    duration = 60
    
    # Prepare output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # First, create and save the looped background video once
    print("\n🎬 Preparing looped background video...")
    temp_bg = creator.video_processor.prepare_background_video(
        background_video,
        duration,
        output_dir / "temp_looped_bg.mp4"
    )
    
    if not temp_bg:
        print("❌ Failed to create looped background video")
        return
    
    print("✅ Background video prepared successfully")
    
    # Generate multiple variations
    for i in range(num_variations):
        print(f"\n📝 Generating story variation {i+1}/{num_variations}")
        
        # Create unique output filename
        output_filename = f"beach_story_variation_{i+1}.mp4"
        
        try:
            # Generate new story and audio
            story = creator.story_generator.generate_story(
                topic=story_prompt,
                duration=duration
            )
            
            if not story:
                print(f"❌ Failed to generate story for variation {i+1}")
                continue
                
            # Create audio
            audio_path = creator.audio_generator.generate_audio(story)
            if not audio_path:
                print(f"❌ Failed to generate audio for variation {i+1}")
                continue
            
            # Create captions
            captions_path = creator.caption_generator.generate_captions(story)
            if not captions_path:
                print(f"❌ Failed to generate captions for variation {i+1}")
                continue
            
            # Create final video using the pre-looped background
            final_video = creator.video_processor.create_final_video(
                temp_bg,  # Use the pre-looped background
                audio_path,
                captions_path,
                output_dir / output_filename
            )
            
            if final_video:
                print(f"✅ Video {i+1} created successfully: {output_filename}")
                print(f"\n📝 Story {i+1}:\n{story}\n")
            else:
                print(f"❌ Failed to create final video for variation {i+1}")
            
        except Exception as e:
            print(f"❌ Error processing variation {i+1}: {e}")
            continue
    
    # Clean up temporary files
    print("\n🧹 Cleaning up temporary files...")
    for temp_file in output_dir.glob("temp_*"):
        try:
            temp_file.unlink()
        except Exception as e:
            print(f"Warning: Could not delete {temp_file}: {e}")

if __name__ == "__main__":
    create_multiple_beach_stories() 