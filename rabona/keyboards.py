from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)


class Keyboard():
    '''
    For conveniently create keyboards.

    :param buttons: `list` something like [button0,[button1, button2],button3]
    '''

    cancel_cn = [["😂 算了"]]

    digits_only = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['0']]
    back = ["↩️ 返回"]
    

    # competition
    comp_cn_0 = [["✏️创建赛事", "🏆我的赛事"], back]
    # create competition
    comp_cn_1 = []

    def __init__(self, buttons: list=None, ruser=None):

        self.makeButton = KeyboardButton
        self.makeInlineButton = InlineKeyboardButton
        self.previous_keyboard = ''
        self.current_keyboard = ''
        self.keyboard_to_send = ''

        if buttons:
            inline = []
            for item in buttons:
                if isinstance(item, list):
                    inline_item = []
                    for atom in item:
                        inline_item.append(InlineKeyboardButton(
                            atom, callback_data=atom))
                        atom = KeyboardButton(atom)
                    inline.append(inline_item)
                else:
                    inline.append(InlineKeyboardButton(
                        item, callback_data=item))
                    item = KeyboardButton(item)

            self.inline = InlineKeyboardMarkup(inline)
            self.reply = ReplyKeyboardMarkup(buttons)

    @classmethod
    def handler(self, bot, update):
        if update.message == 's':
            pass
