# -*- coding: utf-8 -*-

import jfw
import logging
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters, CallbackQueryHandler)

import views
from utils.config import rabona_bot_TOKEN as TOKEN

# init logging
logging.basicConfig(
    filename='log/bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# init messaging
global mid
global active_menu


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def handlerDispatcher(bot, update):
    global active_menu
    views.Keyboard.handler(active_menu, bot, update)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(
        CommandHandler('start', views.MainMenu.start))
    updater.dispatcher.add_handler(MessageHandler(
        (Filters.photo | Filters.text), views.Quickstart.uploadHandler))
    updater.dispatcher.add_handler(CommandHandler('help', views.MainMenu.help))
    updater.dispatcher.add_handler(CallbackQueryHandler(handlerDispatcher()))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
