import os
import subprocess
from pathlib import Path
import ffmpeg

class VideoProcessor:
    def __init__(self, font_path=None):
        self.font_path = font_path or "C:/Windows/Fonts/DejaVuSans.ttf"
        self.ffmpeg_path = "C:/Program Files/ffmpeg-7.1.1-full_build/bin/ffmpeg.exe"
        self.ffprobe_path = "C:/Program Files/ffmpeg-7.1.1-full_build/bin/ffprobe.exe"
        self._verify_ffmpeg()
    
    def _verify_ffmpeg(self):
        """Verify FFmpeg is available"""
        try:
            subprocess.run([self.ffmpeg_path, '-version'], capture_output=True)
            print("✅ FFmpeg is available")
            # Configure ffmpeg-python to use this path
            ffmpeg._run.DEFAULT_FFMPEG_PATH = self.ffmpeg_path
            ffmpeg._probe.DEFAULT_FFPROBE_PATH = self.ffprobe_path
        except Exception as e:
            raise RuntimeError(f"FFmpeg is not available at {self.ffmpeg_path}. Please install FFmpeg first.") from e
    
    def prepare_background_video(self, input_video, target_duration, output_path):
        """Create a looped background video of the target duration"""
        try:
            # Get video duration
            probe = ffmpeg.probe(input_video)
            duration = float(probe['streams'][0]['duration'])
            
            # Calculate number of loops needed
            loops_needed = int(target_duration / duration) + 1
            
            # Create filter complex for seamless looping
            stream = ffmpeg.input(input_video)
            stream = ffmpeg.filter(stream, 'loop', loop=-1)  # Loop infinitely
            stream = ffmpeg.trim(stream, duration=target_duration)  # Trim to exact duration
            stream = ffmpeg.setpts(stream, 'PTS-STARTPTS')  # Reset timestamps
            
            # Save the looped video
            stream = ffmpeg.output(
                stream, 
                str(output_path),
                vcodec='libx264',
                preset='medium',
                crf=23,
                video_bitrate='2500k'
            )
            
            print(f"🔄 Creating looped video of {target_duration} seconds...")
            ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
            print(f"✅ Video looped successfully: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error creating looped background: {e}")
            return None
    
    def create_final_video(self, background_video, audio_file, captions_file, output_file):
        """Create the final video with audio and captions"""
        try:
            print(f"🎬 Creating video: {Path(output_file).name}")
            print("This may take a few minutes...")
            
            # Prepare filter complex for adding captions
            filter_complex = [
                f"subtitles='{captions_file}':force_style='FontName={self.font_path},FontSize=20,PrimaryColour=white,OutlineColour=black,Outline=2'"
            ]
            
            # Create the final video with audio and captions
            stream = ffmpeg.input(background_video)
            audio = ffmpeg.input(audio_file)
            
            # Apply filters and combine with audio
            stream = ffmpeg.filter(stream, 'fps', fps=30)
            stream = ffmpeg.filter(stream, 'scale', 1080, 1920)  # Portrait mode for social media
            stream = ffmpeg.filter_complex(stream, filter_complex)
            
            # Output the final video
            stream = ffmpeg.output(
                stream,
                audio,
                str(output_file),
                acodec='aac',
                vcodec='libx264',
                preset='medium',
                crf=23,
                video_bitrate='2500k',
                audio_bitrate='192k'
            )
            
            ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
            return str(output_file)
            
        except Exception as e:
            print(f"❌ Error creating final video: {e}")
            return None

    def _check_ffmpeg(self):
        """Check if ffmpeg is installed and accessible."""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, check=True)
            print("✅ FFmpeg is available")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ FFmpeg not found. Please install ffmpeg first.")
            print("Download from: https://ffmpeg.org/download.html")
            return False
    
    def _get_video_duration(self, video_path):
        """Get the duration of a video file in seconds."""
        try:
            cmd = [
                'ffmpeg',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except (subprocess.CalledProcessError, ValueError) as e:
            print(f"⚠️ Could not get video duration: {e}")
            return None

    def _loop_video(self, input_video, required_duration, output_path):
        """Loop a video to reach the required duration."""
        video_duration = self._get_video_duration(input_video)
        if video_duration is None:
            return None

        # Calculate how many times we need to loop the video
        loop_count = int(required_duration / video_duration) + 1
        
        # Create a complex filter to loop the video
        filter_complex = f"[0:v]loop={loop_count}:1:0[v];[v]trim=0:{required_duration}[v_trim];[v_trim]setpts=PTS-STARTPTS[v_out]"
        
        cmd = [
            'ffmpeg',
            '-i', input_video,
            '-filter_complex', filter_complex,
            '-map', '[v_out]',
            '-t', str(required_duration),
            '-y',
            str(output_path)
        ]
        
        try:
            print(f"🔄 Looping video to reach {required_duration} seconds...")
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✅ Video looped successfully: {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error looping video: {e}")
            print(f"Stderr: {e.stderr}")
            return None
    
    def create_video_with_captions(self, 
                                 background_video, 
                                 audio_file, 
                                 caption_file, 
                                 output_filename="final_video.mp4",
                                 font_path=None):
        """Create final video with Greek captions overlay."""
        
        output_path = Path(Config.OUTPUT_DIR) / output_filename
        
        # Get audio duration
        audio_duration = self._get_video_duration(audio_file)
        if audio_duration is None:
            return None
        
        # Get background video duration
        bg_duration = self._get_video_duration(background_video)
        if bg_duration is None:
            return None

        # Always use the audio duration as the required duration
        required_duration = audio_duration
        
        if bg_duration < required_duration:
            print(f"🔄 Background video ({bg_duration:.2f}s) is shorter than required duration ({required_duration:.2f}s). Looping...")
            looped_bg = Path(Config.OUTPUT_DIR) / "temp_looped_bg.mp4"
            background_video = self._loop_video(background_video, required_duration, looped_bg)
            if not background_video:
                return None
        
        # Default Greek font path
        if font_path is None:
            font_path = self._get_greek_font_path()
        
        # Build ffmpeg command
        cmd = [
            'ffmpeg',
            '-i', background_video,  # Background video
            '-i', audio_file,        # Greek audio
            '-vf', self._build_subtitle_filter(caption_file, font_path),
            '-c:a', 'aac',           # Audio codec
            '-c:v', 'libx264',       # Video codec
            '-preset', 'medium',     # Encoding preset
            '-crf', '23',            # Quality setting
            '-t', str(required_duration),  # Force output duration to match audio
            '-y',                    # Overwrite output
            str(output_path)
        ]
        
        try:
            print(f"🎬 Δημιουργία βίντεο: {output_filename}")
            print("Αυτό μπορεί να πάρει λίγα λεπτά...")
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Clean up temporary looped video if it exists
            if bg_duration < required_duration:
                try:
                    os.remove(str(looped_bg))
                except OSError:
                    pass
            
            print(f"✅ Το βίντεο δημιουργήθηκε επιτυχώς: {output_path}")
            return str(output_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Σφάλμα στη δημιουργία βίντεο: {e}")
            print(f"Stderr: {e.stderr}")
            return None
    
    def _build_subtitle_filter(self, caption_file, font_path):
        """Build the subtitle filter for ffmpeg with Greek font support."""
        
        # Escape the caption file path for ffmpeg
        escaped_caption_file = caption_file.replace('\\', '\\\\').replace(':', '\\:')
        
        subtitle_filter = f"subtitles='{escaped_caption_file}'"
        
        if font_path and os.path.exists(font_path):
            escaped_font_path = font_path.replace('\\', '\\\\')
            subtitle_filter += f":force_style='FontName=DejaVu Sans,FontSize={Config.CAPTION_FONT_SIZE},PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline={Config.CAPTION_OUTLINE_WIDTH}'"
        
        return subtitle_filter
    
    def _get_greek_font_path(self):
        """Try to find a Greek-compatible font on the system."""
        
        # Common Greek font locations
        possible_fonts = [
            # Windows
            "C:/Windows/Fonts/DejaVuSans.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            # Local fonts directory
            str(Path(Config.FONTS_DIR) / "DejaVuSans.ttf"),
            str(Path(Config.FONTS_DIR) / "greek_font.ttf"),
            # Linux/Mac (if running in WSL or cross-platform)
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]
        
        for font_path in possible_fonts:
            if os.path.exists(font_path):
                print(f"📝 Χρήση γραμματοσειράς: {font_path}")
                return font_path
        
        print("⚠️  Δεν βρέθηκε ελληνική γραμματοσειρά. Χρήση προεπιλογής.")
        return None
    
    def create_background_video(self, color="black", duration=30, output_filename="background.mp4"):
        """Create a simple colored background video."""
        
        output_path = Path(Config.OUTPUT_DIR) / output_filename
        
        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', f'color={color}:size=1080x1920:duration={duration}:rate=30',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-y',
            str(output_path)
        ]
        
        try:
            print(f"🎨 Δημιουργία φόντου βίντεο: {output_filename}")
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✅ Φόντο βίντεο δημιουργήθηκε: {output_path}")
            return str(output_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Σφάλμα στη δημιουργία φόντου: {e}")
            return None
    
    def get_video_info(self, video_path):
        """Get information about a video file."""
        
        cmd = [
            'ffmpeg',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            import json
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            print(f"Σφάλμα στην ανάλυση βίντεο: {e}")
            return None
    
    def extract_audio_from_video(self, video_path, output_filename="extracted_audio.mp3"):
        """Extract audio from a video file."""
        
        output_path = Path(Config.OUTPUT_DIR) / output_filename
        
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vn',  # No video
            '-acodec', 'mp3',
            '-y',
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"🎵 Ήχος εξάχθηκε: {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            print(f"Σφάλμα στην εξαγωγή ήχου: {e}")
            return None 