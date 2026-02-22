# CyDuck Local Development Guide 🦆

Follow these steps to run CyDuck locally on your machine.

## Prerequisites
- Python 3.8+
- [Groq API Key](https://console.groq.com/keys)

## Setup
1. **Clone/Download** the repository.
2. **Setup Environment**:
   - Copy `.env.example` to `.env`.
   - Add your `GROQ_API_KEY` to the `.env` file.
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**:
   ```bash
   python webapp.py
   ```
5. **Access**:
   Open `http://localhost:5000` in your browser.

## Features
- **Local SQLite DB**: Chat history is stored in `cyduck.db`.
- **Streaming**: Experience word-by-word AI responses.
- **Modern UI**: Clean, glassmorphism-based design.
