from __future__ import unicode_literals

import dbus.service
from gi.repository import GObject
import pprint
import os

from device import BTGenericDevice
from media import GenericEndpoint, BTMediaTransport
from codecs import SBCChannelMode, SBCSamplingFrequency, \
    SBCAllocationMethod, SBCSubbands, SBCBlocks, A2DP_CODECS, \
    SBCCodecConfig, SBCCodec
from serviceuuids import SERVICES
from exceptions import BTIncompatibleTransportAccessType, \
    BTInvalidConfiguration


class BTAudio(BTGenericDevice):
    """
    Wrapper around dbus to encapsulate the org.bluez.Audio
    interface.

    :Properties:

    * **State(str) [readonly]**: Possible values: "disconnected",
        "connecting", "connected" with possible state transitions:

      * "disconnected" -> "connecting"
        Either an incoming or outgoing connection attempt
        ongoing.
      * "connecting" -> "disconnected"
        Connection attempt failed
      * "connecting" -> "connected"
        Successfully connected
      * "connected" -> "disconnected"
        Disconnected from the remote device

    See also: :py:class:`.BTGenericDevice` for setup params.
    """
    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Audio',
                                 *args, **kwargs)

    def connect(self):
        """
        Connect all supported audio profiles on the device.

        :return:

        .. note:: This may invoke any registered media
            endpoints where media profiles are compatible.
        """
        return self._interface.Connect()

    def disconnect(self):
        """
        Disconnect all audio profiles on the device

        :return:

        .. note:: This may release any registered media
            endpoints where media profiles are compatible.
        """
        return self._interface.Disconnect()


class BTAudioSource(BTAudio):
    """
    Wrapper around dbus to encapsulate the org.bluez.AudioSource
    interface.

    See also: :py:class:`.BTAudio`
    """
    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.AudioSource',
                                 *args, **kwargs)


class BTAudioSink(BTAudio):
    """
    Wrapper around dbus to encapsulate the org.bluez.AudioSink
    interface

    * **Connected(boolean) [readonly]**: Indicates if a stream is
        setup to a A2DP sink on the remote device.
    * **Playing(boolean) [readonly]**: Indicates if a stream is
        active to a A2DP sink on the remote device.

    See also: :py:class:`.BTAudio`
    """

    SIGNAL_CONNECTED = 'Connected'
    """
    :signal Connected(signal_name, user_arg): Sent when a successful
        connection has been made to the remote A2DP Sink
    """
    SIGNAL_DISCONNECTED = 'Disconnected'
    """
    :signal Disconnected(signal_name, user_arg): Sent when the device has
        been disconnected from.
    """
    SIGNAL_PLAYING = 'Playing'
    """
    :signal Playing(signal_name, user_arg): Sent when a stream
        with remote device is started.
    """
    SIGNAL_STOPPED = 'Stopped'
    """
    :signal Stopped(signal_name, user_arg): Sent when a stream with
        remote device is suspended.
    """

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.AudioSink',
                                 *args, **kwargs)
        self._register_signal_name(BTAudioSink.SIGNAL_CONNECTED)
        self._register_signal_name(BTAudioSink.SIGNAL_DISCONNECTED)
        self._register_signal_name(BTAudioSink.SIGNAL_PLAYING)
        self._register_signal_name(BTAudioSink.SIGNAL_STOPPED)

    def is_connected(self):
        """
        Returns `True` if a stream is setup to a A2DP sink on
        the remote device, `False` otherwise.

        :return Connected: state of `Connected` attribute
        :rtype: boolean
        """
        return self._interface.IsConnected()


class SBCAudioCodec(GenericEndpoint):
    """
    SBCAudioCodec is an implementation of a media endpoint that
    provides common functionality enabling SBC audio source and
    SBC audio sink media endpoints to be established.

    Since certain procedures are specific to whether or not
    the endpoint is a source or sink, in particular the trigger
    points for when the media transport is acquired/release,
    these parts are left to their respective sub-classes.

    SBCAudioCodec handles the following steps in establishing
    an endpoint:

    * Populates `properties` with the capabilities of the codec.
    * `SelectConfiguration`: computes and returns best SBC codec
        configuration parameters based on device capabilities
    * `SetConfiguration`: a sub-class notifier function is called
    * `ClearConfiguration`: nothing is done
    * `Release`: nothing

    In additional to endpoint establishment, the class also has
    transport read and write functions which will handle the
    required SBC media encoding/decoding and RTP encapsulation.

    The user may also register for `transport ready` events
    which allows transport read and write operations to be
    properly synchronized.

    See also: :py:class:`SBCAudioSink` and :py:class:`SBCAudioSource`
    """
    def __init__(self, uuid, path):
        config = SBCCodecConfig(SBCChannelMode.ALL,
                                SBCSamplingFrequency.ALL,
                                SBCAllocationMethod.ALL,
                                SBCSubbands.ALL,
                                SBCBlocks.ALL,
                                2,
                                64)
        caps = SBCAudioCodec._make_config(config)
        codec = dbus.Byte(A2DP_CODECS['SBC'])
        delayed_reporting = dbus.Boolean(True)
        self.tag = None
        self.path = None
        self.user_cb = None
        self.user_arg = None
        self.properties = dbus.Dictionary({'UUID': uuid,
                                           'Codec': codec,
                                           'DelayReporting': delayed_reporting,
                                           'Capabilities': caps})
        GenericEndpoint.__init__(self, path)

    def _transport_ready_handler(self, fd, cb_condition):
        """
        Wrapper for calling user callback routine to notify
        when transport data is ready to read
        """
        if(self.user_cb):
            self.user_cb(self.user_arg)
        return True

    def _install_transport_ready(self):
        if ('r' in self.access_type):
            io_event = GObject.IO_IN
        else:
            io_event = GObject.IO_OUT

        self.tag = GObject.io_add_watch(self.fd, io_event,
                                        self._transport_ready_handler)

    def _uninstall_transport_ready(self):
        if (self.tag):
            GObject.source_remove(self.tag)
            self.tag = None

    def register_transport_ready_event(self, user_cb, user_arg):
        """
        Register for transport ready events.  The `transport ready`
        event is raised via a user callback.  If the endpoint
        is configured as a source, then the user may then
        call :py:meth:`write_transport` in order to send data to
        the associated sink.
        Otherwise, if the endpoint is configured as a sink, then
        the user may call :py:meth:`read_transport` to read
        from the associated source instead.

        :param func user_cb: User defined callback function.  It
            must take one parameter which is the user's callback
            argument.
        :param user_arg: User defined callback argument.
        :return:

        See also: :py:meth:`unregister_transport_ready_event`
        """
        self.user_cb = user_cb
        self.user_arg = user_arg

    def unregister_transport_ready_event(self):
        """
        Unregister previously registered `transport ready`
        events.

        See also: :py:meth:`register_transport_ready_event`
        """
        self.user_cb = None

    def read_transport(self):
        """
        Read data from media transport.
        The returned data payload is SBC decoded and has
        all RTP encapsulation removed.

        :return data: Payload data that has been decoded,
            with RTP encapsulation removed.
        :rtype: array{byte}
        """
        if ('r' not in self.access_type):
            raise BTIncompatibleTransportAccessType
        return self.codec.decode(self.fd, self.read_mtu)

    def write_transport(self, data):
        """
        Write data to media transport.  The data is
        encoded using the SBC codec and RTP encapsulated
        before being written to the transport file
        descriptor.

        :param array{byte} data: Payload data to encode,
            encapsulate and send.
        """
        if ('w' not in self.access_type):
            raise BTIncompatibleTransportAccessType
        return self.codec.encode(self.fd, self.write_mtu, data)

    def close_transport(self):
        """
        Forcibly close previously acquired media transport.

        .. note:: The user should first make sure any transport
            event handlers are unregistered first.
        """
        if (self.path):
            self._release_media_transport(self.path,
                                          self.access_type)
            self.path = None

    def _notify_media_transport_available(self, path, transport):
        """
        Subclass should implement this to trigger setup once
        a new media transport is available.
        """
        pass

    def _acquire_media_transport(self, path, access_type):
        """
        Should be called by subclass when it is ready
        to acquire the media transport file descriptor
        """
        transport = BTMediaTransport(path=path)
        (fd, read_mtu, write_mtu) = transport.acquire(access_type)
        print("Aquired MediaTransport. fd=%s read_mtu=%i write_mtu=%i" % (fd, read_mtu, write_mtu))
        self.fd = fd.take()   # We must do the clean-up later
        self.write_mtu = write_mtu
        self.read_mtu = read_mtu
        self.access_type = access_type
        self.path = path
        self._install_transport_ready()

    def _release_media_transport(self, path, access_type):
        """
        Should be called by subclass when it is finished
        with the media transport file descriptor
        """
        try:
            self._uninstall_transport_ready()
            print("Released MediaTransport. fd=%s" % (self.fd))
            os.close(self.fd)   # Clean-up previously taken fd
            self.fd = None
            transport = BTMediaTransport(path=path)
            transport.release(access_type)
        except:
            pass

    @staticmethod
    def _default_bitpool(frequency, channel_mode):
        if (frequency ==
                SBCSamplingFrequency.FREQ_16KHZ or
            frequency ==
                SBCSamplingFrequency.FREQ_32KHZ):
            return 53
        elif (frequency ==
                SBCSamplingFrequency.FREQ_44_1KHZ):
            if (channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_MONO or
                channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_DUAL):
                return 31
            elif (channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_STEREO or
                  channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_JOINT_STEREO):
                return 53
            else:
                # TODO: Invalid channel_mode
                return 53
        elif (frequency == SBCSamplingFrequency.FREQ_48KHZ):
            if (channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_MONO or
                channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_DUAL):
                return 29
            elif (channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_STEREO or
                  channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_JOINT_STEREO):
                return 51
            else:
                # TODO: Invalid channel_mode
                return 51
        else:
            # TODO: Invalid frequency
            return 53

    @staticmethod
    def _make_config(config):
        """Helper to turn SBC codec configuration params into a
        a2dp_sbc_t structure usable by bluez"""
        # The SBC config encoding is taken from a2dp_codecs.h, in particular,
        # the a2dp_sbc_t type is converted into a 4-byte array:
        #   uint8_t channel_mode:4
        #   uint8_t frequency:4
        #   uint8_t allocation_method:2
        #   uint8_t subbands:2
        #   uint8_t block_length:4
        #   uint8_t min_bitpool
        #   uint8_t max_bitpool
        return dbus.Array([dbus.Byte(config.channel_mode |
                                     (config.frequency << 4)),
                           dbus.Byte(config.allocation_method |
                                     (config.subbands << 2) |
                                     (config.block_length << 4)),
                           dbus.Byte(config.min_bitpool),
                           dbus.Byte(config.max_bitpool)])

    @staticmethod
    def _parse_config(config):
        """Helper to turn a2dp_sbc_t structure into a
        more usable set of SBC codec configuration params"""
        frequency = config[0] >> 4
        channel_mode = config[0] & 0xF
        allocation_method = config[1] & 0x03
        subbands = (config[1] >> 2) & 0x03
        block_length = (config[1] >> 4) & 0x0F
        min_bitpool = config[2]
        max_bitpool = config[3]
        return SBCCodecConfig(channel_mode, frequency, allocation_method,
                              subbands, block_length, min_bitpool, max_bitpool)

    @dbus.service.method("org.bluez.MediaEndpoint1",
                         in_signature="", out_signature="")
    def Release(self):
        pass

    @dbus.service.method("org.bluez.MediaEndpoint1",
                         in_signature="", out_signature="")
    def ClearConfiguration(self):
        pass

    @dbus.service.method("org.bluez.MediaEndpoint1",
                         in_signature="ay", out_signature="ay")
    def SelectConfiguration(self, caps):
        our_caps = SBCAudioCodec._parse_config(self.properties['Capabilities'])
        device_caps = SBCAudioCodec._parse_config(caps)
        frequency = SBCSamplingFrequency.FREQ_44_1KHZ

        if ((our_caps.channel_mode & device_caps.channel_mode) &
                SBCChannelMode.CHANNEL_MODE_JOINT_STEREO):
            channel_mode = SBCChannelMode.CHANNEL_MODE_JOINT_STEREO
        elif ((our_caps.channel_mode & device_caps.channel_mode) &
              SBCChannelMode.CHANNEL_MODE_STEREO):
            channel_mode = SBCChannelMode.CHANNEL_MODE_STEREO
        elif ((our_caps.channel_mode & device_caps.channel_mode) &
              SBCChannelMode.CHANNEL_MODE_DUAL):
            channel_mode = SBCChannelMode.CHANNEL_MODE_DUAL
        elif ((our_caps.channel_mode & device_caps.channel_mode) &
              SBCChannelMode.CHANNEL_MODE_MONO):
            channel_mode = SBCChannelMode.CHANNEL_MODE_MONO
        else:
            raise BTInvalidConfiguration

        if ((our_caps.block_length & device_caps.block_length) &
                SBCBlocks.BLOCKS_16):
            block_length = SBCBlocks.BLOCKS_16
        elif ((our_caps.block_length & device_caps.block_length) &
              SBCBlocks.BLOCKS_12):
            block_length = SBCBlocks.BLOCKS_12
        elif ((our_caps.block_length & device_caps.block_length) &
              SBCBlocks.BLOCKS_8):
            block_length = SBCBlocks.BLOCKS_8
        elif ((our_caps.block_length & device_caps.block_length) &
              SBCBlocks.BLOCKS_4):
            block_length = SBCBlocks.BLOCKS_4
        else:
            raise BTInvalidConfiguration

        if ((our_caps.subbands & device_caps.subbands) &
                SBCSubbands.SUBBANDS_8):
            subbands = SBCSubbands.SUBBANDS_8
        elif ((our_caps.subbands & device_caps.subbands) &
              SBCSubbands.SUBBANDS_4):
            subbands = SBCSubbands.SUBBANDS_4
        else:
            raise BTInvalidConfiguration

        if ((our_caps.allocation_method & device_caps.allocation_method) &
                SBCAllocationMethod.LOUDNESS):
            allocation_method = SBCAllocationMethod.LOUDNESS
        elif ((our_caps.allocation_method & device_caps.allocation_method) &
              SBCAllocationMethod.SNR):
            allocation_method = SBCAllocationMethod.SNR
        else:
            raise BTInvalidConfiguration

        min_bitpool = max(our_caps.min_bitpool, device_caps.min_bitpool)
        max_bitpool = min(SBCAudioCodec._default_bitpool(frequency,
                                                         channel_mode),
                          device_caps.max_bitpool)

        selected_config = SBCCodecConfig(channel_mode,
                                         frequency,
                                         allocation_method,
                                         subbands,
                                         block_length,
                                         min_bitpool,
                                         max_bitpool)

        # Create SBC codec based on selected configuration
        self.codec = SBCCodec(selected_config)

        dbus_val = SBCAudioCodec._make_config(selected_config)
        return dbus_val

    @dbus.service.method("org.bluez.MediaEndpoint1",
                         in_signature="oay", out_signature="")
    def SetConfiguration(self, transport, config):
        self.SelectConfiguration(config['Configuration'])
        self._notify_media_transport_available(config.get('Device'), transport)

    def __repr__(self):
        return pprint.pformat(self.__dict__)


class SBCAudioSink(SBCAudioCodec):
    """
    SBC audio sink media endpoint

    SBCAudioSink implies the BT adapter takes on the role of
    a sink and the external device is the source e.g.,
    iPhone, media player.

    Refer to :py:class:`SBCAudioCodec` for basic overview of
    endpoint steps
    """
    def __init__(self,
                 path='/endpoint/a2dpsink'):
        uuid = dbus.String(SERVICES['AudioSink'].uuid)
        SBCAudioCodec.__init__(self, uuid, path)
        self.register_transport_ready_event(self._process_decoded, ())

    def _property_change_event_handler(self, signal, transport, *args):
        """
        Handler for property change event.  We catch certain state
        transitions in order to trigger media transport
        acquisition/release
        """
        new_properties = args[1]

        for k in new_properties.keys():
            if k == 'State':
                self._state_changed(new_properties[k], transport)
            elif k == 'Volume':
                self.volume(new_properties[k])

    def _state_changed(self, new_state, transport):
        if (self.state == 'idle' and new_state == 'pending'):
            self._acquire_media_transport(transport, 'r')
            self.start()
        elif (self.state == 'active' and new_state == 'idle'):
            self._release_media_transport(transport, 'r')
            self.stop()

        print("State changed from %s to %s." % (self.state, new_state))

        self.state = new_state

    def _notify_media_transport_available(self, path, transport):
        """
        Called by the endpoint when a new media transport is
        available
        """
        print("Transport available! transport=%s" % transport)
        self.source = BTMediaTransport(transport)
        self.state = 'idle'
        self.source.add_signal_receiver(self._property_change_event_handler,
                                        BTAudioSource.SIGNAL_PROPERTY_CHANGED,  # noqa
                                        transport)

    def _process_decoded(self, args):
        self.raw_audio(self.read_transport())

    def raw_audio(self, data):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def volume(self, new_volume):
        pass


class SBCAudioSource(SBCAudioCodec):
    """
    SBC audio source media endpoint.

    SBCAudioSource implies the adapter takes on the role of
    source and the external device is the sink e.g., speaker.

    Refer to :py:class:`SBCAudioCodec` for basic overview of
    endpoint steps
    """
    def __init__(self,
                 path='/endpoint/a2dpsource'):
        uuid = dbus.String(SERVICES['AudioSource'].uuid)
        SBCAudioCodec.__init__(self, uuid, path)

    def _property_change_event_handler(self, signal, transport, *args):
        """
        Handler for property change event.  We catch certain state
        transitions in order to trigger media transport
        acquisition/release
        """
        current_state = self.sink.State
        if ((self.state == 'disconnected' and current_state == 'connected') or
            (self.state == 'connecting' and
                current_state == 'connected')):
            self._acquire_media_transport(transport, 'w')
        elif (self.state == 'connected' and current_state == 'disconnected'):
            self._release_media_transport(transport, 'w')
        self.state = current_state

    def _notify_media_transport_available(self, path, transport):
        """
        Called by the endpoint when a new media transport is
        available
        """
        self.sink = BTAudioSink(dev_path=path)
        self.state = self.sink.State
        self.sink.add_signal_receiver(self._property_change_event_handler,
                                      BTAudioSource.SIGNAL_PROPERTY_CHANGED,  # noqa
                                      transport)
