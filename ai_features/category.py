import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env

class MedicalChatbot:
    def __init__(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        self.available_models = self.get_available_models()
        self.selected_model = self.choose_free_tier_model()
        self.retry_count = 0
        self.max_retries = 2
        
        # Severity categories and routing
        self.severity_levels = {
            "emergency": "🚨 EMERGENCY: Immediate specialist care needed",
            "urgent": "⚠️ URGENT: Specialist consultation recommended",
            "moderate": "🔶 MODERATE: Can consult with specialist when available",
            "mild": "🔷 MILD: Volunteer can provide general advice"
        }
        
        # Comprehensive emergency keywords
        self.emergency_keywords = [
            'emergency', '911', '112', '999', 'urgent', 'dying', 'heart attack', 
            'stroke', 'chest pain', 'bleeding heavily', 'can\'t breathe', 
            'difficulty breathing', 'choking', 'severe pain', 'unconscious',
            'passed out', 'fainted', 'seizure', 'convulsion', 'suicidal',
            'homicidal', 'severe burn', 'broken bone', 'compound fracture',
            'heavy bleeding', 'blood loss', 'poison', 'overdose', 'allergic reaction',
            'anaphylaxis', 'swelling tongue', 'swelling throat', 'paralysis',
            'numbness', 'sudden weakness', 'vision loss', 'sudden blindness',
            'severe headache', 'worst headache', 'electric shock', 'drowning',
            'smoke inhalation', 'carbon monoxide', 'stab wound', 'gunshot',
            'head injury', 'concussion', 'loss of consciousness', 'violent trauma',
            'crush injury', 'amputation', 'severed limb', 'sudden confusion',
            'disorientation', 'slurred speech', 'facial drooping', 'arm weakness',
            'speech difficulty', 'chest pressure', 'jaw pain', 'arm pain',
            'shortness of breath', 'suffocating', 'blue lips', 'blue skin',
            'cyanosis', 'severe abdominal pain', 'rigid abdomen', 'vomiting blood',
            'blood in stool', 'black stool', 'projectile vomiting',
            'high fever with rash', 'meningitis', 'neck stiffness', 'light sensitivity',
            'severe dehydration', 'not urinating', 'sunken eyes', 'rapid heartbeat',
            'palpitations', 'irregular heartbeat', 'cardiac arrest', 'no pulse',
            'not breathing', 'self harm', 'cutting', 'attempted suicide'
        ]
        
        # Specialist database with contact information
        self.specialists = {
            "Cardiologist": {
                "contact": "Cardiology Department: 555-1001\nDr. Smith: 555-1002",
                "conditions": ["heart", "chest pain", "palpitations", "blood pressure"]
            },
            "Neurologist": {
                "contact": "Neurology Department: 555-2001\nDr. Johnson: 555-2002",
                "conditions": ["headache", "migraine", "seizure", "stroke", "numbness"]
            },
            "Gastroenterologist": {
                "contact": "Gastroenterology Department: 555-3001\nDr. Williams: 555-3002",
                "conditions": ["stomach", "abdominal", "digestive", "vomiting", "diarrhea"]
            },
            "Dermatologist": {
                "contact": "Dermatology Department: 555-4001\nDr. Brown: 555-4002",
                "conditions": ["rash", "skin", "acne", "eczema", "psoriasis"]
            },
            "Orthopedist": {
                "contact": "Orthopedics Department: 555-5001\nDr. Davis: 555-5002",
                "conditions": ["bone", "fracture", "joint", "sprain", "arthritis"]
            },
            "Pediatrician": {
                "contact": "Pediatrics Department: 555-6001\nDr. Miller: 555-6002",
                "conditions": ["child", "baby", "infant", "pediatric", "kids"]
            },
            "Gynecologist": {
                "contact": "Gynecology Department: 555-7001\nDr. Wilson: 555-7002",
                "conditions": ["women", "gynecological", "menstrual", "pregnancy"]
            },
            "General Practitioner": {
                "contact": "Primary Care: 555-8001\nDr. Anderson: 555-8002",
                "conditions": ["general", "fever", "cold", "flu", "checkup"]
            },
            "Internist": {
                "contact": "Internal Medicine: 555-9001\nDr. Taylor: 555-9002",
                "conditions": ["internal", "adult medicine", "chronic conditions"]
            },
            "Psychiatrist": {
                "contact": "Psychiatry Department: 555-0101\nDr. Martin: 555-0102",
                "conditions": ["mental", "depression", "anxiety", "suicidal", "emotional"]
            },
            "Emergency Department": {
                "contact": "🚨 EMERGENCY: 911 or your local emergency number\nHospital ER: 555-0001",
                "conditions": ["emergency", "life-threatening", "critical", "urgent"]
            }
        }
        
        # Volunteer contacts for mild conditions
        self.volunteer_contacts = {
            "General Health Volunteers": "Health Helpline: 555-HELP\nVolunteer Coordinator: 555-VOLUNTEER",
            "Mental Health Support": "Crisis Text Line: Text HOME to 741741\nMental Health Volunteers: 555-MHSUPPORT"
        }

    def get_available_models(self):
        """Get all available models that support content generation"""
        try:
            models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    models.append({
                        'name': model.name,
                        'description': getattr(model, 'description', 'No description'),
                        'supported_methods': model.supported_generation_methods
                    })
            return models
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []

    def choose_free_tier_model(self):
        """Select a model that's likely to be in free tier"""
        # Free tier models (avoid pro/preview models that have quotas)
        free_tier_models = [
            'gemini-1.0-pro',
            'gemini-pro',
            'gemini-1.5-flash',
            'gemini-1.5-flash-8b',
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-1.5-flash-latest'
        ]
        
        available_model_names = [model['name'] for model in self.available_models]
        
        # Try to find a free tier model
        for free_model in free_tier_models:
            for available_model in available_model_names:
                if free_model in available_model:
                    print(f"✅ Selected free-tier model: {available_model}")
                    return available_model
        
        # Fallback to any available model
        if self.available_models:
            fallback = self.available_models[0]['name']
            print(f"⚠️  Using available model: {fallback}")
            return fallback
        
        raise Exception("No suitable models available")

    def switch_to_free_model(self):
        """Switch to a free tier model after rate limit error"""
        free_models = ['gemini-1.0-pro', 'gemini-pro', 'gemini-1.5-flash', 'gemini-2.0-flash']
        
        for model in self.available_models:
            for free_model in free_models:
                if free_model in model['name'] and model['name'] != self.selected_model:
                    self.selected_model = model['name']
                    print(f"🔄 Switched to free model: {self.selected_model}")
                    return True
        return False

    def create_medical_system_prompt(self):
        """Create a comprehensive medical system prompt"""
        return """You are a medical information assistant providing general health education.
        
        Provide: General health info, symptom explanations, medication overviews, lifestyle advice
        Avoid: Diagnoses, prescriptions, emergency advice, treatment recommendations
        
        Always include: "Consult healthcare professionals for personal medical advice."
        """

    def assess_severity(self, user_input):
        """Assess the severity of the medical condition described"""
        severity_prompt = f"""
        Analyze this medical query and categorize its severity level:
        "{user_input}"
        
        Respond ONLY with one of these exact severity levels:
        - emergency: Life-threatening conditions (heart attack, stroke, severe bleeding, difficulty breathing, etc.)
        - urgent: Requires prompt medical attention but not immediately life-threatening (high fever, severe pain, etc.)
        - moderate: Concerning symptoms that should be evaluated but not urgent (persistent cough, mild pain, etc.)
        - mild: Minor issues that can be addressed with general advice (common cold, minor cuts, etc.)
        
        Your response should be only one word: emergency, urgent, moderate, or mild.
        """
        
        try:
            model = genai.GenerativeModel(
                model_name=self.selected_model,
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 10,
                }
            )
            
            response = model.generate_content(severity_prompt)
            severity = response.text.strip().lower()
            
            # Validate the response
            if severity not in ["emergency", "urgent", "moderate", "mild"]:
                # Default to moderate if the response is unclear
                severity = "moderate"
                
            return severity
            
        except Exception as e:
            print(f"Error assessing severity: {e}")
            # Default to moderate in case of error
            return "moderate"

    def get_specialist_type(self, user_input, severity):
        """Determine which specialist would be most appropriate"""
        if severity == "emergency":
            return "Emergency Department"
            
        # Check for specific conditions that match specialist expertise
        user_input_lower = user_input.lower()
        
        for specialist, info in self.specialists.items():
            for condition in info["conditions"]:
                if condition in user_input_lower and specialist != "Emergency Department":
                    return specialist
        
        # Default to General Practitioner if no specific match
        return "General Practitioner"

    def get_contact_info(self, specialist_type, severity):
        """Get contact information for the appropriate specialist or volunteer"""
        if severity in ["emergency", "urgent"]:
            if specialist_type in self.specialists:
                return self.specialists[specialist_type]["contact"]
            else:
                return self.specialists["Emergency Department"]["contact"]
        elif severity == "moderate":
            if specialist_type in self.specialists:
                return self.specialists[specialist_type]["contact"]
            else:
                return self.specialists["General Practitioner"]["contact"]
        else:  # mild
            # Return volunteer contact information
            return "\n".join([f"{service}: {contact}" for service, contact in self.volunteer_contacts.items()])

    def get_medical_response(self, user_input, severity):
        """Get response with error handling and retry logic"""
        try:
            # Add severity context to the system prompt
            enhanced_prompt = self.create_medical_system_prompt() + f"""
            Note: This query has been assessed as {severity} severity.
            """
            
            model = genai.GenerativeModel(
                model_name=self.selected_model,
                system_instruction=enhanced_prompt,
                generation_config={
                    "temperature": 0.2,
                    "max_output_tokens": 1024,
                }
            )
            
            chat_session = model.start_chat()
            response = chat_session.send_message(user_input)
            return response.text, True
            
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's a rate limit error
            if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                print(f"⏳ Rate limit hit. Retrying in 5 seconds...")
                time.sleep(5)
                
                if self.retry_count < self.max_retries:
                    self.retry_count += 1
                    # Try switching to free model
                    if self.switch_to_free_model():
                        return self.get_medical_response(user_input, severity)
                else:
                    return "I'm experiencing high demand. Please try again in a minute.", False
                    
            return f"Sorry, I'm having trouble responding. Error: {error_msg}", False

    def medical_chat(self):
        """Main medical chat function"""
        print("=" * 60)
        print("🏥 MEDICAL TRIAGE ASSISTANT")
        print("=" * 60)
        print("💡 I can help assess your medical concerns")
        print("⚠️  NOT for diagnoses or emergencies")
        print("📋 I'll direct you to appropriate care based on severity")
        print("Type 'exit' to quit, 'model' to switch models")
        print("=" * 60)

        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\nThank you! Stay healthy! 🌟")
                    break
                    
                elif user_input.lower() == 'model':
                    self.show_available_models()
                    new_model = input("Enter model name to switch: ").strip()
                    if new_model:
                        self.selected_model = new_model
                        print(f"✅ Switched to: {self.selected_model}")
                    continue
                
                # Check for emergency keywords - immediate response
                if any(keyword in user_input.lower() for keyword in self.emergency_keywords):
                    print("\n🚨 EMERGENCY DETECTED: Please call your local emergency number immediately!")
                    print("💡 You should go to the Emergency Department right away")
                    print(f"📞 {self.specialists['Emergency Department']['contact']}")
                    continue

                # Assess severity of the condition
                print("🔍 Assessing your condition...")
                severity = self.assess_severity(user_input)
                print(f"\n{self.severity_levels[severity]}")
                
                # Determine appropriate specialist
                specialist = self.get_specialist_type(user_input, severity)
                contact_info = self.get_contact_info(specialist, severity)
                
                # Route to appropriate care based on severity
                if severity == "emergency":
                    print("🚨 Please go to the Emergency Department or call emergency services immediately!")
                    print(f"📞 {contact_info}")
                elif severity == "urgent":
                    print(f"📞 Please contact a {specialist} as soon as possible:")
                    print(f"   {contact_info}")
                elif severity == "moderate":
                    print(f"📅 Consider scheduling an appointment with a {specialist}:")
                    print(f"   {contact_info}")
                else:  # mild
                    print("💬 A volunteer can help with general advice:")
                    print(f"   {contact_info}")
                
                # Get medical response
                response, success = self.get_medical_response(user_input, severity)
                
                if success:
                    print(f"\n🩺 Medical Information: {response}")
                else:
                    print(f"\n❌ {response}")
                    
                # Reset retry count after successful response
                if success:
                    self.retry_count = 0
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")

    def show_available_models(self):
        """Display available models"""
        print(f"\n📊 Available Models:")
        print("-" * 50)
        for model in self.available_models:
            status = "✅ CURRENT" if model['name'] == self.selected_model else "  Available"
            print(f"{status} - {model['name']}")
        print("-" * 50)
        print("💡 Tip: Use simpler models like 'gemini-pro' or 'gemini-1.5-flash' to avoid rate limits")

# Run the medical chatbot
if __name__ == "__main__":
    try:
        chatbot = MedicalChatbot()
        chatbot.medical_chat()
    except Exception as e:
        print(f"Failed to initialize: {e}")