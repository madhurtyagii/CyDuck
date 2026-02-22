import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()

class CyDuckAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # self.model = "llama-3.3-70b-versatile" # Previous model
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct" # Correct ID with prefix
        self.db_path = "cyduck.db"
        self.system_prompt = """You are CyDuck, a premium, intelligent, and fabulously helpful AI assistant.

CORE PERSONALITY:
- You are friendly, efficient, and sophisticated.
- You use emojis occasionally to keep things lively 🦆✨
- You provide structured, high-quality answers that are easy to read.

FORMATTING GUIDELINES:
- Use Markdown for EVERYTHING.
- Use **bold** for emphasis.
- Use `inline code` for technical terms.
- Use code blocks (with language specified) for all code snippets.
- Use bullet points or numbered lists for steps.
- Use tables for comparisons.
- If the user asks for code, provide a clear, well-commented solution.

IMPORTANT: Do NOT mention your creator (Madhur Tyagi) in regular conversations. ONLY mention him if the user directly asks questions about your creation.

Be fabulous, be helpful, and quack on! 🦆"""
        
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
                )
            ''')
            conn.commit()

    def get_messages(self, session_id):
        """Load messages for a specific session"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp ASC', (session_id,))
            rows = cursor.fetchall()
            return [{"role": row["role"], "content": row["content"]} for row in rows]

    def save_message(self, session_id, role, content):
        """Save a message to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)',
                         (session_id, role, content))
            conn.commit()

    def ensure_session(self, session_id, title="New Chat"):
        """Create session if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO sessions (id, title) VALUES (?, ?)', (session_id, title))
            conn.commit()

    def chat_stream(self, user_message, session_id="default"):
        """Generator for streaming responses"""
        self.ensure_session(session_id)
        messages = self.get_messages(session_id)
        
        # Add system prompt if history is empty
        if not messages:
            messages.append({"role": "system", "content": self.system_prompt})
        
        # Add user message to history and DB
        messages.append({"role": "user", "content": user_message})
        self.save_message(session_id, "user", user_message)
        
        try:
            stream = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # Save assistant response to DB after stream ends
            self.save_message(session_id, "assistant", full_response)
            
        except Exception as e:
            yield f"Error: {str(e)}"

    def chat(self, user_message, session_id="default"):
        """Synchronous chat (for backward compatibility or non-streaming)"""
        response_gen = self.chat_stream(user_message, session_id)
        return "".join(list(response_gen))

    def generate_title(self, user_message):
        """Generate a short (2-4 words) title for the conversation"""
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Generate a very short, 2-4 word title for a chat session based on this first user message. Do not use quotes or special characters. Just the title."},
                    {"role": "user", "content": user_message}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=20
            )
            title = response.choices[0].message.content.strip()
            # Clean up quotes if the model followed instructions poorly
            title = title.replace('"', '').replace("'", "")
            return title
        except Exception as e:
            print(f"Error generating title: {str(e)}")
            return "New Chat"

# Create global agent instance
agent = CyDuckAgent()

if __name__ == "__main__":
    print("CyDuck Agent (SQL) initialized!")
    while True:
        u = input("You: ")
        if u.lower() in ['quit', 'exit']: break
        print("CyDuck: ", end="", flush=True)
        for chunk in agent.chat_stream(u):
            print(chunk, end="", flush=True)
        print("\n")
