import asyncio
import serial

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

import surface
import graphics
import handle
import programlogic

from surface import Keys

def oscmap_eos():
    """
    Configures OSC address mappings to the dispatcher.
    """
    dispatcher.set_default_handler(handle.eos_echo_handler, True)
    dispatcher.map("/eos/fader/*", handle.eos_fader_level)
    dispatcher.map("/eos/out/fader/*", handle.eos_fader_name)
    dispatcher.map("/eos/out/active/chan", handle.eos_channel_select)
    dispatcher.map("/eos/out/cmd", handle.eos_command_line)
    dispatcher.map("/eos/out/active/wheel/*", handle.eos_encoder_update)

def oscsetup_eos(client: SimpleUDPClient):
    """
    Sends the neccesary OSC messages required for configuring the console.

    Args:
        client (SimpleUDPClient): The SimpleUDPClient to use for the messages.
    """
    # Configure OSC Fader Bank in EOS (5x faders)
    client.send_message("/eos/fader/1/config/5", 1)
    # Tell EOS we want to receive status updates
    client.send_message("/eos/subscribe", 1)

# Configure target console IP address, port
client = SimpleUDPClient(programlogic.GetConsoleIPAddressString(), 8000)

async def mainloop():
    """
    Main Application Logic function.
    This function is called by init_main() as an async function after
    the OSC server gets set up and the dispatcher gets configured.
    """
    # Send neccesary configuration steps to the console...
    oscsetup_eos(client=client)

    # Initialize window (480x320px)
    graphics.GFXSetup()

    s = serial.Serial("/dev/cu.usbmodem21201", 1000000, timeout=0.01)

    # Main Program Loop - Draw Window - Returns false when Raylib.window_should_close()
    while not graphics.GFXDraw(faders=handle.faders, channel=handle.channel, commandline=handle.commandline, encoders=handle.encoders, activeEncoder=handle.activeEncoder):
        surface.handle(client, s.readline())
        programlogic.StateFromClickEvent(graphics.scan())
        await asyncio.sleep(0)

    #Gracefully close program... Do shutdown procedure here.
    return


async def init_main():
    """
    Configures the internal OSC Server to receive messages and route
    to the dispatcher function.

    Also runs the oscsetup_console() functions and
    mainloop() which contains the core program logic.
    """
    oscmap_eos()
    server = AsyncIOOSCUDPServer(("127.0.0.1", 8001), dispatcher, asyncio.get_event_loop())
    transport, protocol = (
        await server.create_serve_endpoint()
    )
    await mainloop()
    transport.close()

# Enable or Disable Verbose OSC output to the terminal.
handle.Init(debug=False)

# Configure our host system's IP Address to match the configuration defined in the ProgramLogic module.
programlogic.InitializeIPAddressConfig() #TODO: Need to make this actually do something...

# Create Dispatcher object outside of any functions so it is globally accessible
dispatcher = Dispatcher()

# Run the init_main() function
asyncio.run(init_main())