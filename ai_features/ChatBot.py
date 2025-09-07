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

    def get_medical_response(self, user_input):
        """Get response with error handling and retry logic"""
        try:
            model = genai.GenerativeModel(
                model_name=self.selected_model,
                system_instruction=self.create_medical_system_prompt(),
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
                        return self.get_medical_response(user_input)
                else:
                    return "I'm experiencing high demand. Please try again in a minute.", False
                    
            return f"Sorry, I'm having trouble responding. Error: {error_msg}", False

    def medical_chat(self):
        """Main medical chat function"""
        print("=" * 60)
        print("🏥 MEDICAL INFORMATION ASSISTANT")
        print("=" * 60)
        print("💡 I can help with general health information")
        print("⚠️  NOT for diagnoses or emergencies")
        print("📋 Ask about: symptoms, medications, health topics")
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
                
                # Check for emergency keywords
                emergency_keywords = ['emergency', '911', 'urgent', 'dying', 'heart attack', 'stroke']
                if any(keyword in user_input.lower() for keyword in emergency_keywords):
                    print("\n🚨 If this is an emergency, call your local emergency number immediately!")
                    continue

                # Get response with error handling
                response, success = self.get_medical_response(user_input)
                
                if success:
                    print(f"\n🩺 Assistant: {response}")
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