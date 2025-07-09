<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="80" alt="Python Logo"/>
</p>

<h1 align="center">PyLauncher</h1>
<p align="center">
  <b>Discord bot for running, analyzing, and learning Python code.<br>
  Developed by Nythque.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python">
  <img src="https://img.shields.io/badge/License-AGPL%20v3-blue">
  <img src="https://img.shields.io/github/issues/nythique/PyLauncher?color=informational">
  <img src="https://img.shields.io/github/stars/nythique/PyLauncher?style=social">
</p>

---

<div align="center">
<details>
  <summary><b style="color:#00ffe7;">Ressources</b></summary>
  <ul>
    <li><a href="https://groq.com/">GROQ API</a></li>
    <li><a href="https://discord.com/developers/applications">DEVELOPER PORTAL</a></li>
  </ul>
</details>
</div>

---

## ✨ Overview

**PyLauncher** is a next-generation Discord bot designed for both beginners and advanced users. It brings a full Python development environment directly to your Discord server, with secure code execution, static analysis, documentation lookup, code explanation, and much more.

---

## 🚦 Features

- 🛡️ **Secure Python & Bash Execution:** Run code snippets safely and receive instant feedback.
- 📓 **Jupyter Notebook Generation:** Create and download Jupyter notebooks from your code.
- 🧑‍💻 **Static Code Analysis:** Detect errors and code issues using Pyflakes.
- 📚 **Documentation Lookup:** Instantly fetch and translate official Python documentation.
- 💡 **Code Explanation:** Get clear, concise explanations of Python code in multiple languages.
- 🔄 **Code Transpilation:** Convert code from JavaScript, Java, C, and more to Python.
- 🎯 **Mini-Challenges:** Generate Python challenges tailored to your skill level.
- 📋 **Pastebin Integration:** Share code easily with Hastebin links.
- 📊 **Server Usage Stats:** Monitor your server's usage and premium status.
- 🛠️ **Admin Tools:** Manage server access, logs, and bot configuration.

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.12+
- Docker (optional, for containerized deployment)
- A Discord bot token

### Installation

```sh
# 1. Clone the repository
git clone https://github.com/nythique/PyLauncher.git
cd PyLauncher

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env and add your Discord and Groq tokens

# 4. Run the bot
python run.py
# Or with Docker
docker-compose up --build -d
```

---

## 💡 Usage

Once the bot is running and invited to your server, use `/help` to see all available commands.

**Examples:**
- `/ping` — Check bot latency.
- `/notebook <title> <code>` — Generate a Jupyter notebook.
- `/analyze <code>` — Analyze Python code for errors.
- `/docs <subject>` — Get official Python documentation.
- `/transpile <language> <code>` — Convert code to Python.
- `/challenge <level> [subject]` — Get a Python challenge.
- `/set channel <channel>` — Restrict code execution to a specific channel (admin only).

---

## 📁 Project Structure

```
.
├── bot/                # Bot launcher and cog loader
├── commands/           # All bot commands (admin & public)
├── config/             # Settings and controller files
├── gen/                # Code execution service
├── home/               # Core logic and plugins
├── logs/               # Error and security logs
├── run.py              # Main entry point
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker build file
├── docker-compose.yml  # Docker Compose config
└── .env                # Environment variables
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or new features.

---

## 📜 License

This project is licensed under the [GNU AGPL v3](LICENSE) and owned by Nythque.

---

<p align="center"><b>PyLauncher</b> — Empowering Python learning and automation on Discord.</p>
Today 09/07/2025
