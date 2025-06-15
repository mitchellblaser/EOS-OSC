from enum import Enum

import graphics
import handle

class State(Enum):
    MAIN = 0
    MENU = 1

ProgramState = State.MAIN

def StateFromClickEvent(element):
    global ProgramState
    if element is not None:
        if element == "Toolbar_Menu":
            ProgramState = State.MENU
            graphics.GFXSetState(ProgramState)
        elif element == "Toolbar_Menu_Exit":
            ProgramState = State.MAIN
            graphics.GFXSetState(ProgramState)
        elif element == "Encoder_1" or element == "Encoder_2":
            handle.SetActiveEncoder(1)
        elif element == "Encoder_3" or element == "Encoder_4":
            handle.SetActiveEncoder(2)
        return
    return