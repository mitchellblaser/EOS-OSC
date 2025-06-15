import asyncio

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

import surface
import graphics
import handle
import programlogic

from surface import Keys

handle.Init(debug=True)

dispatcher = Dispatcher()
dispatcher.set_default_handler(handle.echo_handler, True)
dispatcher.map("/eos/fader/*", handle.fader_level)
dispatcher.map("/eos/out/fader/*", handle.fader_name)
dispatcher.map("/eos/out/active/chan", handle.channel_select)
dispatcher.map("/eos/out/cmd", handle.command_line)
dispatcher.map("/eos/out/active/wheel/*", handle.encoder_update)

## TODO: Encoder Control and OSC Output
## TODO: Continue sending osc init messages until we receive a ping in response
## TODO: Add Keyboard input and translate to OSC for EOS key control
## TODO: IP Address configuration from setup menu
## TODO: Serial Input from Surface
## TODO: Do we need to support both CMY and RGB??

## Main Thread, Initial setup, then Loop.
async def mainloop():
    # Configure target console IP address, port
    client = SimpleUDPClient("127.0.0.1", 8000)
    
    # Configure OSC Fader Bank in EOS (5x faders)
    client.send_message("/eos/fader/1/config/5", 1)

    # Tell EOS we want to receive status updates
    client.send_message("/eos/subscribe", 1)

    # Initialize window (480x320px)
    graphics.GFXSetup()

    # Main Program Loop - Draw Window - Returns false when Raylib.window_should_close()
    while not graphics.GFXDraw(faders=handle.faders, channel=handle.channel, commandline=handle.commandline, encoders=handle.encoders, activeEncoder=handle.activeEncoder):
        programlogic.StateFromClickEvent(graphics.scan())
        surface.handle()
        await asyncio.sleep(0)

    #Gracefully close program... Do shutdown procedure here.
    return


# Configure the OSC server to send any incoming messages to the Dispatcher.
async def init_main():
    server = AsyncIOOSCUDPServer(("127.0.0.1", 8001), dispatcher, asyncio.get_event_loop())
    transport, protocol = (
        await server.create_serve_endpoint()
    )
    await mainloop()
    transport.close()

asyncio.run(init_main())