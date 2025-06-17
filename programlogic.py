from enum import Enum

import graphics
import handle

class State(Enum):
    MAIN = 0
    MENU = 1

ProgramState = State.MAIN

MyIPAddress = [127, 0, 0, 1]
ConsoleIPAddress = [127, 0, 0, 1]

def InitializeIPAddressConfig():
    return

def GetMyIPAddress():
    return MyIPAddress

def GetConsoleIPAddress():
    return ConsoleIPAddress

def GetConsoleIPAddressString():
    return str(ConsoleIPAddress[0]) + "." + str(ConsoleIPAddress[1]) + "." + str(ConsoleIPAddress[2]) + "." + str(ConsoleIPAddress[3])

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
        elif element == "MyIP_1_Up":
            if MyIPAddress[0] < 255:
                MyIPAddress[0] = MyIPAddress[0] + 1
            else:
                MyIPAddress[0] = 0
        elif element == "MyIP_1_Down":
            if MyIPAddress[0] > 0:
                MyIPAddress[0] = MyIPAddress[0] - 1
            else:
                MyIPAddress[0] = 255
        elif element == "MyIP_1_Center":
            if MyIPAddress[0] >= 200:
                MyIPAddress[0] = 0
            else:
                MyIPAddress[0] = MyIPAddress[0] + 100
        elif element == "MyIP_2_Up":
            if MyIPAddress[1] < 255:
                MyIPAddress[1] = MyIPAddress[1] + 1
            else:
                MyIPAddress[1] = 0
        elif element == "MyIP_2_Down":
            if MyIPAddress[1] > 0:
                MyIPAddress[1] = MyIPAddress[1] - 1
            else:
                MyIPAddress[1] = 255
        elif element == "MyIP_2_Center":
            if MyIPAddress[1] >= 200:
                MyIPAddress[1] = 0
            else:
                MyIPAddress[1] = MyIPAddress[1] + 100
        elif element == "MyIP_3_Up":
            if MyIPAddress[2] < 255:
                MyIPAddress[2] = MyIPAddress[2] + 1
            else:
                MyIPAddress[2] = 0
        elif element == "MyIP_3_Down":
            if MyIPAddress[2] > 0:
                MyIPAddress[2] = MyIPAddress[2] - 1
            else:
                MyIPAddress[2] = 255
        elif element == "MyIP_3_Center":
            if MyIPAddress[2] >= 200:
                MyIPAddress[2] = 0
            else:
                MyIPAddress[2] = MyIPAddress[2] + 100
        elif element == "MyIP_4_Up":
            if MyIPAddress[3] < 255:
                MyIPAddress[3] = MyIPAddress[3] + 1
            else:
                MyIPAddress[3] = 0
        elif element == "MyIP_4_Down":
            if MyIPAddress[3] > 0:
                MyIPAddress[3] = MyIPAddress[3] - 1
            else:
                MyIPAddress[3] = 255
        elif element == "MyIP_4_Center":
            if MyIPAddress[3] >= 200:
                MyIPAddress[3] = 0
            else:
                MyIPAddress[3] = MyIPAddress[3] + 100
        elif element == "ConsoleIP_1_Up":
            if ConsoleIPAddress[0] < 255:
                ConsoleIPAddress[0] = ConsoleIPAddress[0] + 1
            else:
                ConsoleIPAddress[0] = 0
        elif element == "ConsoleIP_1_Down":
            if ConsoleIPAddress[0] > 0:
                ConsoleIPAddress[0] = ConsoleIPAddress[0] - 1
            else:
                ConsoleIPAddress[0] = 255
        elif element == "ConsoleIP_1_Center":
            if ConsoleIPAddress[0] >= 200:
                ConsoleIPAddress[0] = 0
            else:
                ConsoleIPAddress[0] = ConsoleIPAddress[0] + 100
        elif element == "ConsoleIP_2_Up":
            if ConsoleIPAddress[1] < 255:
                ConsoleIPAddress[1] = ConsoleIPAddress[1] + 1
            else:
                ConsoleIPAddress[1] = 0
        elif element == "ConsoleIP_2_Down":
            if ConsoleIPAddress[1] > 0:
                ConsoleIPAddress[1] = ConsoleIPAddress[1] - 1
            else:
                ConsoleIPAddress[1] = 255
        elif element == "ConsoleIP_2_Center":
            if ConsoleIPAddress[1] >= 200:
                ConsoleIPAddress[1] = 0
            else:
                ConsoleIPAddress[1] = ConsoleIPAddress[1] + 100
        elif element == "ConsoleIP_3_Up":
            if ConsoleIPAddress[2] < 255:
                ConsoleIPAddress[2] = ConsoleIPAddress[2] + 1
            else:
                ConsoleIPAddress[2] = 0
        elif element == "ConsoleIP_3_Down":
            if ConsoleIPAddress[2] > 0:
                ConsoleIPAddress[2] = ConsoleIPAddress[2] - 1
            else:
                ConsoleIPAddress[2] = 255
        elif element == "ConsoleIP_3_Center":
            if ConsoleIPAddress[2] >= 200:
                ConsoleIPAddress[2] = 0
            else:
                ConsoleIPAddress[2] = ConsoleIPAddress[2] + 100
        elif element == "ConsoleIP_4_Up":
            if ConsoleIPAddress[3] < 255:
                ConsoleIPAddress[3] = ConsoleIPAddress[3] + 1
            else:
                ConsoleIPAddress[3] = 0
        elif element == "ConsoleIP_4_Down":
            if ConsoleIPAddress[3] > 0:
                ConsoleIPAddress[3] = ConsoleIPAddress[3] - 1
            else:
                ConsoleIPAddress[3] = 255
        elif element == "ConsoleIP_4_Center":
            if ConsoleIPAddress[3] >= 200:
                ConsoleIPAddress[3] = 0
            else:
                ConsoleIPAddress[3] = ConsoleIPAddress[3] + 100
    return