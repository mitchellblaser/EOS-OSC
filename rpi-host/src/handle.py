dbg = False

def debug(message):
    """
    Takes a message and passes it to Python's print() function
    provided the debug flag has been set to True.

    Args:
        message: The message to print in debug mode.

    Returns:
        bool: The state of the Debug flag.
    """
    if dbg:
        print(message)
    return dbg

class SelectedChannel():
    """
    Holds all information about the currently selected
    console channel in one container.
    """
    name = ""
    active = False

class EncoderState():
    """
    Holds the current state of all possible encoders that
    can be accessed via the surface/GUI as an integer.

    If the number is a [-1], then the encoder is not available
    for the currently selected channel.
    
    If the number is [>0] then the encoder is treated as active.
    """
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

#############################
## PROGRAM STATE VARIABLES ##
#############################
faders = [[0, "fader1"], [0, "fader2"], [0, "fader3"], [0, "fader4"], [0, "fader5"]]
channel = SelectedChannel()
commandline = ""
encoders = EncoderState()
activeEncoder = 1 #1=Left, 2=Right

def Init(debug=False):
    """
    Called on program initialization, set up any local variables etc.

    Args:
        debug (bool): Whether or not to output debug messages to the terminal.
    """
    global dbg
    dbg = debug
    return
    
def SetActiveEncoder(e: int):
    """
    Define whether the left or right side of the encoder display
    is currently active.

    Args:
        e (int): The encoder side, 1=Left, 2=Right.
    """
    global activeEncoder
    activeEncoder = e

def eos_echo_handler(address, *args):
    """
    Called on unhandled OSC message, falls back to printing
    output to the terminal (provided debug flag is true).

    Args:
        address (str): The source address of the OSC message.
        *args: Arguments from the OSC message
    """
    if dbg:
        print("")
        print("Got unhandled OSC message...")
        print(f"{address}: {args}")
        print("")
    return

def eos_fader_name(address, *args):
    """
    Extracts the Fader Name from an /eos/out/fader message.

    Args:
        address (str): The source address of the OSC message.
        *args: Arguments from the OSC message
    """
    debug(f"{address}: {args}")
    if len(address.split("/")) > 5:
        bank = address.split("/")[4]
        fader = address.split("/")[5]
        name = args[0]
        if address.split("/")[6] == "name":
            faders[int(fader)-1][1] = name
    return

def eos_fader_level(address, *args):
    """
    Extracts the Fader Level from an /eos/fader message.

    Args:
        address (str): The source address of the OSC message.
        *args: Arguments from the OSC message
    """
    debug(f"{address}: {args}")
    bank = address.split("/")[3]
    fader = address.split("/")[4]
    fader1pos = args[0]
    faders[int(fader)-1][0] = args[0]
    return

def eos_channel_select(address, *args):
    """
    Determines whether or not there is a currently selected
    channel in the console, and modifys the channel (SelectedChannel)
    variable accordingly.

    Args:
        address (str): The source address of the OSC message.
        *args: Arguments from the OSC message
    """
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

def eos_encoder_update(address, *args):
    """
    Extracts any encoder values (at least, the ones we care about)
    from an /eos/out/active/wheel/* message and stores to the
    encoder (EncoderState) variable.

    Args:
        address (str): The source address of the OSC message.
        *args: Arguments from the OSC message
    """
    debug(args)
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

def eos_command_line(address, *args):
    """
    Extracts the current commandline message and stores it to
    the commandline variable.

    Args:
        address (str): The source address of the OSC message.
        *args: Arguments from the OSC message
    """
    global commandline
    commandline = str(args[0])
    return
