from telegram import ReplyKeyboardMarkup, KeyboardButton


class Keyboard():
    '''
    For conveniently create keyboards.

    :param buttons: `list` something like [button0,[button1, button2],button3]
    '''

    main_menu_cn = [["🚀快速开始"], ["📈我的战报"], ["❕ 挑战"], ["🏆 赛事"], ["⚙️ 设置"]]
    quickstart_cn = [["📷 传图", "📝 手记"], back_cn]
    
    # competition
    comp_cn_0 = [["✏️创建赛事", "🏆我的赛事"], back_cn]
    # create competition
    comp_cn_1 = []
    
    settings_cn = [["🛡 主队"], ["🇨🇳 语言/Language🇬🇧"], back_cn]
    back_cn = ["🔙 返回"]
    cancel_cn = [["😂 算了"]]

    def __init__(self, buttons: list=None, mode: str='reply'):
        self.previous_keyboard = ''
        self.current_keyboard = ''
        self.keyboard_to_send = ''

        if mode is 'reply':
            if buttons:
                for item in buttons:
                    if isinstance(item, list):
                        for atom in item:
                            atom = KeyboardButton(atom)
                    else:
                        item = KeyboardButton(item)

                self.markup = ReplyKeyboardMarkup(buttons)

    @classmethod
    def handler(self, bot, update):
        if update.message ==:


main_menu_markup = Keyboard(Keyboard.main_menu_cn).markup
cancel_markup = Keyboard(Keyboard.cancel_cn).markup
