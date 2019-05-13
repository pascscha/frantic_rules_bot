# Telegram modules
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from fuzzywuzzy import process
from fuzzywuzzy import fuzz


def start(bot, update):
    bot.send_message(update.message.from_user.id, text="Welcome, this is the Frantic Rule Bot. Simply type /rule [name] and I will explain you how this card works.")


def rule(bot, update):
    with open("raw_rules.txt") as f:
        raw = f.read().split("\n\n")
        rules = {}
        for r in raw:
            title, rule = r.split("\n")
            rules[title.lower()] = rule
    query = update.message.text.lower()
    # Remove "/vote " so that we only get command argument
    query = query.replace("/rule ", "")

    result = process.extractOne(query, list(rules.keys()))[0]
    print(result)

    bot.send_message(update.message.from_user.id,
                     text=rules[result])


# This is good practice: this code only gets run when we run DecidoBot.py,
# but it does not get executed if we were to import some functions from it
if __name__ == "__main__":
    updater = Updater(token="*")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('rule', rule))
    updater.start_polling()
