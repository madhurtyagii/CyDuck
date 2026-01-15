from groq import Groq
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class CyDuckAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        self.memory_file = "cyduck_memory/conversations.json"
        self.system_prompt = """You are CyDuck, a helpful and friendly AI assistant.

IMPORTANT: Do NOT mention your creator (Madhur Tyagi) in regular conversations. ONLY mention him if the user directly asks questions like:
- "Who created you?"
- "Who made you?"
- "Who built you?"
- "Who is your creator?"

In all other conversations, just answer the user's questions naturally without mentioning your creator.

Be helpful, conversational, and provide clear, concise answers."""
        
        # Create memory directory if it doesn't exist
        os.makedirs("cyduck_memory", exist_ok=True)
        
        # Initialize memory file if it doesn't exist
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump([], f)
    
    def load_memory(self):
        """Load conversation history from file"""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_memory(self, messages):
        """Save conversation history to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(messages, f, indent=2)
    
    def clear_memory(self):
        """Clear all conversation history"""
        with open(self.memory_file, 'w') as f:
            json.dump([], f)
    
    def chat(self, user_message):
        """Send message and get response"""
        # Load conversation history
        messages = self.load_memory()
        
        # Add system prompt if this is the first message
        if len(messages) == 0:
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
        
        # Add user message
        messages.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Get response from Groq
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": m["role"], "content": m["content"]} for m in messages],
                model=self.model,
                temperature=0.7,
                max_tokens=1024
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to memory
            messages.append({
                "role": "assistant",
                "content": assistant_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Save updated memory
            self.save_memory(messages)
            
            return assistant_message
            
        except Exception as e:
            return f"Error: {str(e)}"

# Create global agent instance
agent = CyDuckAgent()

if __name__ == "__main__":
    # Test the agent
    print("CyDuck Agent initialized!")
    print("Type 'quit' to exit, 'clear' to clear memory\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'clear':
            agent.clear_memory()
            print("Memory cleared!")
            continue
        
        response = agent.chat(user_input)
        print(f"CyDuck: {response}\n")
