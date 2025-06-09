#!/usr/bin/env python3
"""
Create a 60-second looped background video.
Only needs to be run once.
"""

import os
import subprocess
import sys

def get_next_number():
    """Get the next available number for the background file."""
    i = 1
    while os.path.exists(f"assets/looped_background_{i}.mp4"):
        i += 1
    return i

def create_looped_background():
    """Create a 60-second looped background video with smooth crossfade transitions."""
    # Get next available number
    next_num = get_next_number()
    output_file = f"assets/looped_background_{next_num}.mp4"
    
    # Check if input file exists
    input_file = "assets/daphnebeach.mp4"
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return False

    # FFmpeg command to create looped background
    ffmpeg_path = "C:/Program Files/ffmpeg-7.1.1-full_build/bin/ffmpeg.exe"
    
    # Complex filter to create clean crossfades between loops:
    # 1. Split input into multiple streams
    # 2. Create overlapping segments with xfade transitions
    # 3. Concatenate them together for full duration
    filter_complex = [
        "[0:v]fps=30,split=6[v1][v2][v3][v4][v5][v6]",  # Split into 6 streams
        "[v1][v2]xfade=transition=fade:duration=0.5:offset=9.5[xa]",  # Crossfade 1-2
        "[xa][v3]xfade=transition=fade:duration=0.5:offset=19.5[xb]",  # Crossfade 2-3
        "[xb][v4]xfade=transition=fade:duration=0.5:offset=29.5[xc]",  # Crossfade 3-4
        "[xc][v5]xfade=transition=fade:duration=0.5:offset=39.5[xd]",  # Crossfade 4-5
        "[xd][v6]xfade=transition=fade:duration=0.5:offset=49.5[xf]"   # Crossfade 5-6
    ]
    
    command = [
        ffmpeg_path,
        "-stream_loop", "-1",  # Loop input
        "-i", input_file,
        "-filter_complex", ";".join(filter_complex),
        "-map", "[xf]",
        "-t", "60",  # Exact duration of 60 seconds
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "medium",
        "-movflags", "+faststart",
        "-y",  # Overwrite output file if it exists
        output_file
    ]

    try:
        # Run FFmpeg command with stdout and stderr captured
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print(f"✅ Created 60-second looped background with crossfades: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error: {e}")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)
        return False

if __name__ == "__main__":
    create_looped_background() 