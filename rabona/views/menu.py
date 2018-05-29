from models import RabonaUser
from .welcome import Welcome
from .keyboards import Keyboard


class Menu():
    pass


class MainMenu(Menu):

    def __init__(self, ru: RabonaUser):
        main_menu = [[ru.appellation], ["🏆 赛事", "🚀快速开始", "⚙️ 设置"]]
        self.inline = Keyboard(main_menu).inline
        self.reply = Keyboard(main_menu).reply

    @classmethod
    def start(self, bot, update):
        user = RabonaUser(update.effective_user)
        welcome = Welcome(user)
        message = welcome.message
        self.mmm = bot.send_message(
            user.tele_id, message, reply_markup=self.inline)

    def handler(self, bot, update):
        query = update.callback_query
        if query:
            if query.data == "⚙️ 设置":
                mid = update.effective_message.message_id
                text = 'here you can do some settings.'
                bot.editMessageText(mid, text, reply_markup=Settings().inline)
            elif query.data == "🚀快速开始":
                mid = update.effective_message.message_id
                text = 'here you can do some settings.'
                bot.editMessageText(mid, text, reply_markup=Settings().inline)


class Settings():
    def __init__(self):
        settings = [["🛡 主队"], ["🇨🇳 语言/Language🇬🇧"]]
        self.inline = Keyboard(settings, BACK=True).inline
        self.reply = Keyboard(settings, BACK=True).reply


class Quickstart():
    def __init__(self):
        quickstart = [["📷 传图", "📝 对战"]]
        self.inline = Keyboard(quickstart, BACK=True).inline
        self.reply = Keyboard(quickstart, BACK=True).reply
