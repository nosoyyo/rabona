from telegram.message import Message
from telegram import InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async

from ri import RabonaImage
from .welcome import Welcome
from .keyboards import Keyboard
from errors import AppointOpponentError
from models import RabonaUser, RabonaMatch


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
    @run_async
    def uploadHandler(cls, bot, update) -> (Message, InlineKeyboardMarkup):
        mid = bot.send_message(update.effective_user.id,
                               'Please hold on, this may take up a while...')
        bot.sendChatAction(update.effective_chat.id, action='typing')
        ru = RabonaUser(update.message.from_user)
        photo_file = bot.get_file(update.message.photo[-1].file_id)
        local_file_name = ru.savePhoto(bot, photo_file)

        # notifying
        bot.send_message('547562504', '{} 上传了一张图片.'.format(ru.appellation))

        # deal with local photo file
        ri = RabonaImage(local_file_name)
        match = RabonaMatch(ru=ru, ri=ri)
        ru.recent_match = match
        ru.save()

        # appoint opponent
        if match.user_310 == 3:
            if match.user_is_home:
                text = '{}，你的主场真是无坚不摧！那个客场的倒霉蛋是谁？'.format(ru.appellation)
            else:
                text = '这是谁？他的主场完全挡不住你{}的铁蹄践踏！'.format(ru.appellation)
        elif match.user_310 == 1:
            text = '能跟{}你势均力敌、平分秋色的家伙，想来也不是易与之辈。'.format(ru.appellation)
        elif match.user_310 == 0:
            if match.user_is_home:
                text = '「防守！防守！」助理教练声嘶力竭地喊着，而你早已瘫在教练席\n你输给了：'.format(
                    ru.appellation)
            else:
                text = '客场输球很正常，再接再厉\n你输给了：'.format(ru.appellation)
        else:
            raise AppointOpponentError(match)

        bot.editMessageText(text, ru.tele_id, mid,
                            reply_markup=Opponent(mid, match).inline)

        # TODO save local_file_name in Qiniu

    def challangeHandler(self, bot, update):
        pass


class Opponent(Menu):
    '''
    Part II of upload. Appoint opponent.

    :param mid: `int` message_id for bot.editMessageText
    '''

    buttons = [["AI", "好友..."]]

    def __init__(self, mid: int, rm: RabonaMatch):
        self.match = rm
        self.mid = mid

    def AIHandler(self, bot, update) -> (Message, InlineKeyboardMarkup):
        # message = '对手 {} 是 AI.'.format(self.match.home) or away??
        # TODO
        self.match.opponent = 'AI'
        self.match.save()
        bot.editMessageText('比赛已保存。', update.effective_user.id, self.mid)

    def contactHandler(self, bot, update):
        pass
