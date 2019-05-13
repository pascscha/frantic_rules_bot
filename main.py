# Telegram modules
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import random


def start(bot, update):
    bot.send_message(update.message.from_user.id,
                     text="Welcome, this is the Frantic Rule Bot. Simply type <code>/rule &lt;command name&gt;</code> and I will explain you how this card works. Type <code>/rule</code> To get a list of all available rules.",
                     parse_mode=telegram.ParseMode.HTML)


def rule(bot, update):
    try:
        with open("raw_rules.txt") as f:
            raw = f.read().split("\n\n")
            rules = {}
            for r in raw:
                title, rule = r.split("\n")
                rules[title.lower()] = rule
        query = update.message.text.lower()
        # Remove "/vote " so that we only get command argument
        if query == "/rule":
            out = "Usage: /rule &lt;command name&gt;\nAvailable rules:\n"
            for rule in rules.keys():
                out += "\n - <code>/rule {}</code>".format(rule.title())
            out += "\n\n<i>(click rule name to copy it)</i>"
        else:
            query = query.replace("/rule ", "")

            results = process.extract(query, list(rules.keys()), limit=3, scorer=fuzz.ratio)
            if results[0][1] < 70:
                out = "Oops, I'm not sure which rule you mean. Possible options are:"
                for result in results:
                    out += "\n - <code>/rule {}</code>".format(result[0].title())
                out += "\n\n<i>(click rule name to copy it)</i>"
            else:
                print(results[0])

                title = results[0][0].title()
                rule = rules[results[0][0]]

                out = "<b>{}</b>\n{}".format(title, rule)

        bot.send_message(update.message.from_user.id,
                         text=out,
                         parse_mode=telegram.ParseMode.HTML)

    except Exception as e:
        print("Exception: ", e)


def pdf(bot, update):
    bot.send_document(update.message.from_user.id,
                      document="https://rulefactory.ch/wp-content/uploads/2019/02/Regeln_Gesamtuebersicht.pdf",
                      caption="Here you go :)")


def event(bot, update):
    try:
        events = ["Tornado", "Earthquake", "Finish Line", "Vandalism", "Doomsday", "Mating Season", "Robin Hood", "Surprise Party", "Gambling Man", "Time Bomb", "Communism", "Charity", "Friday the 13th", "Expansion", "Recession", "The All Seeing Eye", "Mexican Standoff", "Market", "Third Time Lucky", "Merry Christmas", "Russian Roulette", "Plague", "Event Manager", "Trust Fall", "Double Taxation", "Crowdfunding", "Identity Theft", "Last Chance", "Repeat", "Plus One", "Distributor", "Capitalism", "Seppuku", "Black Hole"]
        query = update.message.text.lower()
        if query == "/event":
            with open("generated.txt") as f:
                text = f.read().strip()
            if len(text) == 0:
                already_played = []
            else:
                already_played = [int(s) for s in text.split(",")]
            unplayed = []
            for i in range(len(events)):
                if i + 1 not in already_played:
                    unplayed.append(i + 1)
            if len(unplayed) == 0:
                bot.send_message(update.message.from_user.id,
                                 text="All event cards have been played. Reshuffle with <code>/event shuffle</code>",
                                 parse_mode=telegram.ParseMode.HTML)
            else:

                with open("raw_rules.txt") as f:
                    raw = f.read().split("\n\n")
                rules = {}
                for r in raw:
                    title, rule = r.split("\n")
                    rules[title.lower()] = rule

                choice = random.choice(unplayed)
                url = "http://rulefactory.ch/special/troublemaker-generator/img/event{}.png".format(choice)
                result = process.extractOne(events[choice - 1], list(rules.keys()), scorer=fuzz.ratio)[0]
                explanation = rules[result]
                bot.send_photo(update.message.from_user.id,
                               photo=url,
                               caption=explanation,
                               parse_mode=telegram.ParseMode.HTML)
                already_played.append(choice)

                with open("generated.txt", "w+") as f:
                    f.write(",".join([str(i) for i in already_played]))
        elif query == "/event shuffle":
            with open("generated.txt", "w+") as f:
                f.write("")
            bot.send_message(update.message.from_user.id,
                                 text="All event cards have been shuffled again.",
                                 parse_mode=telegram.ParseMode.HTML)
    except Exception as e:
        print("Error:", e)


# This is good practice: this code only gets run when we run DecidoBot.py,
# but it does not get executed if we were to import some functions from it
if __name__ == "__main__":
    with open("token.txt") as f:
        token = f.read().strip()
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('rule', rule))
    dispatcher.add_handler(CommandHandler('pdf', pdf))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('event', event))
    updater.start_polling()
