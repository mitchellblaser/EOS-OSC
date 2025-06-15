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

#########################
## PROGSTATE VARIABLES ##
#########################
faders = [[0, "fader1"], [0, "fader2"], [0, "fader3"], [0, "fader4"], [0, "fader5"]]
channel = SelectedChannel()
commandline = ""
encoders = EncoderState()
activeEncoder = 1 #1=Left, 2=Right

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
    return

def command_line(address, *args):
    global commandline
    commandline = str(args[0])
    return

#/eos/out/active/chan: ('',)
#/eos/out/active/wheel/1: ('  [0]', 0, 0.0)

# /eos/out/active/chan: ('1  [0] Custom Saturn_300_Wash',) 
# /eos/out/active/wheel/1: ('Intens  [0]', 1, 0.0)
# /eos/out/active/wheel/2: ('Pan  [80]', 2, 80.0)
# /eos/out/active/wheel/3: ('Tilt  [-47]', 2, -47.400001525878906)
# /eos/out/active/wheel/4: ('X Focus  [-3]', 2, -2.8993000984191895)
# /eos/out/active/wheel/5: ('Y Focus  [-1]', 2, -0.5112000107765198)
# /eos/out/active/wheel/6: ('Z Focus  [7]', 2, 6.707200050354004)
# /eos/out/active/wheel/7: ('Position MSpeed  [100]', 2, 100.0)
# /eos/out/active/wheel/8: ('Red  [30]', 3, 30.0)
# /eos/out/active/wheel/9: ('Green  [10]', 3, 10.0)
# /eos/out/active/wheel/10: ('Blue  [100]', 3, 100.0)
# /eos/out/active/wheel/11: ('White  [100]', 3, 100.0)
# /eos/out/active/wheel/12: ('Hue  [0]', 3, 0.0)
# /eos/out/active/wheel/13: ('Saturation  [0]', 3, 0.0)
# /eos/out/active/wheel/14: ('Color Macros  [0]', 3, 0.0)
# /eos/out/active/wheel/15: ('Color Temperature  [0]', 3, 0.0)
# /eos/out/active/wheel/16: ('Zoom  [5]', 5, 4.5)
# /eos/out/active/wheel/17: ('Shutter Strobe  [0]', 5, 0.0)
# /eos/out/color/hs: (307.3926086425781, 17.399124145507812)
# /eos/out/pantilt: (-270.0, 270.0, -135.0, 135.0, 80.0, -47.400001525878906)
# /eos/out/xyz: (-2.8993000984191895, -0.5112000107765198, 6.707200050354004)