import jfw
from keyboards import main_menu_markup
from telegram import bot
bot = bot.Bot('587304899:AAFkY8Qv4YQnI4gGwns670STnszZu3CAquI')
u = bot.get_updates()


u[0].message.reply_text('hello', reply_markup=main_menu_markup)
