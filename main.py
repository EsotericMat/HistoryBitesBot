import os
import random
import json
from facts import FACTS, SYMBOLS
from on_this_day import extract_events_and_births
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, Application

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
        events = random.choices(extract_events_and_births()[0], k=5)
        txt = ''.join([f"{ev}. \n\n" for ev in events])
        await update.message.reply_text(f"{SYMBOLS[user_choice]} On This Day \n\n{txt}")

    elif user_choice == "On this Day: Birth":
        events = random.choices(extract_events_and_births()[1], k=5)
        txt = ''.join([f"{ev}. \n\n" for ev in events])
        await update.message.reply_text(f"{SYMBOLS[user_choice]} On this Day: Birth \n\n{txt}")

    elif user_choice in FACTS.keys():
        fact = random.choice(FACTS[user_choice])
        await update.message.reply_text(f"{SYMBOLS[user_choice]} {fact}")

def webhook(request):
    # Build the bot application
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    app = Application.builder().token(os.environ["TELEGRAM_TOKEN"]).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_fact))

    # Convert incoming Telegram update to Update object
    try:
        logger.info(f"Incoming request: {request.data}")
        update = Update.de_json(json.loads(request.data), app.bot)
        app.update_queue.put_nowait(update)

        return "OK", 200
    except Exception as e:
        print(e)
        return f"Error: {e}", 500

# def main():
#     # Replace 'YOUR_API_TOKEN' with your bot's API token
#     app = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
#
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_fact))
#
#     print("Bot is running...")
#     app.run_polling()
#     return 'ok'

# if __name__ == "__main__":
#     os.environ['TELEGRAM_TOKEN'] = "7608536516:AAFX2aQh18Qj9W1q8bUyCwa3I687qLQX5Qs"
#     main()

# curl -X POST "https://api.telegram.org/bot<YOUR_TELEGRAM_TOKEN>/setWebhook" \
#      -d "url=<YOUR_CLOUD_FUNCTION_URL>"