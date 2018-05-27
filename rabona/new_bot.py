# -*- coding: utf-8 -*-

import jfw
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from ri import RabonaImage
from menu import MainMenu
from keyboards import Keyboard
from models.ru import RabonaUser
from models.rm import RabonaMatch
from utils.config import rabona_bot_TOKEN as TOKEN


logging.basicConfig(
    filename='log/bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def ocr(bot, update):
    bot.sendChatAction(update.effective_user.id, 'typing')
    user = RabonaUser(update.message.from_user)
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    local_file_name = user.savePhoto(bot, photo_file)

    # notifying
    bot.send_message('547562504', '用户 {} 上传了一张图片.'.format(user.title))

    # deal with local photo file
    ri = RabonaImage(local_file_name)
    match = RabonaMatch(user=user, data=ri.A_parsed)
    ocr_kb = Keyboard(ri, match)
    update.message.reply_text('获取比分：{}'.format(
        ri.A_parsed.match_result), reply_markup=ocr_kb.keyboard)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', MainMenu.start))
    updater.dispatcher.add_handler(MessageHandler(
        (Filters.photo | Filters.text), Keyboard.handler))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
