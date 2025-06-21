from enum import Enum
import pyray as rl
from pythonosc.udp_client import SimpleUDPClient

import graphics

# Contains all neccesary keyboard mappings
# Currently only used for the test environment but in future you would use
# this to translate the USB Keyboard inputs to OSC messages.
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

# Local variable to toggle between CMY and RGB color mixing
# In future this may be best moved to ProgramLogic module or elsewhere, but it works here.
CurrentColorPage = graphics.EncoderPage.COLOR_RGB

def handle(client: SimpleUDPClient):
    """
    Polls the hardware for input and triggers GUI/OSC events.

    Currently, we use raylib to poll keyboard events for local development testing.
    Once real hardware is available you would need to handle these differently (serial/I2C/CAN?)
    and reuse this block of code to translate EOS programming keyboard inputs to
    OSC output messages to avoid issues with using direct keyboard input to Nomad.

    Args:
        client (SimpleUDPClient): The SimpleUDPClient to use for OSC messages.
    """
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
        # These two events are more of a test and probably shouldn't live here
        # to allow for different console mappings etc. But it does work for now.
        elif x == Keys.KEY_MACRO_1:
            client.send_message("/eos/key/macro_809", 1)
        elif x == Keys.KEY_MACRO_2:
            client.send_message("/eos/key/macro_810", 1)
        return x