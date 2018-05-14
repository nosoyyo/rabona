class DetectScreen():
    '''
        first of all, get the screen from raw
        the smaller the step is, the better the final result looks
        but also slower down the process
    '''
    bleed = 50
    guess = 175
    bounds = (40, 55)
    step = 10


class Segmentation():
    '''
        do segmenting on the screen detected
        so pure screen here, avr_whiteness could be high!
    '''
    bleed = 10
    guess = 175
    bounds = (136, 146)
    step = 4
    # A_ratio = <A actual height> / <Screen._raw height>
    # for instance: 200 / 1161
    A_ratio = 0.1723
    # A_score_ratio = <score area width> / <A full width>
    # for instance: 273 / 2131
    A_score_ratio = 0.1281
