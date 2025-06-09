import requests
import os
from pathlib import Path
from config import Config

class GreekAudioGenerator:
    def __init__(self):
        self.api_key = Config.ELEVENLABS_API_KEY
        self.voice_id = Config.ELEVENLABS_VOICE_ID
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Ensure output directory exists
        Path(Config.OUTPUT_DIR).mkdir(exist_ok=True)
    
    def generate_audio(self, text, filename="audio.mp3", voice_settings=None):
        """Generate Greek audio from text using ElevenLabs API."""
        
        if not self.api_key or not self.voice_id:
            raise ValueError("ElevenLabs API key and Voice ID must be set in .env file")
        
        # Default voice settings optimized for Greek
        if voice_settings is None:
            voice_settings = {
                "stability": 0.4,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
        
        url = f"{self.base_url}/text-to-speech/{self.voice_id}"
        
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": voice_settings
        }
        
        try:
            print(f"Δημιουργία ήχου για κείμενο: {text[:50]}...")
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            output_path = Path(Config.OUTPUT_DIR) / filename
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"Ο ήχος αποθηκεύτηκε στο: {output_path}")
            return str(output_path)
            
        except requests.exceptions.RequestException as e:
            print(f"Σφάλμα στη δημιουργία ήχου: {e}")
            if hasattr(e.response, 'text'):
                print(f"Λεπτομέρειες σφάλματος: {e.response.text}")
            return None
    
    def get_available_voices(self):
        """Get list of available voices from ElevenLabs."""
        
        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            voices = response.json().get("voices", [])
            greek_voices = []
            
            for voice in voices:
                # Look for voices that support Greek or are multilingual
                if any(lang.get("language_id") in ["el", "multilingual"] 
                       for lang in voice.get("fine_tuning", {}).get("language", [])):
                    greek_voices.append({
                        "voice_id": voice["voice_id"],
                        "name": voice["name"],
                        "description": voice.get("description", ""),
                        "category": voice.get("category", "")
                    })
            
            return greek_voices
            
        except requests.exceptions.RequestException as e:
            print(f"Σφάλμα στην ανάκτηση φωνών: {e}")
            return []
    
    def test_voice(self, text="Γεια σας, αυτή είναι μια δοκιμή της ελληνικής φωνής."):
        """Test the current voice with a simple Greek phrase."""
        return self.generate_audio(text, "voice_test.mp3") 