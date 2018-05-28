import logging
from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)

from models import RabonaUser
from errors import HandlerInitError


logging.basicConfig(
    filename='log/kb.log',
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
    BACK = ["↩️ 返回"]
    CANCEL = [["😂 算了"]]

    def back():
        pass

    def cancel():
        pass

    def __init__(self,
                 buttons: list=None,
                 funcs: list=None,
                 ruser: RabonaUser=None,
                 BACK: bool=False,
                 CANCEL: bool=False):

        self.previous_keyboard = ''
        self.current_keyboard = ''
        self.keyboard_to_send = ''

        if buttons:
            if funcs:
                self.build(buttons, funcs)
            else:
                self.build(buttons)

    def build(self, buttons: list, funcs: list=None):
        inline = []
        reply = []
        for item in buttons:
            if isinstance(item, list):
                inline_item = list(
                    map(lambda text: InlineKeyboardButton(
                        text, callback_data=text), item))
                reply_item = list(map(KeyboardButton, item))

            else:
                inline_item = InlineKeyboardButton(
                    item, callback_data=item)
                reply_item = KeyboardButton(item)
            inline.append(inline_item)
            reply.append((reply_item))
        self.inline = InlineKeyboardMarkup(inline)
        self.reply = ReplyKeyboardMarkup(reply)

        # mapping
        if funcs:
            keys = [y for x in buttons for y in x]
            if len(keys) != len(funcs):
                raise HandlerInitError(len(buttons), len(funcs))
            else:
                self.mapping = dict([(keys[i], funcs[i])
                                     for i in range(len(keys))])

    @classmethod
    def handler(cls, k, bot, update):
        if update.callback_query:
            # some inline logic
            query = update.callback_query
            logging.debug('caught {}, returning {}'.format(
                query.data, k.mapping[query.data]))
            return k.mapping[query.data]
        else:
            return k.mapping[update.message.text]
