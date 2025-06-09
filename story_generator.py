import openai
from config import Config
import re

class GreekStoryGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate_story(self, topic="διατροφή και αυτοπεποίθηση", duration=60):
        """Generate a Greek story based on the given topic and duration."""
        
        # Calculate optimal sentence count for good pacing (about 7-8 seconds per sentence)
        # Fixed to 7 sentences to ensure completion within 60 seconds with buffer
        optimal_sentences = 7  # Fixed number of sentences for better timing control
        
        prompt = f"""
        Γράψε μια συναισθηματική ιστορία ακριβώς {duration} δευτερολέπτων για {topic}.

        Δομή και Χρονισμός:
        - Η ιστορία ΠΡΕΠΕΙ να έχει ΑΚΡΙΒΩΣ {optimal_sentences} προτάσεις (ΟΧΙ ΠΕΡΙΣΣΟΤΕΡΕΣ)
        - Κάθε πρόταση να είναι 6-10 λέξεις για καλό ρυθμό αφήγησης
        - Δομή: Εισαγωγή (2 προτάσεις) → Κύριο μέρος (3 προτάσεις) → Συμπέρασμα (2 προτάσεις)
        - Η τελευταία πρόταση ΠΡΕΠΕΙ να είναι ολοκληρωμένη και να κλείνει την ιστορία
        - ΚΑΘΕ πρόταση πρέπει να είναι σύντομη και περιεκτική
        - ΚΑΘΕ πρόταση πρέπει να διαρκεί περίπου 8-9 δευτερόλεπτα

        Απαιτήσεις Περιεχομένου:
        - Απλή, ρεαλιστική και συναισθηματική ιστορία
        - Καθημερινή ελληνική γλώσσα
        - Κατάλληλη για social media (TikTok/Instagram)
        - Ξεκάθαρο μήνυμα και συναισθηματικό αντίκτυπο
        - Προσωπική αφήγηση σε πρώτο πρόσωπο
        - ΜΗΝ συμπεριλάβεις σχόλια χρονισμού ή αρίθμηση προτάσεων
        - ΟΛΕΣ οι προτάσεις πρέπει να είναι ολοκληρωμένες
        - Χρησιμοποίησε ΜΟΝΟ απλές προτάσεις, όχι σύνθετες
        - Απόφυγε μεγάλες λέξεις και περίπλοκες εκφράσεις
        - ΣΗΜΑΝΤΙΚΟ: Η ιστορία ΠΡΕΠΕΙ να τελειώνει με την {optimal_sentences}η πρόταση
        - ΣΗΜΑΝΤΙΚΟ: Η τελευταία πρόταση ΠΡΕΠΕΙ να είναι ολοκληρωμένη και να κλείνει με τελεία

        Επέστρεψε μόνο το κείμενο της ιστορίας, χωρίς επιπλέον εξηγήσεις ή σχόλια χρονισμού.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Είσαι ένας ειδικός συγγραφέας ελληνικών ιστοριών για social media. Δημιουργείς σύντομες, συναισθηματικές ιστορίες με ακριβή χρονισμό για βίντεο. Κάθε πρόταση είναι υπολογισμένη να διαβάζεται σε περίπου 8-9 δευτερόλεπτα. Χρησιμοποιείς μόνο απλές, σύντομες προτάσεις. Επιστρέφεις μόνο το καθαρό κείμενο της ιστορίας, χωρίς σχόλια. ΠΑΝΤΑ τελειώνεις την ιστορία με την 7η πρόταση και ΠΑΝΤΑ κλείνεις με τελεία."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            story = response.choices[0].message.content.strip()
            
            # Clean up any remaining timing annotations or numbering
            story = re.sub(r'\d+\.\s*', '', story)  # Remove numbering
            story = re.sub(r'\(\d+\s*δευτ\.\)', '', story)  # Remove timing
            story = re.sub(r'[""]', '', story)  # Remove quotes
            story = re.sub(r'\s+', ' ', story)  # Fix spacing
            story = story.strip()
            
            # Verify we have complete sentences
            sentences = story.split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            if len(sentences) != optimal_sentences:
                print(f"Warning: Story has {len(sentences)} sentences instead of {optimal_sentences}")
            
            # Ensure the story ends with a period
            if not story.endswith('.'):
                story += '.'
            
            return story
            
        except Exception as e:
            print(f"Σφάλμα στη δημιουργία ιστορίας: {e}")
            return None
    
    def generate_story_variations(self, topic, count=3):
        """Generate multiple story variations for the same topic."""
        stories = []
        for i in range(count):
            story = self.generate_story(topic)
            if story:
                stories.append(story)
        return stories
    
    def get_story_themes(self):
        """Return a list of popular Greek story themes for social media."""
        return [
            "διατροφή και αυτοπεποίθηση",
            "πρώτη μέρα στη δουλειά",
            "οικογενειακές παραδόσεις",
            "φιλία που άλλαξε τη ζωή μου",
            "ταξίδι που με έμαθε κάτι",
            "παιδικές αναμνήσεις",
            "ξεπέρασμα φόβων",
            "αγάπη και χωρισμός",
            "επιτυχία μετά από αποτυχία",
            "οι μικρές χαρές της ζωής"
        ] 