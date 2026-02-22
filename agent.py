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
        self.model = "llama-4-maverick-17b-128e-instruct" # Best available currently, Llama 4 Maverick
        self.db_path = "cyduck.db"
        self.system_prompt = """You are CyDuck, a helpful and friendly AI assistant.

IMPORTANT: Do NOT mention your creator (Madhur Tyagi) in regular conversations. ONLY mention him if the user directly asks questions like:
- "Who created you?"
- "Who made you?"
- "Who built you?"
- "Who is your creator?"

In all other conversations, just answer the user's questions naturally without mentioning your creator.

Be helpful, conversational, and provide clear, concise answers."""
        
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
