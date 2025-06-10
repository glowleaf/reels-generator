import os
import subprocess
import sys
from pathlib import Path

def get_next_number():
    """Get the next available number for the output video."""
    i = 1
    while os.path.exists(f"output/final/final_{i}.mp4"):
        i += 1
    return i

def create_final_video(srt_file, background_video, output_file):
    """Create a final video with background, audio, and captions."""
    # Get the corresponding story file
    story_num = srt_file.stem.split('_')[1]
    
    # Check if all input files exist
    if not all(f.exists() for f in [srt_file, Path(background_video)]):
        print(f"❌ Missing input files for {output_file}")
        return False
        
    # Create output directories if they don't exist
    os.makedirs("output/final", exist_ok=True)
    os.makedirs("output/audio", exist_ok=True)
    os.makedirs("output/temp", exist_ok=True)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Generate audio from the SRT caption file using ElevenLabs
    audio_file = f"output/audio/audio_{story_num}.mp3"
    if not os.path.exists(audio_file):
        try:
            # Extract text from SRT file
            with open(srt_file, 'r', encoding='utf-8') as f:
                srt_content = f.read().strip()
            
            # Extract just the text from SRT (remove timestamps and line numbers)
            import re
            # Remove SRT formatting and extract just the Greek text
            text_lines = []
            for line in srt_content.split('\n'):
                line = line.strip()
                # Skip empty lines, numbers, and timestamp lines
                if (line and 
                    not line.isdigit() and 
                    not re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line)):
                    text_lines.append(line)
            
            # Join all the text
            caption_text = ' '.join(text_lines)
            print(f"🔊 Generating audio from captions: {caption_text[:100]}...")
            
            # Use ElevenLabs for audio generation - save to correct path
            sys.path.append(str(Path(__file__).parent))
            from audio_generator import GreekAudioGenerator
            
            # Create the audio subdirectory if it doesn't exist
            os.makedirs("output/audio", exist_ok=True)
            
            audio_gen = GreekAudioGenerator()
            # Generate audio with just the filename (it saves to output/)
            temp_audio_file = f"audio_{story_num}.mp3"
            result = audio_gen.generate_audio(caption_text, temp_audio_file)
            if result:
                # Move the file from output/ to output/audio/
                temp_path = f"output/{temp_audio_file}"
                if os.path.exists(temp_path):
                    import shutil
                    shutil.move(temp_path, audio_file)
                    print(f"✅ Generated and moved ElevenLabs audio: {audio_file}")
                else:
                    print(f"✅ Generated ElevenLabs audio: {audio_file}")
            else:
                print(f"❌ Failed to generate ElevenLabs audio")
                return False
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            return False

    # Get the actual audio duration and regenerate SRT with correct timing
    try:
        ffprobe_path = "C:/Program Files/ffmpeg-7.1.1-full_build/bin/ffprobe.exe"
        probe_command = [
            ffprobe_path,
            "-i", audio_file,
            "-show_entries", "format=duration",
            "-v", "quiet",
            "-of", "default=noprint_wrappers=1:nokey=1"
        ]
        result = subprocess.run(probe_command, check=True, capture_output=True, text=True)
        audio_duration = float(result.stdout.strip())
        print(f"📏 Audio duration: {audio_duration:.2f} seconds")
        
        # Regenerate SRT file with correct timing
        synced_srt_file = f"output/temp/synced_{srt_file.name}"
        
        # Extract text from original SRT file
        with open(srt_file, 'r', encoding='utf-8') as f:
            srt_content = f.read().strip()
        
        import re
        # Parse SRT and extract text segments
        text_segments = []
        lines = srt_content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if (line and 
                not line.isdigit() and 
                not re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line) and
                line != ''):
                text_segments.append(line)
        
        # Generate new SRT with proper timing
        segment_duration = audio_duration / len(text_segments)
        
        with open(synced_srt_file, 'w', encoding='utf-8', newline='') as f:
            for i, text in enumerate(text_segments):
                start_time = i * segment_duration
                end_time = (i + 1) * segment_duration
                
                # Convert to SRT time format
                start_h = int(start_time // 3600)
                start_m = int((start_time % 3600) // 60)
                start_s = int(start_time % 60)
                start_ms = int((start_time % 1) * 1000)
                
                end_h = int(end_time // 3600)
                end_m = int((end_time % 3600) // 60)
                end_s = int(end_time % 60)
                end_ms = int((end_time % 1) * 1000)
                
                f.write(f"{i + 1}\n")
                f.write(f"{start_h:02d}:{start_m:02d}:{start_s:02d},{start_ms:03d} --> {end_h:02d}:{end_m:02d}:{end_s:02d},{end_ms:03d}\n")
                f.write(f"{text}\n\n")
        
        print(f"✅ Generated synced SRT file: {synced_srt_file}")
        # Use the synced SRT file instead - simple relative path
        srt_file_path = synced_srt_file.replace('\\', '/')
        
    except Exception as e:
        print(f"⚠️ Could not sync timing, using original SRT: {e}")
        srt_file_path = str(srt_file).replace('\\', '/')
    
    # Use the synced SRT file with correct timing
    srt_file_path = synced_srt_file.replace('\\', '/')
    print(f"🎯 Using synced SRT file: {srt_file_path}")

    # Build the filter complex with subtitles - move to lower third
    print(f"🎯 Using SRT file: {srt_file_path}")
    filter_complex = [
        "[0:v]scale=1080:1920[scaled]",
        f"[scaled]subtitles='{srt_file_path}':force_style='FontName=Segoe UI,FontSize=16,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BackColour=&H80000000,Bold=1,Outline=2,Shadow=1,Alignment=2,MarginV=400,MarginL=80,MarginR=80'[v]"
    ]

    # FFmpeg command to combine everything
    ffmpeg_path = "C:/Program Files/ffmpeg-7.1.1-full_build/bin/ffmpeg.exe"
    
    # Convert paths to proper format for FFmpeg
    background_video = background_video.replace('\\', '/')
    audio_file = audio_file.replace('\\', '/')
    output_file = output_file.replace('\\', '/')
    
    command = [
        ffmpeg_path,
        "-i", background_video,
        "-i", audio_file,
        "-vf", f"scale=1080:1920,subtitles='{srt_file_path}':force_style='FontName=Arial,FontSize=16,PrimaryColour=&Hffffff,OutlineColour=&H000000,Bold=1,Outline=2,Alignment=2,MarginV=50'",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y",
        output_file
    ]

    try:
        print("Running FFmpeg command:")
        print(" ".join(command))
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ Created final video: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error: {e}")
        if e.stdout:
            print("FFmpeg stdout output:")
            print(e.stdout)
        if e.stderr:
            print("FFmpeg stderr output:")
            print(e.stderr)
        return False

def main():
    """Create final videos for caption files that have corresponding audio."""
    # Input background video
    background_video = "assets/looped_background_11.mp4"
    
    # Get all caption files
    caption_files = sorted(Path("output/captions").glob("captions_*.srt"))
    if not caption_files:
        print("❌ No caption files found")
        return
    
    # Process story 41
    srt_file = Path("output/captions/captions_41.srt")
    if not srt_file.exists():
        print("❌ captions_41.srt not found")
        return
    # Get all existing final video numbers
    existing_nums = []
    for f in os.listdir("output/final"):
        if f.startswith("final_") and f.endswith(".mp4"):
            parts = f.replace("final_", "").replace(".mp4", "").split("_")
            try:
                existing_nums.append(int(parts[0]))
            except:
                pass
    next_num = max(existing_nums) + 1 if existing_nums else 1
    story_num = srt_file.stem.split('_')[1]
    output_file = f"output/final/final_{next_num}_story_{story_num}.mp4"
    print(f"\n🎬 Processing {srt_file.name}...")
    create_final_video(srt_file, background_video, output_file)

if __name__ == "__main__":
    main() 