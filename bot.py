import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    CallbackQueryHandler, 
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
import sqlite3
from datetime import datetime

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token
TOKEN = "YourToken"

# Database setup
def setup_database():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        joined_date TEXT
    )
    ''')
    
    # Create interactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action_type TEXT,
        page_visited TEXT,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Database functions
def add_user(user_id, username, first_name, last_name):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        # Add new user
        cursor.execute(
            "INSERT INTO users (user_id, username, first_name, last_name, joined_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, first_name, last_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
    
    conn.close()

def log_interaction(user_id, action_type, page_visited):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO interactions (user_id, action_type, page_visited, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, action_type, page_visited, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    
    conn.commit()
    conn.close()

# Pages content and keyboard layouts
def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 About Me", callback_data="page_about")],
        [InlineKeyboardButton("🗃️ Portfolio", callback_data="portfolio")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard(page="page_main"):
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data=page)]]
    return InlineKeyboardMarkup(keyboard)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name, user.last_name)
    log_interaction(user.id, "command", "/start")
    
    await update.message.reply_text(
        f"Welcome {user.first_name}! I'm your interactive bot. Choose an option below:",
        reply_markup=get_main_menu_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    log_interaction(user_id, "command", "/help")
    
    help_text = (
        "Here's how to use this bot:\n\n"
        "- Click on any button to navigate through different pages\n"
        "- Send any text message to see the main menu\n"
        "- Use /start to return to the main menu\n"
        "- Use /help to see this message again\n"
        "- Use /stats to see your interaction statistics"
    )
    
    await update.message.reply_text(
        help_text,
        reply_markup=get_back_keyboard()
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    log_interaction(user_id, "command", "/stats")
    
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    # Get total interactions count
    cursor.execute("SELECT COUNT(*) FROM interactions WHERE user_id = ?", (user_id,))
    total_interactions = cursor.fetchone()[0]
    
    # Get most visited page
    cursor.execute("""
        SELECT page_visited, COUNT(*) as count 
        FROM interactions 
        WHERE user_id = ? 
        GROUP BY page_visited 
        ORDER BY count DESC 
        LIMIT 1
    """, (user_id,))
    most_visited = cursor.fetchone()
    
    # Get first interaction date
    cursor.execute("""
        SELECT timestamp 
        FROM interactions 
        WHERE user_id = ? 
        ORDER BY timestamp ASC 
        LIMIT 1
    """, (user_id,))
    first_interaction = cursor.fetchone()
    
    conn.close()
    
    stats_text = (
        "📊 Your Interaction Statistics 📊\n\n"
        f"Total interactions: {total_interactions}\n"
    )
    
    if most_visited:
        stats_text += f"Most visited page: {most_visited[0]} ({most_visited[1]} times)\n"
    
    if first_interaction:
        stats_text += f"First interaction: {first_interaction[0]}\n"
    
    await update.message.reply_text(
        stats_text,
        reply_markup=get_back_keyboard()
    )

# Handler for any text message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text
    
    # Add user if not in database
    add_user(user.id, user.username, user.first_name, user.last_name)
    
    # Log the interaction
    log_interaction(user.id, "text_message", f"message: {message_text[:30]}")
    
    # Respond with main menu
    await update.message.reply_text(
        f"Hello {user.first_name}! 👋 Hi there! I'm your Python Backend Developer passionate about turning data challenges into elegant solutions.",
        reply_markup=get_main_menu_keyboard()
    )

# Callback query handler
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    log_interaction(user_id, "button_click", callback_data)
    
    # Main pages
    if callback_data == "page_main":
        await query.edit_message_text(
            text="I look forward to working with you and contributing to your success!:",
            reply_markup=get_main_menu_keyboard()
        )
    
    elif callback_data == "page_about":
        about_text = (
            "🏢 *About Me*\n\n"
            "Python Backend Developer with expertise in data automation and API integration. Since 2022, I've specialized in building efficient systems using Python, RestAPI, Google API, SerpAPI, and OpenAI. "
            "\n\n*💻 Technical Skills:*  \n\n- Python & Data Management\n - RestAPI & API Integration\n - NetApp & Oracle Storage Solutions\n - Web Development (HTML/CSS/JS)\n"
            
            "\n\n*🔍 Experience:*  \n\n- Python Backend Developer (2022-Present)\n - Junior Web Designer (2019-2020)\n - Web Developer (2018)\n"
            "\n\nI'm passionate about solving complex problems through code and creating streamlined data pipelines. Currently expanding my knowledge in data engineering and AI applications."
        )
        await query.edit_message_text(
            text=about_text,
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
    
    elif callback_data == "portfolio":
        portfolio_display = (
            "*Welcome to my portfolio*\n\n🚀 Explore what I do:\n\n"
            "📄 Resume: https://shorturl.at/jCcbu \n"
            "📂 GitHub: https://github.com/No0Bitah \n"
            "🌐 LinkedIn: https://www.linkedin.com/in/jomari-daison-406624334 \n"
        )

        await query.edit_message_text(
            text=portfolio_display,
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
    
    
   

def main():
    # Set up database
    setup_database()
    
    # Create application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CallbackQueryHandler(button_click))
    
    # Add handler for any text message - this will show the main menu
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Run the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
