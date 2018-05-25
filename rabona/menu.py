from models import RabonaUser
from welcome import Welcome
from keyboards import Keyboard


class Menu():
    pass


class MainMenu(Menu):
    @classmethod
    def start(self, bot, update):
        user = RabonaUser(update.effective_user)
        welcome = Welcome(user)
        message = welcome.output
        keyboard = welcome.keyboard
        mmm = bot.send_message(user.tele_id, message, reply_markup=keyboard)
        self.mmmid = mmm.message_id
