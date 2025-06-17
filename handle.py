dbg = False

class SelectedChannel():
    name = ""
    active = False

class EncoderState():
    Intensity = -1
    Red = -1
    Green = -1
    Blue = -1
    White = -1
    Cyan = -1
    Magenta = -1
    Yellow = -1
    Zoom = -1
    Focus = -1
    Pan = -1
    Tilt = -1

#########################
## PROGSTATE VARIABLES ##
#########################
faders = [[0, "fader1"], [0, "fader2"], [0, "fader3"], [0, "fader4"], [0, "fader5"]]
channel = SelectedChannel()
commandline = ""
encoders = EncoderState()
activeEncoder = 1 #1=Left, 2=Right

def SetActiveEncoder(e: int):
    global activeEncoder
    activeEncoder = e
    
def Init(debug=False):
    global dbg
    dbg = debug
    return

def echo_handler(client_addr, unused_addr, *args):
    if dbg:
        print("")
        print("Got unhandled OSC message...")
        print(f"{unused_addr}: {args}")
        print("")
    return

def fader_name(address, *args):
    if dbg:
        print(f"{address}: {args}")
    if len(address.split("/")) > 5:
        bank = address.split("/")[4]
        fader = address.split("/")[5]
        name = args[0]
        if address.split("/")[6] == "name":
            faders[int(fader)-1][1] = name
    return

def fader_level(address, *args):
    if dbg:
        print(f"{address}: {args}")
    bank = address.split("/")[3]
    fader = address.split("/")[4]
    fader1pos = args[0]
    faders[int(fader)-1][0] = args[0]
    return

def channel_select(address, *args):
    global channel
    global encoders
    if args[0] == '':
        channel = SelectedChannel()
        encoders = EncoderState()
    else:
        channel.active = True
        channel.name = args[0]
        encoders = EncoderState()
    return

def encoder_update(address, *args):
    print(args)
    WheelType = args[0].split("  ")[0]
    if WheelType == "Intens":
        encoders.Intensity = float(args[2])
    elif WheelType == "Red":
        encoders.Red = float(args[2])
    elif WheelType == "Green":
        encoders.Green = float(args[2])
    elif WheelType == "Blue":
        encoders.Blue = float(args[2])
    elif WheelType == "White":
        encoders.White = float(args[2])
    elif WheelType == "Cyan":
        encoders.Cyan = float(args[2])
    elif WheelType == "Magenta":
        encoders.Magenta = float(args[2])
    elif WheelType == "Yellow":
        encoders.Yellow = float(args[2])
    elif WheelType == "Zoom":
        encoders.Zoom = float(args[2])
    elif WheelType == "Edge":
        encoders.Focus = float(args[2])
    elif WheelType == "Pan":
        encoders.Pan = float(args[2])
    elif WheelType == "Tilt":
        encoders.Tilt = float(args[2])
    return

def command_line(address, *args):
    global commandline
    commandline = str(args[0])
    return
