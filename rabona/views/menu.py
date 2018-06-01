from telegram.ext.dispatcher import run_async

from ri import RabonaImage
from .welcome import Welcome
from .keyboards import Keyboard
from errors import AppointOpponentError
from models import RabonaUser, RabonaMatch


class Menu(Keyboard):
    '''

    Note: if rewrite __init__ then must include

    `self.build(<buttons>)`

    &

    `self.buildMap()`

    '''

    buttons = [['placeholder']]

    def __init__(self, buttons: list=None):
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
        self.build(self.buttons)
        self.buildMap()

    @classmethod
    def start(self, bot, update):

        ru = RabonaUser(update.message.from_user)

        welcome = Welcome(ru)
        message = welcome.message
        # mmid: ru.menu_message_id
        ru.mmid = bot.send_message(
            ru.tele_id, message, reply_markup=self.inline)
        ru.save()

    def help(bot, update):
        update.message.reply_text("Use /start to test this bot.")

    def handler(self, bot, update):
        query = update.callback_query
        if query:
            if query.data == "⚙️ 设置":
                # should use ru.mmid
                mmid = update.effective_message.message_id
                text = 'here you can do some settings.'
                bot.editMessageText(mmid, text, reply_markup=Settings().inline)
            elif query.data == "🚀快速开始":
                mmid = update.effective_message.message_id
                text = 'here you can do some settings.'
                bot.editMessageText(mmid, text, reply_markup=Settings().inline)

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
    def uploadHandler(cls, bot, update):
        mmid = bot.send_message(
            update.effective_user.id,
            'Please hold on, this may take up a while...').message_id
        bot.sendChatAction(update.effective_chat.id, action='typing')

        ru = RabonaUser(update.message.from_user)
        ru.mmid = mmid

        photo_file = bot.get_file(update.message.photo[-1].file_id)
        local_file_name = ru.savePhoto(bot, photo_file)

        # notifying
        bot.send_message('547562504', '{} 上传了一张图片.'.format(ru.appellation))

        # deal with local photo file
        ri = RabonaImage(local_file_name)
        match = RabonaMatch(ru=ru, ri=ri)
        ru.recent_match = match

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

        op = Opponent(match)
        ru.active_menu = op
        ru.save()

        # set keyboard before call a handler!
        # editMessageText(text, cid, mid, reply_markup)
        bot.editMessageText(text, ru.tele_id, mmid,
                            reply_markup=op.inline)

        # TODO save local_file_name in Qiniu

    def challangeHandler(self, bot, update):
        pass


class Opponent(Menu):
    '''
    Part II of upload. Appoint opponent.
    Note: if rewrite __init__ then must include

    `self.build(<buttons>)`

    &

    `self.buildMap()`

    :param mmid: `int` message_id for bot.editMessageText
    '''

    buttons = [["AI", "好友..."]]

    def __init__(self, rm: RabonaMatch):
        self.match = rm
        self.build(self.buttons)
        self.buildMap()

    def AIHandler(self, bot, update):
        # message = '对手 {} 是 AI.'.format(self.match.home) or away??
        # TODO
        ru = RabonaUser(update.message.from_user)
        self.match.opponent = 'AI'
        self.match.save()
        # editMessageText(text, cid, mid, reply_markup)
        bot.editMessageText('比赛已保存。', ru.tele_id, ru.mmid)

    def contactHandler(self, bot, update):
        pass
