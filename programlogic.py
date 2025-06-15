from enum import Enum

import graphics

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
        return
    return