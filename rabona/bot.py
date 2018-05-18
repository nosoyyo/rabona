# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""
import jfw
import logging
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                          MessageHandler, Filters)

from models.ru import RabonaUser
from ri import RabonaImage


logging.basicConfig(
    filename='log/bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


# main menu
main_menu_kb = [[InlineKeyboardButton("上传战果", callback_data='upload'),
                 InlineKeyboardButton("查看战绩", callback_data='results')],
                [InlineKeyboardButton("赛事", callback_data='events')]]

main_menu = InlineKeyboardMarkup(main_menu_kb)

# general cancel
cancel_kb = [[InlineKeyboardButton("算了", callback_data='cancel')]]
cancel_markup = InlineKeyboardMarkup(cancel_kb)


# result confirmation
confirmation_kb = [[InlineKeyboardButton("没毛病", callback_data='correct'),
                    InlineKeyboardButton("有毛病", callback_data='wrong')]]
confirmation_markup = InlineKeyboardMarkup(confirmation_kb)


def start(bot, update):
    user = RabonaUser(update.effective_user)
    if user.is_new:
        welcome = 'Hi, ' + user.title + \
            '. 我是高级智慧型机器人 rabona.\n 初次见面，请多关照！\n 使用方面的疑问请输入 /help \n 祝您生活愉快😉'
    else:
        welcome = 'Hi ' + user.title + '，今天战绩如何？'
    update.message.reply_text(welcome, reply_markup=main_menu)


def button(bot, update):
    query = update.callback_query
    user = RabonaUser(update.effective_user)
    if query.data == 'upload':
        bot.edit_message_text(text="来吧"+user.title+"，照片走起！",
                              reply_markup=cancel_markup,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

    elif query.data == 'results':
        bot.edit_message_text(text="你等等",
                              reply_markup=cancel_markup,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
    elif query.data == 'events':
        bot.edit_message_text(text="木有这个功能😱",
                              reply_markup=main_menu,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

    elif query.data == 'cancel':
        bot.edit_message_text(text="想好再来😁嘻嘻",
                              reply_markup=main_menu,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)


def opponent(bot, update):
    pass


def photo(bot, update):
    bot.send_message(update.effective_user.id, '牛逼。我看一下啊。')
    user = RabonaUser(update.message.from_user)
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    local_file_name = user.savePhoto(bot, photo_file)

    # notifying
    bot.send_message('547562504', '用户 {} 上传了一张图片.'.format(user.title))
#    bot.send_photo('547562504', photo_file)

    # deal with local photo file
    ri = RabonaImage(local_file_name)
    update.message.reply_text('你看下对不对：{}'.format(
        ri.A_parsed), reply_markup=confirmation_markup)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("587304899:AAFkY8Qv4YQnI4gGwns670STnszZu3CAquI")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
