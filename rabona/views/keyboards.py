import logging
from telegram.message import Message
from telegram.ext.dispatcher import run_async
from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)

from models import RabonaUser
from errors import HandlerInitError


logging.basicConfig(
    filename='var/log/kb.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)


class Keyboard():
    '''
    For conveniently create keyboards.

    :param buttons: `list` something like [button0,[button1, button2],button3]
    :param funcs: `list` handler funcs as affiliation of each button.
                             so that the functions should be put into a list
                             with exactly same format to the buttons list.
    :param ruser: `object` RabonaUser obj, for user-keyboard-related stuff
    :param BACK: `bool` add a 'BACK' button into the keyboard if True
    :param CANCEL: `bool` same to 'BACK'
    '''

    DIGITS = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['0']]

    def __init__(self, buttons: list=None):

        self.previous_keyboard = ''
        self.current_keyboard = ''
        self.keyboard_to_send = ''

        if buttons:
            self.build(buttons)
        elif self.buttons:
            self.build(self.buttons)

    def build(self, buttons: list, funcs: list=None):
        flatten = [y for x in buttons for y in x]
        inline = []
        reply = []
        for item in buttons:
            inline_item = list(
                map(lambda text: InlineKeyboardButton(
                    text, callback_data=text), item))
            reply_item = list(map(KeyboardButton, item))

            inline.append(inline_item)
            reply.append((reply_item))
        self.inline = InlineKeyboardMarkup(inline)
        self.reply = ReplyKeyboardMarkup(reply)

        # mapping
        if funcs:
            if len(flatten) != len(funcs):
                raise HandlerInitError(len(flatten), len(funcs))
            else:
                self.mapping = dict(zip(flatten, funcs))

    @classmethod
    def add_handler(cls, handler: callable):
        pass

    @classmethod
    @run_async
    def handler(cls, obj, bot, update) -> Message or bool:
        if update.callback_query:
            ru = RabonaUser(update.effective_user)
            query = update.callback_query
            cid = update.effective_chat.id
            logging.debug('caught {}, returning {}'.format(
                query.data, obj.mapping[query.data]))

            # here a bit tricky
            # since calling a class.method(not @classmethod!)
            # need to put the obj as the first positional arg
            obj.mapping[query.data](obj, bot, update)
            
        else:
            return obj.mapping[update.message.text]
