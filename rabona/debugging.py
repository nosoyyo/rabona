import jfw
import models
import pickle
from telegram import bot
from keyboards import Keyboard as k


bot = bot.Bot('587304899:AAFkY8Qv4YQnI4gGwns670STnszZu3CAquI')
u = bot.get_updates()


# u[0].message.reply_text('hello', reply_markup=main_menu_markup)

with open('tests/TeleUser', 'rb') as f:
    tele_user = pickle.load(f)
ru = models.RabonaUser(tele_user)
