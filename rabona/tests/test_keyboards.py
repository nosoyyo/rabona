import unittest
from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)

from views import Keyboard as k


class SomeRealKeyboard(k):
    grp = ['✈️ 按钮0', '🚄 按钮1', '🚗 按钮2']
    buttons = [['test_button0'], ['测试按钮1'], grp, ['结尾']]

    def func0(self):
        print('func0')

    def func1(self):
        print('func1')

    def func2(self):
        print('func2')

    def func3(self):
        print('func4')

    def func4(self):
        print('func4')

    def func5(self):
        print('func5')


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


'''
    def test_reply_handler(self):
        print('\nTestKeyboard | test_reply_handler \n')
        flatten = [y for x in self.buttons for y in x]
        s = SomeRealKeyboard()
        for button in flatten:
            s.text, s.message = button, s
            self.assertEqual(s.handler(s, s, s)(button),
                             funcs[flatten.index(button)](button))


    def test_inline_handler(self):
        print('\nTestKeyboard | test_inline_handler \n')
        flatten = [y for x in self.buttons for y in x]
        s = SomeRealKeyboard()

        for button in flatten:
            s.data, s.callback_query = button, s
            self.assertEqual(s.handler(s, s, s)(button),
                             funcs[flatten.index(button)](button))

    def test_self_contained_buttons_and_funcs(self):
        print('\nTestKeyboard | test_self_contained_buttons_and_funcs \n')
        s = SomeRealKeyboard()
        self.assertIsInstance(s.reply, ReplyKeyboardMarkup)
        self.assertIsInstance(s.inline, InlineKeyboardMarkup)
'''

if __name__ == '__main__':
    unittest.main()
