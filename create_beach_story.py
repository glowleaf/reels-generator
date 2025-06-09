from main import GreekVideoCreator

def create_beach_confidence_story():
    creator = GreekVideoCreator()
    
    # Story parameters
    story_prompt = "Μια γυναίκα που πάλευε με την εικόνα του σώματός της στην παραλία, αλλά τελικά βρήκε την αυτοπεποίθησή της"
    background_video = "assets/daphnebeach.mp4"
    duration = 60  # Changed to 60 seconds
    
    # Create the video
    result = creator.create_complete_video(
        topic=story_prompt,
        background_video=background_video,
        duration=duration
    )
    
    if result:
        print(f"\n🎬 Video created successfully: {result['video_path']}")
        print(f"\n📝 Story text:\n{result['story']}")

if __name__ == "__main__":
    create_beach_confidence_story() 