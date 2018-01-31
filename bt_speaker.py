#!/usr/bin/python

from gi.repository import GLib
from bt_manager.audio import SBCAudioSink
from bt_manager.media import BTMedia
from bt_manager.device import BTDevice
from bt_manager.agent import BTAgent, BTAgentManager
from bt_manager.adapter import BTAdapter
from bt_manager.serviceuuids import SERVICES
from bt_manager.uuid import BTUUID

import dbus
import dbus.mainloop.glib
import signal
import subprocess
import alsaaudio
import math
import configparser
import io

BTSPEAKER_CONFIG_FILE = '/etc/bt_speaker/config.ini'

# Load config
default_config = u'''
[bt_speaker]
play_command = aplay -f cd -
connect_command = ogg123 /usr/share/sounds/freedesktop/stereo/service-login.oga
disconnect_command = ogg123 /usr/share/sounds/freedesktop/stereo/service-logout.oga

[bluez]
device_path = /org/bluez/hci0

[alsa]
mixer = PCM
id = 0
cardindex = 0
'''

config = configparser.SafeConfigParser()
config.readfp(io.StringIO(default_config))
config.read(BTSPEAKER_CONFIG_FILE)

class PipedSBCAudioSinkWithAlsaVolumeControl(SBCAudioSink):
    """
    An audiosink that pipes the decoded output to a command via stdin.
    The class also sets the volume of an alsadevice
    """
    def __init__(self, path='/endpoint/a2dpsink',
                       command=config.get('bt_speaker', 'play_command'),
                       alsa_control=config.get('alsa', 'mixer'),
                       alsa_id=int(config.get('alsa', 'id')),
                       alsa_cardindex=int(config.get('alsa', 'cardindex')),
                       buf_size=2560):
        SBCAudioSink.__init__(self, path=path)
        # Start process
        self.start_aplay(command,buf_size)
        # Hook into alsa service for volume control
        self.alsamixer = alsaaudio.Mixer(control=alsa_control,
                                         id=alsa_id,
                                         cardindex=alsa_cardindex)

    def start_aplay(self, command, buf_size):
        # Start the aplay process
        self.process = subprocess.Popen(command, shell=True, bufsize=buf_size, stdin=subprocess.PIPE)
        # Store the command and the buf size in case we need to restart aplay at some time
        self.aplay_command = command
        self.aplay_buf_size = buf_size

    def restart_aplay(self):
        # Restart the aplay-process with the same parameters as when it was started
        self.start_aplay(self.aplay_command,self.aplay_buf_size)

    def raw_audio(self, data, retry=False):
        # pipe to the play command
        try:
            self.process.stdin.write(data)
        except IOError as err:
            # This is already a retry. Restarting aplay did not work. Nothing we can do here...
            if retry:
                raise err

            # Probably the aplay-process crashed. Restart it and try again.
            self.restart_aplay()
            self.raw_audio(data,retry=True)

    def volume(self, new_volume):
        # normalize volume
        volume = float(new_volume) / 127.0

        print("Volume changed to %i%%" % (volume * 100.0))

        # it looks like the value passed to alsamixer sets the volume by 'power level'
        # to adjust to the (human) perceived volume, we have to square the volume
        # @todo check if this only applies to the raspberry pi or in general (or if i got it wrong)
        volume = math.pow(volume, 1.0/3.0)

        # alsamixer takes a percent value as integer from 0-100
        self.alsamixer.setvolume(int(volume * 100.0))

class AutoAcceptSingleAudioAgent(BTAgent):
    """
    Accepts one client unconditionally and hides the device once connected.
    As long as the client is connected no other devices may connect.
    This 'first comes first served' is not necessarily the 'bluetooth way' of
    connecting devices but the easiest to implement.
    """
    def __init__(self, connect_callback, disconnect_callback):
        BTAgent.__init__(self, cb_notify_on_authorize=self.auto_accept_one)
        self.adapter = BTAdapter(config.get('bluez', 'device_path'))
        self.allowed_uuids = [ SERVICES["AdvancedAudioDistribution"].uuid, SERVICES["AVRemoteControl"].uuid ]
        self.connected = None
        self.tracked_devices =  []
        self.connect_callback = connect_callback
        self.disconnect_callback = disconnect_callback
        self.update_discoverable()

    def update_discoverable(self):
        if bool(self.connected):
            print("Hiding adapter from all devices.")
            self.adapter.set_property('Discoverable', False)
        else:
            print("Showing adapter to all devices.")
            self.adapter.set_property('Discoverable', True)

    def auto_accept_one(self, method, device, uuid):
        if not BTUUID(uuid).uuid in self.allowed_uuids: return False
        if self.connected and self.connected != device:
            print("Rejecting device, because another one is already connected. connected_device=%s, device=%s" % (self.connected, device))
            return False

        # track connection state of the device (is there a better way?)
        if not device in self.tracked_devices:
            self.tracked_devices.append(device)
            self.adapter._bus.add_signal_receiver(self._track_connection_state,
                                                  path=device,
                                                  signal_name='PropertiesChanged',
                                                  dbus_interface='org.freedesktop.DBus.Properties',
                                                  path_keyword='device')

        return True

    def _track_connection_state(self, addr, properties, signature, device):
        if self.connected and self.connected != device: return
        if not 'Connected' in properties: return

        if not self.connected and bool(properties['Connected']):
            print("Device connected. device=%s" % device)
            self.connected = device
            self.update_discoverable()
            self.connect_callback()

        elif self.connected and not bool(properties['Connected']):
            print("Device disconnected. device=%s" % device)
            self.connected = None
            self.update_discoverable()
            self.disconnect_callback()

def setup_bt():
    # register sink and media endpoint
    sink = PipedSBCAudioSinkWithAlsaVolumeControl()
    media = BTMedia(config.get('bluez', 'device_path'))
    media.register_endpoint(sink._path, sink.get_properties())

    def connect():
        subprocess.Popen(config.get('bt_speaker', 'connect_command'), shell=True)

    def disconnect():
        sink.close_transport()
        subprocess.Popen(config.get('bt_speaker', 'disconnect_command'), shell=True)

    # setup bluetooth agent (that manages connections of devices)
    agent = AutoAcceptSingleAudioAgent(connect, disconnect)
    manager = BTAgentManager()
    manager.register_agent(agent._path, "NoInputNoOutput")
    manager.request_default_agent(agent._path)

def run():
    # Initialize the DBus SystemBus
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    # Mainloop for communication
    mainloop = GLib.MainLoop()

    # catch SIGTERM
    GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGTERM, lambda signal: mainloop.quit(), None)

    # setup bluetooth configuration
    setup_bt()

    # Run
    mainloop.run()

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    except Exception as e:
        print(e.message)
