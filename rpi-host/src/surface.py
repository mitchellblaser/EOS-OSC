from enum import Enum
import pyray as rl
from pythonosc.udp_client import SimpleUDPClient

import graphics

import handle as h

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

def linear_scale(source_value, source_min, source_max, target_min, target_max):
    return (source_value - source_min) * (target_max - target_min) / (source_max - source_min) + target_min

def handle(client: SimpleUDPClient, message: bytes):
    """
    Polls the hardware for input and triggers GUI/OSC events.

    Currently, we use raylib to poll keyboard events for local development testing.
    Once real hardware is available you would need to handle these differently (serial/I2C/CAN?)
    and reuse this block of code to translate EOS programming keyboard inputs to
    OSC output messages to avoid issues with using direct keyboard input to Nomad.

    E, A/B, 0/1 - Encoder A/B, Press/Release
    S, 0-21, 0/1 - Switch 0-19 keys, 20-21 Encoder switches, Press/Release
    F, 0-4, 0-255 - Fader 0-5 at value x

    Args:
        client (SimpleUDPClient): The SimpleUDPClient to use for OSC messages.
    """
    global CurrentColorPage

    if message is not b'':
        m = message.rstrip().decode("utf-8").split("_")
        if m[0] == "S":
            switch = int(m[1])
            state = int(m[2])

            if switch in range(15, 20):
                client.send_message("/eos/key/bump_" + str(switch-14), state)
            elif switch in range(10, 15):
                client.send_message("/eos/key/stop_" + str(switch-9), state)
            elif switch in range(5, 10):
                client.send_message("/eos/key/fader_" + str(switch-4), state)
            elif switch in range(0, 5):
                if switch == 0 and state == 0:
                    graphics.GFXSetEncoderPage(graphics.EncoderPage.INTENSITY)
                elif switch == 1 and state == 0:
                    if graphics.GFXGetEncoderPage() == graphics.EncoderPage.COLOR_RGB:
                        CurrentColorPage = graphics.EncoderPage.COLOR_CMY
                    elif graphics.GFXGetEncoderPage() == graphics.EncoderPage.COLOR_CMY:
                        CurrentColorPage = graphics.EncoderPage.COLOR_RGB
                    graphics.GFXSetEncoderPage(CurrentColorPage)
                elif switch == 2 and state == 0:
                    graphics.GFXSetEncoderPage(graphics.EncoderPage.POSITION)
            elif switch in range(20, 22) and state == 0:
                if h.GetActiveEncoder() == 1:
                    h.SetActiveEncoder(2)
                else:
                    h.SetActiveEncoder(1)

        elif m[0] == "F":
            client.send_message("/eos/fader/1/" + str(int(m[1])+1), round(linear_scale(int(m[2]), 0, 255, 0, 1), 3))

        elif m[0] == "E":
            if graphics.GFXGetEncoderPage() == graphics.EncoderPage.INTENSITY:
                if h.GetActiveEncoder() == 1:
                    if m[1] == "A":
                        if m[2] == "1":
                            client.send_message("/eos/wheel/Intens", 1)
                        else:
                            client.send_message("/eos/wheel/Intens", -1)
                else:
                    if m[1] == "A":
                        if m[2] == "1":
                            client.send_message("/eos/wheel/Zoom", 1)
                        else:
                            client.send_message("/eos/wheel/Zoom", -1)
                    if m[1] == "B":
                        if m[2] == "1":
                            client.send_message("/eos/wheel/Edge", 1)
                        else:
                            client.send_message("/eos/wheel/Edge", -1)




    # x = rl.get_key_pressed()
    # if x in Keys:
    #     x = Keys(x)
    #     if x == Keys.KEY_INTENSITY:
    #         graphics.GFXSetEncoderPage(graphics.EncoderPage.INTENSITY)
    #     elif x == Keys.KEY_COLOR:
    #         if graphics.GFXGetEncoderPage() == graphics.EncoderPage.COLOR_RGB:
    #             CurrentColorPage = graphics.EncoderPage.COLOR_CMY
    #         elif graphics.GFXGetEncoderPage() == graphics.EncoderPage.COLOR_CMY:
    #             CurrentColorPage = graphics.EncoderPage.COLOR_RGB
    #         graphics.GFXSetEncoderPage(CurrentColorPage)
    #     elif x == Keys.KEY_POSITION:
    #         graphics.GFXSetEncoderPage(graphics.EncoderPage.POSITION)
    #     # These two events are more of a test and probably shouldn't live here
    #     # to allow for different console mappings etc. But it does work for now.
    #     elif x == Keys.KEY_MACRO_1:
    #         client.send_message("/eos/key/macro_809", 1)
    #     elif x == Keys.KEY_MACRO_2:
    #         client.send_message("/eos/key/macro_810", 1)
