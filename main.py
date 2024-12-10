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


def main():
    application = Application.builder().token(token).build()
    print('BotIsUp')
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_fact))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    print('main!')
    main()
