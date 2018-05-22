from keyboards import main_menu_markup


class Welcome():
    def __init__(self, ruser):
        '''
        Generates welcome message based on analysis of a series of past data.

        :param ruser: `obj` A RabonaUser object
        '''
        self.message = 'rabona serves you.'
        self.keyboard = main_menu_markup
