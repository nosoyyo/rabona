from telegram.message import Message
from telegram import InlineKeyboardMarkup

from ri import RabonaImage
from models import RabonaUser, RabonaMatch
from .welcome import Welcome
from .keyboards import Keyboard


class Menu(Keyboard):

    def __init__(self):
        self.buildMap()

    def buildMap(self):
        flatten = [y for x in self.buttons for y in x]
        funcs = self.collectFuncs()
        print(funcs)
        self.mapping = dict(zip(flatten, funcs))

    def collectFuncs(self):
        return list(map(lambda key: self.__class__.__dict__[key], list(filter(
                        lambda key: key.endswith('Handler'),
                        [key for key in self.__class__.__dict__.keys()]))))


class MainMenu(Menu):

    def __init__(self, ru: RabonaUser):
        self.buttons = [[ru.appellation], ["🏆 赛事", "🚀快速开始", "⚙️ 设置"]]

    @classmethod
    def start(self, bot, update):
        global active_menu
        active_menu = self
        user = RabonaUser(update.effective_user)
        welcome = Welcome(user)
        message = welcome.message
        self.mmm = bot.send_message(
            user.tele_id, message, reply_markup=self.inline)

    def help(bot, update):
        update.message.reply_text("Use /start to test this bot.")

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

    def profileHandler(self, bot, update):
        pass

    def compHandler(self, bot, update):
        pass

    def quickstartHandler(self, bot, update):
        pass

    def settingsHandler(self, bot, update):
        pass


class Settings(Menu):

    buttons = [["🛡 主队"], ["🇨🇳 语言/Language🇬🇧"]]

    def setHomeHandler(self, bot, update):
        pass

    def setLangHandler(self, bot, update):
        pass


class Quickstart(Menu):

    buttons = [["📷 传图", "📝 对战"]]

    @classmethod
    def uploadHandler(cls, bot, update) -> (Message, InlineKeyboardMarkup):
        bot.sendChatAction(update.effective_chat.id, action='typing')
        ru = RabonaUser(update.message.from_user)
        photo_file = bot.get_file(update.message.photo[-1].file_id)
        local_file_name = ru.savePhoto(bot, photo_file)

        # notifying
        bot.send_message('547562504', '{} 上传了一张图片.'.format(ru.appellation))

        # deal with local photo file
        ri = RabonaImage(local_file_name)
        match = RabonaMatch(user=ru, data=ri.A_parsed)
        return ri.A_parsed.match_result, Opponent(match).inline

    def challangeHandler(self, bot, update):
        pass


class Opponent(Menu):

    buttons = [["AI", "好友..."]]

    def __init__(self, rm: RabonaMatch):
        self.match = rm

    def AIHandler(self, bot, update) -> (Message, InlineKeyboardMarkup):
        message = '对手 {} 是 AI.'.format(self.match.)

    def contactHandler(self, bot, update):
        pass
