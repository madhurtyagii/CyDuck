# 🦆 CyDuck AI: The Premium Assistant

<div align="center">

![CyDuck Banner](https://img.shields.io/badge/CyDuck-Llama%204%20Maverick-8B5CF6?style=for-the-badge&logo=robot&logoColor=white)
[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge&logo=render)](https://cyduck-wgms.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A high-performance, glassmorphism-styled AI companion powered by Llama 4 Maverick.**

[Live Demo](https://cyduck-wgms.onrender.com) • [Report Bug](https://github.com/madhurtyagii/CyDuck/issues) • [Request Feature](https://github.com/madhurtyagii/CyDuck/issues)

</div>

---

## 🌟 Fabulous Features

- 🚀 **Llama 4 Maverick Engine** - Powered by Meta's flagship MoE model on Groq.
- 🌊 **Real-Time Streaming** - Word-by-word response delivery for a fluid experience.
- 🧠 **Smart Multi-Session Memory** - SQLite-backed history that remembers everything.
- 🏷️ **Auto-Rename** - CyDuck intelligently names your chats based on your first prompt.
- 🎨 **Glassmorphism UI** - Stunning modern design with semi-transparent frosted effects.
- � **Dev-First Rendering** - Beautiful Markdown support with Syntax Highlighting and "Copy Code" buttons.
- ⚡ **Turbo Speed** - Sub-second inference powered by Groq's LPU architecture.
- �️ **Render Optimized** - Fine-tuned to run smoothly on 512MB RAM free-tier servers.

---

## 🛠️ Modern Tech Stack

- **Backend:** Flask & Python 3.12
- **AI Model:** Groq API (`meta-llama/llama-4-maverick-17b-128e-instruct`)
- **Frontend:** HTML5, CSS3 (Glass), JavaScript (Vanilla, marked.js, highlight.js)
- **Database:** SQLite (`cyduck.db`) for robust history management
- **Deployment:** Render (Free Tier Optimized)

---

## 📦 Installation & Setup

### Prerequisites

- **Python 3.12**
- **Groq API Key** ([Get one here](https://console.groq.com))
- **Git**

### Local Development

1. **Clone & Enter**
   ```bash
   git clone https://github.com/madhurtyagii/CyDuck.git
   cd CyDuck
   ```

2. **Environment Setup**
   Create a `.env` file:
   ```env
   GROQ_API_KEY=your_key_here
   PORT=5000
   DEBUG=True
   ```

3. **Install & Run**
   ```bash
   pip install -r requirements.txt
   python webapp.py
   ```

4. **Visit**
   `http://localhost:5000`

---

## 📁 Project Structure

```
CyDuck/
├── static/              # CSS & Glassmorphism styles
├── templates/           # Modern index.html with Markdown logic
├── agent.py             # Llama 4 Agent & Memory logic
├── webapp.py            # Flask endpoints & SSE server
├── cyduck.db            # SQLite history (Auto-generated)
├── requirements.txt     # Locked dependencies
├── runtime.txt          # Python 3.12 runtime config
└── .env                 # Secret keys (ignored by git)
```

---

## ‍💻 Author

**Madhur Tyagi**

- GitHub: [@madhurtyagii](https://github.com/madhurtyagii)
- Portfolio: [Coming Soon]
- Passion: Building state-of-the-art AI applications that WOW!

---

<div align="center">

**Made with ❤️ and 🦆 by Madhur Tyagi**

⭐ **Star this repo if you're quacking with excitement!** ⭐

</div>
