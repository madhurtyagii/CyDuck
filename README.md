# 🦆 CyDuck AI Assistant

<div align="center">

![CyDuck Banner](https://img.shields.io/badge/CyDuck-AI%20Assistant-8B5CF6?style=for-the-badge&logo=robot&logoColor=white)
[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge&logo=render)](https://cyduck-wgms.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Your intelligent AI companion with memory!**

[Live Demo](https://cyduck-wgms.onrender.com) • [Report Bug](https://github.com/madhurtyagii/CyDuck/issues) • [Request Feature](https://github.com/madhurtyagii/CyDuck/issues)

</div>

---

## 🌟 Features

- 🤖 **AI-Powered Conversations** - Powered by Groq's LLaMA 3.3 70B model
- 🧠 **Conversation Memory** - Remembers your chat history across sessions
- 🎨 **Beautiful UI** - Modern gradient design with smooth animations
- ⚡ **Fast Responses** - Lightning-quick AI inference with Groq
- 🔒 **Secure** - Environment-based API key management
- 📱 **Responsive** - Works perfectly on desktop, tablet, and mobile devices
- 👨‍💻 **Creator Info** - Ask CyDuck about its creator!

---

## 🚀 Live Demo

Try CyDuck now: **[https://cyduck-wgms.onrender.com](https://cyduck-wgms.onrender.com)**

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python 3.13)
- **AI Model:** Groq API (LLaMA 3.3 70B Versatile)
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Render
- **Production Server:** Gunicorn
- **Memory System:** JSON-based conversation storage

---

## 📦 Installation

### Prerequisites

- Python 3.13 or higher
- Groq API Key ([Get one free here](https://console.groq.com))
- Git

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/madhurtyagii/CyDuck.git
   cd CyDuck
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   python webapp.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

---

## 🎯 Usage

1. Open CyDuck in your web browser
2. Type your message in the input box at the bottom
3. Press **Send** or hit **Enter**
4. CyDuck responds with AI-generated answers
5. Your conversation history is automatically saved
6. Click **"Clear History"** button to start a fresh conversation
7. Try asking: *"Who created you?"* to learn about the creator!

---

## 📁 Project Structure

```
CyDuck/
├── templates/
│   └── index.html          # Frontend UI template
├── cyduck_memory/          # Conversation history storage
│   └── conversations.json  # Stored conversations
├── agent.py               # AI agent logic with Groq integration
├── webapp.py              # Flask web application
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version for deployment
├── nixpacks.toml         # Nixpacks configuration
├── .env                  # Environment variables (not in repo)
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for AI inference | ✅ Yes |

---

## 🚢 Deployment

### Deploy on Render (Recommended)

1. **Fork this repository** to your GitHub account
2. Sign up at [Render.com](https://render.com) (free tier available)
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure the service:
   - **Name:** `cyduck` (or your preferred name)
   - **Region:** Choose closest to your location
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn webapp:app`
6. Add environment variables in the **Environment** section:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
7. Select the **Free** plan
8. Click **"Create Web Service"**
9. Wait 2-3 minutes for deployment to complete
10. Your app is live! 🎉

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - feel free to use it for your own projects!

---

## 👨‍💻 Author

**Madhur Tyagi**

- GitHub: [@madhurtyagii](https://github.com/madhurtyagii)
- Project: [CyDuck](https://github.com/madhurtyagii/CyDuck)
- Live Demo: [https://cyduck-wgms.onrender.com](https://cyduck-wgms.onrender.com)

BCA Student & AI Engineer passionate about building intelligent applications!

---

## 🙏 Acknowledgments

- [Groq](https://groq.com) - For providing the lightning-fast AI inference API
- [Flask](https://flask.palletsprojects.com/) - Excellent Python web framework
- [Render](https://render.com) - Seamless deployment platform

---

<div align="center">

**Made with ❤️ and 🦆 by Madhur Tyagi**

⭐ **Star this repo if you found it helpful!** ⭐

</div>
