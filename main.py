import os
import random
import threading

import requests
from flask import Flask, request
from facts import FACTS, SYMBOLS
from on_this_day import extract_events_and_births, get_events
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, Application

app = Flask(__name__)
# token = os.environ["TELEGRAM_TOKEN"]
token = "7608536516:AAFX2aQh18Qj9W1q8bUyCwa3I687qLQX5Qs"
bot = ApplicationBuilder().token(token).build()

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


@app.route(f'/webhook/{token}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True))
    bot.process_update(update)
    return 'ok', 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

