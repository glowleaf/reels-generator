# 📖 Usage Examples - Greek Video Generator

## 🏃‍♂️ Quick Examples

### Example 1: Default Story (Easiest)
```bash
python main.py --quick
```
Creates a 30-second video about "διατροφή και αυτοπεποίθηση" with default settings.

### Example 2: Interactive Mode (Recommended)
```bash
python main.py --interactive
```
Guides you through:
- Choosing from 10 predefined Greek story themes
- Setting custom duration
- Adding background video (optional)

### Example 3: Custom Topic
```bash
python main.py "ιστορία αγάπης και χωρισμού"
```
Creates video about a custom topic: "love and breakup story"

## 🎨 Creative Examples

### Fitness Journey Story
```bash
python main.py "η διαδρομία μου στο γυμναστήριο"
```

### Family Tradition Story  
```bash
python main.py "οικογενειακές παραδόσεις των Χριστουγέννων"
```

### Career Change Story
```bash
python main.py "όταν άλλαξα καριέρα στα 35"
```

### Friendship Story
```bash
python main.py "η φιλία που με έσωσε"
```

## 🔧 Advanced Usage

### Custom Duration
```python
from main import GreekVideoCreator

creator = GreekVideoCreator()
result = creator.create_complete_video(
    topic="ταξίδι στα νησιά",
    duration=45  # 45 seconds
)
```

### With Background Video
```python
creator = GreekVideoCreator()
result = creator.create_complete_video(
    topic="ιστορία επιτυχίας",
    background_video="assets/my_background.mp4",
    duration=30
)
```

### Multiple Stories
```python
from story_generator import GreekStoryGenerator

generator = GreekStoryGenerator()
stories = generator.generate_story_variations(
    "παιδικές αναμνήσεις", 
    count=3
)

for i, story in enumerate(stories):
    print(f"Story {i+1}: {story}")
```

## 📁 File Structure After Creation

After running the generator, you'll have:

```
output/
├── story_audio.mp3           # Greek narration
├── story_captions.srt        # Timed subtitles
├── background.mp4            # Background video (if generated)
└── greek_story_[topic].mp4   # Final social media ready video
```

## 🎬 Social Media Best Practices

### For TikTok
- Use trending topics: "διατροφή", "fitness", "σχέσεις"
- Keep videos 15-30 seconds
- Ensure captions are large and readable

### For Instagram Reels
- Use emotional stories: "αυτοπεποίθηση", "οικογένεια", "φιλία"
- 30 seconds is ideal
- Vertical format (already optimized)

### For YouTube Shorts
- Can go up to 60 seconds
- Use educational or inspirational themes

## 🌟 Pro Tips

1. **Test Your Voice**: Use the demo to test ElevenLabs voice quality
```bash
python demo.py
```

2. **Batch Create**: Create multiple videos for content planning
```python
topics = ["διατροφή", "γυμναστική", "σχέσεις", "καριέρα"]
for topic in topics:
    creator.create_complete_video(topic=topic)
```

3. **Custom Backgrounds**: Place your video files in `assets/` folder and reference them

4. **Font Optimization**: Add Greek fonts to `fonts/` folder for better caption rendering

## 🔄 Workflow for Content Creators

1. **Morning**: Generate 5-10 stories with different themes
2. **Afternoon**: Review and select best stories
3. **Evening**: Create videos and upload to social media

```bash
# Generate stories for the week
python main.py "fitness motivation"
python main.py "family memories"  
python main.py "career success"
python main.py "friendship story"
python main.py "travel adventure"
```

## 🎯 Target Audience Examples

### Fitness Content
```bash
python main.py "η πρώτη μου μέρα στο γυμναστήριο"
python main.py "πώς έχασα 10 κιλά"
python main.py "η αλλαγή που με έκανε δυνατή"
```

### Lifestyle Content
```bash
python main.py "η πρώτη μου μέρα ως freelancer"
python main.py "πώς οργανώνω τη μέρα μου"
python main.py "οι μικρές χαρές της καθημερινότητας"
```

### Emotional Content
```bash
python main.py "όταν ένιωσα μόνη"
python main.py "η στιγμή που κατάλαβα τι θέλω"
python main.py "πώς ξεπέρασα το φόβο μου"
```

---

**Start creating your Greek social media empire! 🇬🇷👑** 