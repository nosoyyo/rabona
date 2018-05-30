class Welcome():
    def __init__(self, ru):
        '''
        Generates welcome message based on analysis of a series of past data.

        :param ru: `obj` A RabonaUser object
        '''
        self.message = ('你好，{}！'
                        '直接上传图片或拍照就可触发记录赛果流程'
                        '其他功能内测中，暂未开放'.format(ru.appellation)
                        )
