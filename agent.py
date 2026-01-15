import os
from datetime import datetime
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class CyDuckAgent:
    def __init__(self):
        # Initialize Groq client
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables!")
        
        self.client = Groq(api_key=api_key)
        self.model_name = "llama-3.3-70b-versatile"  # Fast and powerful!
        
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
        context = []
        for msg in recent:
            context.append({"role": "user", "content": msg['user']})
            context.append({"role": "assistant", "content": msg['assistant']})
        return context
    
    def generate_response(self, user_message, user_id="default"):
        """Generate AI response with conversation memory using Groq"""
        try:
            # Get conversation context
            context = self.get_recent_context(limit=3)
            
            # Build messages array
            messages = [
                {
                    "role": "system",
                    "content": """You are CyDuck 🦆, a helpful AI assistant built by Madhur Tyagi. 
You are friendly, knowledgeable, and remember past conversations.
Keep responses concise, helpful, and engaging."""
                }
            ]
            
            # Add context
            messages.extend(context)
            
            # Add current message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                stream=False
            )
            
            ai_response = chat_completion.choices[0].message.content.strip()
            
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
