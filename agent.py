import requests

class CyDuckAgent:
    def __init__(self, model="qwen2.5:7b"):
        self.model = model
        self.base_url = "http://localhost:11434/api/generate"
        self.system_prompt = """You are CyDuck, a friendly and helpful AI assistant. 
You're knowledgeable, conversational, and always eager to help users with their questions.
Keep responses concise but informative."""
        
    def generate_response(self, user_message):
        prompt = f"{self.system_prompt}\n\nUser: {user_message}\nCyDuck:"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Oops! CyDuck had a hiccup: {str(e)}"
