import requests
from datetime import datetime
import json
import os
from pathlib import Path

class CyDuckAgent:
    def __init__(self):
        self.model_url = "http://localhost:11434/api/generate"
        self.model_name = "qwen2.5:7b"
        
        # Create memory storage directory
        self.memory_dir = Path("cyduck_memory")
        self.memory_dir.mkdir(exist_ok=True)
        
        # Chat history file
        self.history_file = self.memory_dir / "chat_history.json"
        self.load_history()
    
    def load_history(self):
        """Load chat history from file"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.chat_history = json.load(f)
        else:
            self.chat_history = []
    
    def save_history(self):
        """Save chat history to file"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
    
    def get_recent_context(self, limit=5):
        """Get recent conversation context"""
        recent = self.chat_history[-limit:] if len(self.chat_history) > 0 else []
        context = ""
        for msg in recent:
            context += f"User: {msg['user']}\nCyDuck: {msg['assistant']}\n\n"
        return context
    
    def generate_response(self, user_message, user_id="default"):
        """Generate AI response with conversation memory"""
        try:
            # Get conversation context
            context = self.get_recent_context(limit=3)
            
            # Build prompt with context
            system_prompt = """You are CyDuck 🦆, a helpful AI assistant built by Madhur Tyagi. 
You are friendly, knowledgeable, and remember past conversations.
Keep responses concise and helpful."""
            
            prompt = f"{system_prompt}\n\nRecent conversation:\n{context}\nUser: {user_message}\nCyDuck:"
            
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            }
            
            response = requests.post(self.model_url, json=payload, timeout=60)
            
            if response.status_code == 200:
                ai_response = response.json()['response'].strip()
                
                # Save to history
                self.chat_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user_id": user_id,
                    "user": user_message,
                    "assistant": ai_response
                })
                
                # Keep only last 100 messages
                if len(self.chat_history) > 100:
                    self.chat_history = self.chat_history[-100:]
                
                self.save_history()
                
                return ai_response
            else:
                return f"Error: Ollama returned status {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return "Oops! CyDuck can't connect to Ollama. Make sure it's running (ollama serve)"
        except Exception as e:
            return f"Oops! CyDuck had a hiccup: {str(e)}"
    
    def get_chat_history(self, limit=10):
        """Get recent chat history"""
        return self.chat_history[-limit:] if self.chat_history else []
    
    def clear_history(self):
        """Clear all chat history"""
        self.chat_history = []
        self.save_history()
        return "Chat history cleared! 🦆"
