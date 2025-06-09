# 🇬🇷 Greek Social Story Video Generator

Automated tool for creating engaging Greek-captioned story videos for social media platforms like TikTok, Instagram Reels, and YouTube Shorts.

## ✨ Features

- **AI Story Generation**: Uses GPT-4 to create authentic Greek stories
- **Greek Text-to-Speech**: ElevenLabs integration for natural Greek narration
- **Automatic Captions**: SRT subtitle generation with proper Greek text timing
- **Video Processing**: FFmpeg integration for professional video output
- **Interactive Interface**: Easy-to-use command-line interface
- **Customizable**: Multiple story themes and duration options

## 🛠️ Prerequisites

### Required Software
1. **Python 3.8+**
2. **FFmpeg** - [Download here](https://ffmpeg.org/download.html)

### API Keys Required
1. **OpenAI API Key** - [Get here](https://platform.openai.com/api-keys)
2. **ElevenLabs API Key** - [Get here](https://elevenlabs.io/api)
3. **ElevenLabs Greek Voice ID** - Find a Greek voice in your ElevenLabs dashboard

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys
# Add your OpenAI API key
# Add your ElevenLabs API key
# Add your preferred Greek voice ID
```

### 3. Run the Generator
```bash
# Interactive mode (recommended for first use)
python main.py --interactive

# Quick demo with default settings
python main.py --quick

# Create video with custom topic
python main.py "ιστορία αγάπης και χωρισμού"
```

## 📁 Project Structure

```
reels-generator/
├── main.py                 # Main application entry point
├── config.py              # Configuration and settings
├── story_generator.py     # GPT-4 story generation
├── audio_generator.py     # ElevenLabs audio generation
├── caption_generator.py   # SRT caption creation
├── video_processor.py     # FFmpeg video processing
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── output/               # Generated videos and assets
├── assets/               # Background videos and images
└── fonts/                # Greek-compatible fonts
```

## 🎯 Available Story Themes

1. Διατροφή και αυτοπεποίθηση
2. Πρώτη μέρα στη δουλειά
3. Οικογενειακές παραδόσεις
4. Φιλία που άλλαξε τη ζωή μου
5. Ταξίδι που με έμαθε κάτι
6. Παιδικές αναμνήσεις
7. Ξεπέρασμα φόβων
8. Αγάπη και χωρισμός
9. Επιτυχία μετά από αποτυχία
10. Οι μικρές χαρές της ζωής

## 🎬 How It Works

1. **Story Generation**: GPT-4 creates an authentic Greek story based on your chosen theme
2. **Audio Creation**: ElevenLabs converts the story to natural Greek speech
3. **Caption Generation**: Automatic timing and SRT file creation for Greek subtitles
4. **Video Processing**: FFmpeg combines background video, audio, and captions
5. **Output**: Ready-to-use MP4 video for social media

## ⚙️ Advanced Configuration

### Custom Background Videos
Place your background videos in the `assets/` folder and specify the path when prompted.

### Greek Fonts
For best caption rendering, place Greek-compatible fonts (like DejaVu Sans) in the `fonts/` folder.

### Voice Settings
Modify voice settings in `audio_generator.py`:
```python
voice_settings = {
    "stability": 0.4,        # Voice consistency
    "similarity_boost": 0.75, # Voice similarity
    "style": 0.0,            # Style exaggeration
    "use_speaker_boost": True # Speaker boost
}
```

## 🐛 Troubleshooting

### FFmpeg Not Found
```bash
# Windows (using Chocolatey)
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

### Greek Characters Not Displaying
- Ensure you have Greek-compatible fonts installed
- Check that your terminal supports UTF-8 encoding

### API Errors
- Verify your API keys in the `.env` file
- Check your ElevenLabs credit balance
- Ensure your OpenAI API key has GPT-4 access

### Audio Generation Issues
- Test your ElevenLabs voice ID with the test function
- Try different voice settings for better Greek pronunciation

## 📊 Example Output

The generator creates:
- `story_audio.mp3` - Greek narration
- `story_captions.srt` - Timed Greek subtitles
- `background.mp4` - Generated background (if none provided)
- `greek_story_[topic].mp4` - Final video ready for social media

## 🔧 Customization

### Adding New Story Themes
Edit the `get_story_themes()` method in `story_generator.py`.

### Changing Video Format
Modify the FFmpeg parameters in `video_processor.py` for different resolutions or formats.

### Caption Styling
Adjust caption appearance in `config.py`:
```python
CAPTION_FONT_SIZE = 24
CAPTION_FONT_COLOR = "white"
CAPTION_OUTLINE_COLOR = "black"
CAPTION_OUTLINE_WIDTH = 2
```

## 📱 Social Media Optimization

The generated videos are optimized for:
- **Instagram Reels**: 1080x1920 vertical format
- **TikTok**: Portrait orientation with engaging captions
- **YouTube Shorts**: High-quality encoding

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT-4 story generation
- ElevenLabs for Greek text-to-speech
- FFmpeg for video processing
- The Greek community for authentic story inspiration

## Important Notes

### ⚠️ DO NOT USE LIBASS
- NEVER use libass for subtitle rendering - it has been tried and does not work for this project
- Stick to FFmpeg's built-in subtitle filters

## Project Structure

- `assets/` - Background videos
- `output/`
  - `captions/` - SRT caption files
  - `stories/` - Text files for audio generation
  - `audio/` - Generated MP3 files
  - `final/` - Output directory for final videos

## Video Specifications

- Resolution: 1080x1920 (9:16 aspect ratio)
- Subtitle styling:
  - Font: Segoe UI
  - Size: 60
  - Colors: White text, black outline
  - Semi-transparent background

---

**Happy creating! 🎬🇬🇷** 