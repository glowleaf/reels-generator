import re
import pysrt
from pathlib import Path
from config import Config

class GreekCaptionGenerator:
    def __init__(self):
        # Ensure output directory exists
        Path(Config.OUTPUT_DIR).mkdir(exist_ok=True)
    
    def create_captions(self, text, duration, output_filename="captions.srt"):
        """Create SRT captions from text with proper timing."""
        
        # Use the provided output filename directly
        output_path = Path(output_filename)
        
        # Split text into sentences using more sophisticated splitting
        sentences = self._split_into_sentences(text)
        
        # Calculate time per sentence, ensuring even distribution
        total_sentences = len(sentences)
        time_per_sentence = duration / total_sentences if total_sentences > 0 else duration
        
        # Add a small gap between sentences
        gap = 0.5  # half second gap
        effective_time = time_per_sentence - gap
        
        # Create subtitle file
        subs = pysrt.SubRipFile()
        
        for i, sentence in enumerate(sentences):
            if sentence:
                # Calculate timing with gap
                start_time = i * time_per_sentence
                end_time = start_time + effective_time
                
                # Create subtitle
                sub = pysrt.SubRipItem(
                    index=i+1,
                    start=self._seconds_to_srt_time(start_time),
                    end=self._seconds_to_srt_time(end_time),
                    text=sentence.strip()
                )
                subs.append(sub)
        
        # Create parent directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to file
        subs.save(str(output_path), encoding='utf-8')
        print(f"Υπότιτλοι αποθηκεύτηκαν στο: {output_path}")
        
        # Preview the captions
        self.preview_captions(str(output_path))
        
        return str(output_path)
    
    def _split_into_sentences(self, text):
        """Split Greek text into appropriately sized sentences for captions."""
        
        # First split by natural sentence endings
        sentences = re.split(r'[.!;·]', text)
        
        # Clean and filter empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Further split long sentences by commas or conjunctions
        final_sentences = []
        for sentence in sentences:
            if len(sentence) > 80:  # Too long for one caption
                # Try to split by comma or common Greek conjunctions
                parts = re.split(r'[,]|(?:\s+(?:και|αλλά|όμως|μα|κι|ή)\s+)', sentence)
                for part in parts:
                    if part.strip():
                        final_sentences.append(part.strip())
            else:
                final_sentences.append(sentence)
        
        return final_sentences
    
    def _seconds_to_srt_time(self, seconds):
        """Convert seconds to SRT time format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return pysrt.SubRipTime(hours, minutes, secs, milliseconds)
    
    def create_manual_captions(self, caption_data, filename="manual_captions.srt"):
        """Create captions from manual timing data.
        
        caption_data should be a list of tuples: [(start_time, end_time, text), ...]
        """
        
        subs = pysrt.SubRipFile()
        
        for i, (start_time, end_time, text) in enumerate(caption_data):
            start_srt = self._seconds_to_srt_time(start_time)
            end_srt = self._seconds_to_srt_time(end_time)
            
            sub_item = pysrt.SubRipItem(
                index=i + 1,
                start=start_srt,
                end=end_srt,
                text=text.strip()
            )
            
            subs.append(sub_item)
        
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        subs.save(str(output_path), encoding='utf-8')
        
        print(f"Χειροκίνητοι υπότιτλοι αποθηκεύτηκαν στο: {output_path}")
        return str(output_path)
    
    def preview_captions(self, srt_file):
        """Preview the generated captions with timing."""
        print("\n📝 Προεπισκόπηση Υποτίτλων:")
        print("-" * 50)
        
        subs = pysrt.open(srt_file)
        for sub in subs:
            print(f"{sub.index}: {sub.start} --> {sub.end}")
            print(f"   {sub.text}\n") 