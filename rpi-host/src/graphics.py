######################
## IMPORT LIBRARIES ##
######################
import pyray as rl
from enum import Enum
import UIElements as UI
from programlogic import State, GetMyIPAddress, GetConsoleIPAddress
from handle import SelectedChannel, EncoderState

# Load a custom font
font = rl.load_font_ex("font.ttf", 200, None, 0)

#################
## DEFINITIONS ##
#################
class col():
    """
    Stores some predefined colors that determine how
    we draw our UI elements
    """
    encoderDisabled = rl.Color(10, 10, 10, 255)
    encoderBorders = rl.Color(30, 30, 30, 30)
    encoderTitle = rl.WHITE
    encoderFontDisabled = rl.GRAY
    faderNumberFont = rl.LIME
    faderFont = rl.WHITE
    buttonBackground = rl.BLACK
    buttonFont = rl.WHITE
    buttonBackgroundActive = rl.WHITE
    buttonFontActive = rl.BLACK
    toolbarBackground = rl.GRAY

class EncoderPage(Enum):
    """
    A list of all possible encoder pages
    """
    INTENSITY = 0
    COLOR_RGB = 1
    COLOR_CMY = 2
    POSITION = 3

# Default to intensity on bootup
activeEncoderPage = EncoderPage.INTENSITY

def scan() -> str:
    """
    Checks if mouse button (or touch) has been pressed,
    and returns the element's unique ID string.

    Returns:
        str: Unique element identifier.
    """
    if rl.is_mouse_button_pressed(0):
        return get_element_from_coordinates(rl.get_mouse_x(), rl.get_mouse_y())

def get_element_from_coordinates(x: int, y: int) -> str:
    """
    Checks all elements in a list and returns a unique identifier.

    Args:
        x (int): The X coordinate of the touch event.
        y (int): The Y coordinate of the touch event.

    Returns:
        str: The unique identifier as a string.
    """
    global ProgramState

    if ProgramState == State.MAIN:
        iterate_target = UI.Elements_MainWindow
    elif ProgramState == State.MENU:
        iterate_target = UI.Elements_MenuWindow
    else:
        return ""
    
    for element in iterate_target:
        if x in range(iterate_target[element].sx, iterate_target[element].ex):
            if y in range(iterate_target[element].sy, iterate_target[element].ey):
                return element
    return ""

def GFXSetState(state: State):
    """
    Sets the local ProgramState variable,
    which is responsible for changing pages in the application.

    Args:
        state (programlogic.State): The desired GUI page to draw.
    """
    global ProgramState
    ProgramState = state

def GFXSetEncoderPage(page: EncoderPage):
    """
    Sets the local activeEncoderPage variable,
    which is responsible for changing which encoder page is
    currently being drawn.

    Args:
        page (EncoderPage): The desired encoder page to draw.
    """
    global activeEncoderPage
    activeEncoderPage = page

def GFXGetEncoderPage() -> EncoderPage:
    """
    Exposes the variable activeEncoderPage so it can be called
    from other modules.

    Returns:
        EncoderPage: The currently active Encoder Page.
    """
    global activeEncoderPage
    return activeEncoderPage

###################
## DRAW ROUTINES ##
###################
def GFXSetup():
    global ProgramState
    global font
    ProgramState = State.MAIN
    rl.init_window(320, 480, "LunarOSC-EOS")
    font = rl.load_font_ex("font.ttf", 200, None, 0)

def GFXDraw(faders, channel, commandline, encoders, activeEncoder):
    global ProgramState
    rl.begin_drawing()
    if ProgramState == State.MAIN:
        # rl.draw_text_ex(font, "TEST", rl.Vector2(50, 120), 20, 0.5, rl.WHITE)
        DrawMainWindow(faders=faders, channel=channel, commandline=commandline, encoders=encoders, activeEncoder=activeEncoder)
    if ProgramState == State.MENU:
        DrawMenuWindow()
    rl.end_drawing()
    return rl.window_should_close()

def DrawMainWindow(faders, channel, commandline, encoders, activeEncoder):
    rl.clear_background(rl.BLACK)
    rl.draw_rectangle(0, 0, 320, 50, rl.GRAY)
    rl.draw_rectangle(UI.Elements_MainWindow["Toolbar_Menu"].sx, UI.Elements_MainWindow["Toolbar_Menu"].sy, UI.Elements_MainWindow["Toolbar_Menu"].width, UI.Elements_MainWindow["Toolbar_Menu"].height, col.buttonBackground)
    rl.draw_text_ex(font, "Setup", rl.Vector2(UI.Elements_MainWindow["Toolbar_Menu"].sx+12, UI.Elements_MainWindow["Toolbar_Menu"].sy+10), 24, 0.5, col.buttonFont)
    DrawFaderIcon(1, faders[0][1])
    DrawFaderIcon(2, faders[1][1])
    DrawFaderIcon(3, faders[2][1])
    DrawFaderIcon(4, faders[3][1])
    DrawFaderIcon(5, faders[4][1])
    DrawEncoderDisplay(encoders, activeEncoder)
    # DrawSelectedChannel(channel)
    DrawCommandLine(commandline)

def DrawNumberTicker(posx, posy, value):
    rl.draw_rectangle(posx, posy, 50, 50, rl.GRAY)
    rl.draw_text_ex(font, "+", rl.Vector2(posx+6, posy-15), 80, 0.5, rl.BLACK)
    rl.draw_rectangle_lines(posx, posy+50, 50, 50, rl.GRAY)
    rl.draw_text_ex(font, str(value), rl.Vector2(posx, posy+60), 28, 0.5, rl.WHITE)
    rl.draw_rectangle(posx, posy+100, 50, 50, rl.GRAY)
    rl.draw_text_ex(font, "-", rl.Vector2(posx+8, posy+100-27), 100, 0.5, rl.BLACK)

def DrawMenuWindow():
    rl.clear_background(rl.BLACK)
    rl.draw_rectangle(0, 0, 320, 50, col.toolbarBackground)
    rl.draw_rectangle(UI.Elements_MainWindow["Toolbar_Menu"].sx, UI.Elements_MainWindow["Toolbar_Menu"].sy, UI.Elements_MainWindow["Toolbar_Menu"].width, UI.Elements_MainWindow["Toolbar_Menu"].height, col.buttonBackground)
    rl.draw_text_ex(font, "Back", rl.Vector2(UI.Elements_MainWindow["Toolbar_Menu"].sx+16, UI.Elements_MainWindow["Toolbar_Menu"].sy+10), 24, 0.5, col.buttonFont)

    rl.draw_text_ex(font, "IP Address", rl.Vector2(30, 60), 24, 0.5, rl.WHITE)
    DrawNumberTicker(30, 85, GetMyIPAddress()[0])
    DrawNumberTicker(100, 85, GetMyIPAddress()[1])
    DrawNumberTicker(170, 85, GetMyIPAddress()[2])
    DrawNumberTicker(240, 85, GetMyIPAddress()[3])

    rl.draw_text_ex(font, "Console IP", rl.Vector2(30, 240), 24, 0.5, rl.WHITE)
    DrawNumberTicker(30, 265, GetConsoleIPAddress()[0])
    DrawNumberTicker(100, 265, GetConsoleIPAddress()[1])
    DrawNumberTicker(170, 265, GetConsoleIPAddress()[2])
    DrawNumberTicker(240, 265, GetConsoleIPAddress()[3])

    return

def DrawFaderIcon(index, text):
    posx = UI.Elements_MainWindow["FaderBox_" + str(index)].sx
    posy = UI.Elements_MainWindow["FaderBox_" + str(index)].sy
    width = UI.Elements_MainWindow["FaderBox_" + str(index)].width
    height = UI.Elements_MainWindow["FaderBox_" + str(index)].height
    rl.draw_rectangle_rounded(rl.Rectangle(posx, posy, width, height), 0.5, 4, rl.Color(33, 33, 33, 255))
    rl.draw_text_ex(font, str(index), rl.Vector2(posx, posy+8), 24, 0.5, col.faderNumberFont)
    rl.draw_text_ex(font, text, rl.Vector2(posx+20, posy), 20, 0.5, col.faderFont)

def DrawSelectedChannel(channel):
    if channel.active:
        rl.draw_text_ex(font, channel.name, rl.Vector2(5, 280), 16, 0.5, col.encoderTitle)

def DrawCommandLine(commandline):
    rl.draw_text_ex(font, commandline, rl.Vector2(5, 280), 16, 0.5, col.encoderTitle)
    return

def DrawEncoderSingle(title: str, value: float, color: rl.Color, index: int, active: bool):
    posx = 0
    posy = 0

    if index == 1:
        posx = 2
        posy = 302
    if index == 2:
        posx = 2
        posy = 392
    if index == 3:
        posx = 162
        posy = 302
    if index == 4:
        posx = 162
        posy = 392

    if active and value != -1:
        # rl.draw_rectangle_gradient_v(posx, posy, 156, 86, rl.BLACK, color)
        rl.draw_rectangle(posx, posy, 156, 86, color)
    else:
        rl.draw_rectangle(posx, posy, 156, 86, col.encoderDisabled)


    rl.draw_text_ex(font, title, rl.Vector2((posx+78)-(rl.measure_text_ex(font, title, 24, 0.5).x/2), posy+20), 24, 0.5, col.encoderTitle)
    if value != -1:
        rl.draw_text_ex(font, str(round(value, 2)), rl.Vector2((posx+78)-(rl.measure_text_ex(font, str(round(value, 2)), 24, 0.5).x/2), posy+45), 24, 0.5, col.encoderTitle)

    return

def DrawEncoderDisplay(encoders: EncoderState, activeEncoder: int):
    # rl.draw_rectangle(0, 300, 320, 180, col.encoderBorders)
    #320x180 area, quadrants=(160x90)
    leftActive = False
    rightActive = False
    if activeEncoder == 1:
        leftActive = True
    elif activeEncoder == 2:
        rightActive = True
    
    if activeEncoderPage == EncoderPage.INTENSITY:
        DrawEncoderSingle("Intensity", encoders.Intensity, rl.GRAY, 1, leftActive)
        DrawEncoderSingle("Zoom", encoders.Zoom, rl.GRAY, 3, rightActive)
        DrawEncoderSingle("Focus", encoders.Focus, rl.GRAY, 4, rightActive)

    elif activeEncoderPage == EncoderPage.COLOR_RGB:
        DrawEncoderSingle("Red", encoders.Red, rl.RED, 1, leftActive)
        DrawEncoderSingle("Green", encoders.Green, rl.GREEN, 2, leftActive)
        DrawEncoderSingle("Blue", encoders.Blue, rl.BLUE, 3, rightActive)
        DrawEncoderSingle("White", encoders.White, rl.GRAY, 4, rightActive)

    elif activeEncoderPage == EncoderPage.COLOR_CMY:
        DrawEncoderSingle("Cyan", encoders.Cyan, rl.Color(0, 255, 255, 255), 1, leftActive)
        DrawEncoderSingle("Magenta", encoders.Magenta, rl.MAGENTA, 2, leftActive)
        DrawEncoderSingle("Yellow", encoders.Yellow, rl.YELLOW, 3, rightActive)

    elif activeEncoderPage == EncoderPage.POSITION:
        DrawEncoderSingle("Pan", encoders.Pan, rl.RED, 1, leftActive)
        DrawEncoderSingle("Tilt", encoders.Tilt, rl.BLUE, 2, leftActive)
