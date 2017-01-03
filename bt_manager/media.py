from __future__ import unicode_literals

from interface import BTSimpleInterface, BTInterface
# from manager import BTManager
# from adapter import BTAdapter
from exceptions import BTDeviceNotSpecifiedException
import dbus.service


class BTMedia(BTSimpleInterface):
    """
    Wrapper around dbus to encapsulate org.bluez.Media
    interface.

    The media interface allows media endpoints to be
    established in accordance with the capabilities
    of a specific media service profile.

    For example, an A2DP media endpoint could be
    created allowing data from a remote device
    to be streamed to/from the sender.

    Each media endpoint is associated with a service
    object instance that implements the required
    behaviours of the endpoint.  The service object
    must be created at a given path before it
    is registered.

    See also: :py:class:`.GenericEndpoint`
    """
    def __init__(self, adapter_path):
        BTSimpleInterface.__init__(self, adapter_path, 'org.bluez.Media1')

    def register_endpoint(self, path, properties):
        """
        Register a local end point to sender, the sender can
        register as many end points as it likes.

        The properties dictionary parameter may take the
        following fields:

        * UUID(str): UUID of the profile which the endpoint is
            for e.g., ``SERVICES['AudioSource']``
        * Codec(byte): Assigned mumber of codec that the
            endpoint implements. The values should match the profile
            specification which is indicated by the UUID
            e.g., ``A2DP_CODECS['SBC']``
        * Capabilities(array{byte}): Capabilities blob, it is used
            as it is so the size and byte order must match.

        See also: :py:data:`.A2DP_CODECS` and :py:data:`.SERVICES`

        If the sender disconnects the end points are
        automatically unregistered.

        :param: str path: a freely definable path name for
            registering the endpoint e.g., '/endpoint/a2dpsource'.
        :param: dict properties: a dictionary defining the
            endpoints properties which may contain.
        :return:
        :raises dbus.Exception: org.bluez.Error.InvalidArguments
        :raises dbus.Exception: org.bluez.Error.NotSupported
        """
        self._interface.RegisterEndpoint(path, properties)

    def unregister_endpoint(self, path):
        """
        Unregister sender end point.

        :param: str path: a freely definable path name previously
            used for registering via :py:meth:`register_endpoint`
        :return:
        """
        self._interface.UnregisterEndpoint(path)


class BTMediaTransport(BTInterface):
    """
    Wrapper around dbus to encapsulate the org.bluez.MediaTransport1
    interface.

    A media transport instance provides a mechanism by which
    data streamed to/from a device can be sent/received via
    the L2 transport.

    This is done by `acquiring` a transport file descriptor
    object which then allows the underlying file to be
    read from or written to.

    When finished, the file descriptor should be closed using
    a normal UNIX **close()** operation before `releasing` the
    media transport back again.

    .. warning:: The media transport interface does not implement
        any CODECs and should be regarded as providing direct
        access to the underlying data transport.

    :param: str path: [Optional] Absolute object path to the
        device's file descriptor node carrying the media transport.
    :param: str dev_path: [Optional] Device's object path.  The
        file descriptor node will be provided via `fd` argument.
    :param: int fd: [Optional] File number for the file descriptor
        node associated with the device given by either `dev_path`
        or `dev_id`
    :param: str adapter_id: [Optional] Adapter identifier from
        which to look-up the `dev_id`
    :param: str dev_id: [Optional] Device identifier of the form
        e.g., '11:22:33:44:55:66'.
    :raises BTDeviceNotSpecifiedException: if the device path could
        not be determined unambiguously from the supplied parameters.

    :Properties:

    * **Device(str) [readonly]**: Device object which the transport
        is connected to.
    * **UUID(str) [readonly]**: UUID of the profile which the
        transport is for.
    * **Codec(byte) [readonly]**: Assigned mumber of codec that the
        transport support.  The value should match the profile
        specification which is indicated by the UUID.
    * **Configuration(byte) [readonly]**: Configuration blob, it is
        used as it is so the size and byte order must match.
    * **Delay(uint16) [readwrite]**: Optional. Transport delay in
            1/10 of milisecond, this property is only writeable when
            the transport was acquired by the sender.
    * **NREC(boolean) [readwrite]**: Optional. Indicates if echo
        cancelling and noise reduction functions are active in the
        transport, this property is only writeable when the transport
        was acquired by the sender.
    * **InbandRingtone(boolean) [readwrite]**: Optional. Indicates
        if the transport support sending ringtones, this property
        is only writeable when the transport was acquired by the
        sender.
    * **Routing(str) [readonly]**: Optional. Indicates where is the
        transport being routed and may be 'HCI' or 'PCM'.
    """
    def __init__(self, path, fd=None, adapter_id=None,
                 dev_path=None, dev_id=None):
        if (not path):
            fd_suffix = '/fd' + str(fd)
            if (dev_path):
                path = dev_path + fd_suffix
            elif (dev_id):
                if (adapter_id):
                    adapter = BTAdapter(adapter_id)
                else:
                    adapter = BTAdapter()
                    path = adapter.find_device(dev_id) + fd_suffix
            else:
                raise BTDeviceNotSpecifiedException
        BTInterface.__init__(self, path, 'org.bluez.MediaTransport1')

    def acquire(self, access_type):
        """
        Acquire transport file descriptor and the MTU for read
        and/or write respectively.  Possible access_type:

        * "r" : Read only access
        * "w" : Write only access
        * "rw": Read and write access

        :param str access_type: as defined above.
        :return: A tuple of the form (fd, write_mtu, read_mtu)
        :rtype: tuple
        """
        return self._interface.Acquire(access_type)

    def release(self, access_type):
        """
        Releases file descriptor.

        Possible access_type:

        * "r" : Read only access
        * "w" : Write only access
        * "rw": Read and write access

        :param str access_type: as defined above.
        """
        return self._interface.Release(access_type)


class GenericEndpoint(dbus.service.Object):
    """
    Generic media endpoint service object class.

    .. note:: GenericEndpoint can't be directly instantiated.
        It should be sub-classed and provides a template for
        implementing an endpoint service object.

    :param str path: Freely definable object path for the
        media endpoint e.g., '/endpoint/a2dpsink'.
    """
    def __init__(self, path):
        self._bus = dbus.SystemBus()
        self._path = path
        super(GenericEndpoint, self).__init__(self._bus, self._path)

    def get_properties(self):
        """
        Returns the properties of the endpoint.  These should
        be initialized by a suitable subclass implementation
        by setting the `properties` class attribute.

        :return properties: dictionary of endpoint's capabilties
        :rtype: dict
        """
        return self.properties

    # Service object entry points defined below here --
    # you will need to implement these in your subclass
    @dbus.service.method("org.bluez.MediaEndpoint1",
                         in_signature="", out_signature="")
    def Release(self):
        """
        Called by bluez to let us know our registration
        has been released and the endpoint no longer exists

        :return:
        """
        pass

    @dbus.service.method("org.bluez.MediaEndpoint1",
                         in_signature="", out_signature="")
    def ClearConfiguration(self):
        """
        Called by bluez to let us know that the audio
        streaming process has been reset, for whatever reason,
        and we should now perform clean-up.

        :return:
        """
        pass

    @dbus.service.method("org.bluez.MediaEndpoint1",
                         in_signature="oay", out_signature="")
    def SetConfiguration(self, transport, config):
        """
        Provides a path to the media transport to use and
        the active configuration that was negotiated.

        :param str transport: Path to a device's file descriptor node
            which can be used to acquire the media transport e.g.,
            '/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE/fd0'
        :param array{byte} config: The configuration being used for
            the media transport.

        See also: :py:class:`.BTMediaTransport`
        """
        pass

    @dbus.service.method("org.bluez.MediaEndpoint1",
                         in_signature="ay", out_signature="ay")
    def SelectConfiguration(self, caps):
        """
        Initiates negotiations of the capabilities which should
        be resolved by this method.

        :param dict caps: Dictionary of device's capabilities
            for resolving capability negotiation by comparing
            to own capabilities.
        :return config: The resolved configuration
            to be used for the media transport.
        :rtype: array{byte}
        """
        pass
