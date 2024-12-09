import os
import random
import threading
from flask import Flask
from facts import FACTS, SYMBOLS
from on_this_day import extract_events_and_births, get_events
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, Application

app = Flask(__name__)

@app.route('/')
def home():
    return 'botIsUp'

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[key] for key in FACTS.keys()] + [['Random'], ["On this Day"], ["On this Day: Birth"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Welcome! Choose a category to hear an interesting fact:",
        reply_markup=reply_markup
    )


# Message handler for categories
async def send_fact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_choice = update.message.text
    if user_choice == 'Random':
        fact = random.choice([f for fl in FACTS.values() for f in fl])
        await update.message.reply_text(f"{SYMBOLS[user_choice]} {fact}")

    elif user_choice == "On this Day":
        events = random.choices(extract_events_and_births(get_events())[0], k=5)
        txt = ''.join([f"{ev}. \n\n" for ev in events])
        await update.message.reply_text(f"{SYMBOLS[user_choice]} On This Day \n\n{txt}")

    elif user_choice == "On this Day: Birth":
        events = random.choices(extract_events_and_births(get_events())[1], k=5)
        txt = ''.join([f"{ev}. \n\n" for ev in events])
        await update.message.reply_text(f"{SYMBOLS[user_choice]} On this Day: Birth \n\n{txt}")

    elif user_choice in FACTS.keys():
        fact = random.choice(FACTS[user_choice])
        await update.message.reply_text(f"{SYMBOLS[user_choice]} {fact}")


def bot_pull():
    bot = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()

    # Add handlers
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_fact))

    print("Bot is running...")
    bot.run_polling()


if __name__ == "__main__":
    threading.Thread(target=bot_pull).start()
    app.run(host='0.0.0.0',
            port=5000)

