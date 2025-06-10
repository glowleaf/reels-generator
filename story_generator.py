import openai
from config import Config
import re

class GreekStoryGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate_story(self, topic="διατροφή και αυτοπεποίθηση", duration=60):
        """Generate a Greek story based on the given topic and duration."""
        
        # Calculate optimal sentence count for 50-60 seconds of narration
        # Each sentence should be 8-10 seconds when spoken in Greek
        optimal_sentences = 12  # 12 sentences x 5 seconds = 60 seconds total
        
        prompt = f"""
        Γράψε μια συναισθηματική ιστορία ακριβώς {duration} δευτερολέπτων για {topic}.

        Δομή και Χρονισμός:
        - Η ιστορία ΠΡΕΠΕΙ να έχει ΑΚΡΙΒΩΣ {optimal_sentences} προτάσεις (ΟΧΙ ΠΕΡΙΣΣΟΤΕΡΕΣ, ΟΧΙ ΛΙΓΟΤΕΡΕΣ)
        - Κάθε πρόταση να είναι 8-12 λέξεις για πλήρη ανάπτυξη
        - Δομή: Εισαγωγή (3 προτάσεις) → Ανάπτυξη (6 προτάσεις) → Κλείσιμο (3 προτάσεις)
        - Η τελευταία πρόταση ΠΡΕΠΕΙ να είναι ολοκληρωμένη και να κλείνει την ιστορία
        - ΚΑΘΕ πρόταση πρέπει να είναι πλήρης και περιεκτική
        - ΚΑΘΕ πρόταση πρέπει να διαρκεί περίπου 5 δευτερόλεπτα όταν διαβάζεται

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
        - ΑΠΑΓΟΡΕΥΕΤΑΙ να κόψεις την ιστορία στη μέση - ΠΡΕΠΕΙ να είναι πλήρης
        - Η ιστορία πρέπει να διαρκεί 50-60 δευτερόλεπτα όταν διαβάζεται δυνατά
        - ΥΠΟΧΡΕΩΤΙΚΑ γράψε ΟΛΕΣ τις {optimal_sentences} προτάσεις - ΜΗΝ σταματήσεις νωρίτερα
        - Κάθε πρόταση πρέπει να τελειώνει με τελεία και να είναι ολοκληρωμένη

        Επέστρεψε μόνο το κείμενο της ιστορίας, χωρίς επιπλέον εξηγήσεις ή σχόλια χρονισμού.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Είσαι ένας ειδικός συγγραφέας ελληνικών ιστοριών για social media. Δημιουργείς πλήρεις, συναισθηματικές ιστορίες 50-60 δευτερολέπτων για βίντεο. Κάθε πρόταση είναι υπολογισμένη να διαβάζεται σε περίπου 5 δευτερόλεπτα. Χρησιμοποιείς πλήρεις, περιεκτικές προτάσεις. Επιστρέφεις μόνο το καθαρό κείμενο της ιστορίας, χωρίς σχόλια. ΠΑΝΤΑ τελειώνεις την ιστορία με την 12η πρόταση και ΠΑΝΤΑ κλείνεις με τελεία. ΑΠΑΓΟΡΕΥΕΤΑΙ να κόψεις την ιστορία στη μέση."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            story = response.choices[0].message.content.strip()
            
            # Clean up any remaining timing annotations or numbering
            story = re.sub(r'\d+\.\s*', '', story)  # Remove numbering
            story = re.sub(r'\(\d+\s*δευτ\.\)', '', story)  # Remove timing
            story = re.sub(r'[""]', '', story)  # Remove quotes
            story = re.sub(r'\s+', ' ', story)  # Fix spacing
            story = story.strip()
            
            # Verify we have complete sentences - if not, regenerate
            sentences = story.split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            if len(sentences) != optimal_sentences:
                print(f"Warning: Story has {len(sentences)} sentences instead of {optimal_sentences}")
                # Try to regenerate with more explicit instructions
                if len(sentences) < optimal_sentences:
                    print("Story too short, attempting regeneration...")
                    return self.generate_story(topic, duration)  # Retry once
            
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