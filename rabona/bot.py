# local debugging
import jfw

import psutil
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import logging

from conf_mgmt import botConf


# init
logging.basicConfig(
    filename='log/telebot.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
logging.info('session started.')


update_id = None


# general - welcome, start, help, who
def send(bot, update, text):
    bot.send_message(chat_id=update.message.chat_id, text=text)


def start(bot, update):
    lines = """                 🤓欢迎光临🤓\r
                可用命令：
                /start 显示本信息&常用命令
                /help 查看全部命令
                /who 显示当前登录账号

                🐦🐦🐦twitter🐦🐦🐦
                /st 切换 twitter 测试/正式环境"
                /twit <文字内容> 把 <文字内容> 发布到推特，命令后面接一个空格！
                /del <推特链接1> <推特链接2>... 删除一条或多条推特（❕无确认步骤，谨慎❕）
            """
    send(bot, update, lines)


def help(bot, update):
    text = "twitter bot. help maybe."
    send(bot, update, text)


def who():
    tu, thome = user.conf.username, user.conf.home_url
    report = '''
                账号：{}
                测试地址：{}
            '''.format(tu, thome)
    return report

def main():
    """Run the bot."""
    global update_id

    # save pid
    p = psutil.Process()
    with open('pid', 'w') as pidfile:
        pidfile.write(p.pid)

    # 0: maybe 1: btct
    bot = telegram.Bot(botConf('0').TOKEN)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            handle(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def handle(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            if update.message.text == '/start':
                start(bot, update)
            elif update.message.text == '/help':
                help(bot, update)
            elif update.message.text == '/who':
                update.message.reply_text(who())

            elif update.message.text == '/st':
                user = TwitterUser()
                result = user.switch()
                send(bot, update, result)

            elif update.message.text.startswith('/twit'):
                content = update.message.text[6:]
                update.message.reply_text(twit(content))
            elif update.message.text.startswith('/del'):
                content = update.message.text[5:]
                update.message.reply_text(delete(content))

            else:
                update.message.reply_text('你输入了：' + update.message.text)


if __name__ == '__main__':
    main()
