import unittest
from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)

from views import Keyboard as k


class TestKeyboard(unittest.TestCase):

    grp = ['✈️ 按钮0', '🚄 按钮1', '🚗 按钮2']
    buttons = [['test_button0'], ['测试按钮1'], grp, ['结尾']]

    def test_init(self):
        print('\nTestKeyboard | test_init \n')

    def test_basic(self):
        print('\nTestKeyboard | test_basic \n')
        test_kb = k(self.buttons)
        self.assertIsInstance(test_kb.reply, ReplyKeyboardMarkup)
        self.assertIsInstance(test_kb.inline, InlineKeyboardMarkup)

    def test_reply(self):
        test_kb = k(self.buttons)
        for item in test_kb.reply.keyboard:
            text_list = [atom.text for atom in item]
            self.assertEqual(
                text_list, self.buttons[self.buttons.index(text_list)])
            for atom in item:
                self.assertIsInstance(atom, KeyboardButton)

    def test_inline(self):
        print('\nTestKeyboard | test_inline \n')
        test_kb = k(self.buttons)
        for item in test_kb.inline.inline_keyboard:
            text_list = [atom.text for atom in item]
            self.assertEqual(
                text_list, self.buttons[self.buttons.index(text_list)])
            for atom in item:
                self.assertIsInstance(atom, InlineKeyboardButton)
                self.assertEqual(atom.callback_data, atom.text)

    def test_reply_handler(self):
        print('\nTestKeyboard | test_reply_handler \n')
        flatten_buttons = [y for x in self.buttons for y in x]
        funcs = [lambda x: print(x) for x in range(len(flatten_buttons))]
        test_kb = k(self.buttons, funcs)
        for button in flatten_buttons:
            k.text, k.message = button, k
            self.assertEqual(test_kb.handler(test_kb, k, k)(button),
                             funcs[flatten_buttons.index(button)](button))

    def test_inline_handler(self):
        print('\nTestKeyboard | test_inline_handler \n')
        flatten_buttons = [y for x in self.buttons for y in x]
        funcs = [lambda x: print(x) for x in range(len(flatten_buttons))]
        test_kb = k(self.buttons, funcs)

        for button in flatten_buttons:
            k.data, k.callback_query = button, k
            self.assertEqual(test_kb.handler(test_kb, k, k)(button),
                             funcs[flatten_buttons.index(button)](button))


if __name__ == '__main__':
    unittest.main()
