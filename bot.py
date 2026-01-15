import os
import nest_asyncio
nest_asyncio.apply()

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from agent import CyDuckAgent

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
agent = CyDuckAgent()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🦆 Quack! I'm CyDuck, your AI assistant! Ask me anything!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = agent.generate_response(user_message)
    await update.message.reply_text(response)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🦆 CyDuck is running!")
    app.run_polling()

if __name__ == "__main__":
    main()
