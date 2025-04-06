# 🤖 python-telegram-bot

A personal interactive Telegram bot built with Python, powered by `python-telegram-bot` v20+ and SQLite for tracking user interactions.  
This bot showcases a dynamic portfolio interface and logs activity like commands, button clicks, and messages.

### 📌 Try the Bot Live
👉 [@wakachabot on Telegram](https://t.me/wakachabot)

---

## 💼 Features

- `/start` - Launches the main interactive menu
- `/help` - Provides guidance on using the bot
- `/stats` - Displays your personal interaction statistics
- Interactive inline keyboard navigation
- Pages include:
  - **About Me**
  - **Portfolio** (Resume, GitHub, LinkedIn links)
- SQLite database for:
  - User registrations
  - Interaction logging (clicks, messages, visits)

---

## 🛠 Tech Stack

- Python 3.10+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- SQLite
- Flask-style structure

---

## 🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/python-telegram-bot.git
   cd python-telegram-bot
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your bot**
   - Create a `.env` file or edit `TOKEN` in the script (⚠️ don’t expose it in public repos).

5. **Run the bot**
   ```bash
   python bot.py
   ```

---

## 📂 Project Structure

```
📦 python-telegram-bot/
├── bot.py
├── bot_database.db
├── README.md
├── .gitignore
└── requirements.txt
```

---

## 🛡️ Security Notes

- **Never commit your Telegram Bot Token** to the repository. Use environment variables or a `.env` file.
- This repo is for educational and portfolio purposes.

---

## 👤 Author

**Jomari Daison**  
🔗 [GitHub](https://github.com/No0Bitah) | [LinkedIn](https://www.linkedin.com/in/jomari-daison-406624334)

---

## 📃 License

MIT License. Feel free to fork and customize.
