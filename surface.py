from enum import Enum
import pyray as rl

import graphics

class Keys(Enum):
    NONE = 0
    KEY_INTENSITY = 49
    KEY_COLOR = 50
    KEY_POSITION = 51
    KEY_MACRO_1 = 52
    KEY_MACRO_2 = 53
    KEY_SELECT_1 = 81
    KEY_SELECT_2 = 87
    KEY_SELECT_3 = 69
    KEY_SELECT_4 = 82
    KEY_SELECT_5 = 84
    KEY_STOP_1 = 65
    KEY_STOP_2 = 83
    KEY_STOP_3 = 68
    KEY_STOP_4 = 70
    KEY_STOP_5 = 71
    KEY_GO_1 = 90
    KEY_GO_2 = 88
    KEY_GO_3 = 67
    KEY_GO_4 = 86
    KEY_GO_5 = 66

CurrentColorPage = graphics.EncoderPage.COLOR_RGB

def handle():
    global CurrentColorPage
    x = rl.get_key_pressed()
    if x in Keys:
        x = Keys(x)
        if x == Keys.KEY_INTENSITY:
            graphics.GFXSetEncoderPage(graphics.EncoderPage.INTENSITY)
        elif x == Keys.KEY_COLOR:
            if graphics.GFXGetEncoderPage() == graphics.EncoderPage.COLOR_RGB:
                CurrentColorPage = graphics.EncoderPage.COLOR_CMY
            elif graphics.GFXGetEncoderPage() == graphics.EncoderPage.COLOR_CMY:
                CurrentColorPage = graphics.EncoderPage.COLOR_RGB
            graphics.GFXSetEncoderPage(CurrentColorPage)
        elif x == Keys.KEY_POSITION:
            graphics.GFXSetEncoderPage(graphics.EncoderPage.POSITION)
        return x