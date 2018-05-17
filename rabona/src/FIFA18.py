class Preparation():
    '''
        first of all, binarize the raw image
        the smaller the step is, the better the final result looks
        but also slower down the process
    '''
    guess = 175
    bleed = 50
    bounds = (40, 55)
    step = 10


class RectifyScreen():
    '''
        use this template for crop the screen area
    '''
    bleed = 50
    threshold = 175
    vertical_darkness = 10
    vertical_whiteness = 175
    right_whiteness = 40
    right_darkness = 20
    left_whiteness = 10
    left_darkness = 10


class Segmentation():
    '''
        do segmenting on the screen detected
        so pure screen here, avr_whiteness could be high!
    '''
    bleed = 10
    guess = 175
    bounds = (136, 146)
    step = 4

    # A_ratio = <A actual height> / <Screen._bin height>
    # for instance:
    A_ratio = 0.25

    # A_score_ratio = <score area width> / <A full width>
    # for instance: 273 / 2131
    A_score_ratio = 0.1281

    # A_score_bleed should be a tiny value, like 2~4 px
    A_score_bleed = 2


class Anchoring():
    '''
        to absolute positioning
    '''
    E_y_bleed = 20
    E_x0_bleed = 20
    E_x1_bleed = 70

    A_y0_bleed = 10

    sa_x_bleed = 10
    sa_y_bleed = 25
    # mutiple coefficient. the bigger, the righter
    sa_x0 = 1.57

    def F_to_screen_w(F_width):
        return 4.021802325581396*F_width+-20.732558139534984

    def F_to_screen_h(F_width):
        return 1.910921926910299*F_width+34.59302325581393

    padding_ratio = (0.03, 0.08125)
