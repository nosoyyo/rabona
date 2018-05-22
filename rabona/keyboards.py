from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# main menu
main_menu_kb = [[InlineKeyboardButton("上传战果", callback_data='upload'),
                 InlineKeyboardButton("手动输入", callback_data='raw_input'), ],
                [InlineKeyboardButton("查看战绩", callback_data='results')],
                [InlineKeyboardButton("赛事", callback_data='events')]]

main_menu_markup = InlineKeyboardMarkup(main_menu_kb)

# general cancel
cancel_kb = [[InlineKeyboardButton("算了", callback_data='cancel')]]
cancel_markup = InlineKeyboardMarkup(cancel_kb)


# result confirmation
confirmation_kb = [[InlineKeyboardButton("没毛病", callback_data='correct'),
                    InlineKeyboardButton("有毛病", callback_data='wrong')],
                   [InlineKeyboardButton("算了", callback_data='cancel')]]
confirmation_markup = InlineKeyboardMarkup(confirmation_kb)


class Keyboard():
    pass
