from __future__ import unicode_literals

from interface import BTInterface

class BTAdapter(BTInterface):
    """
    Wrapper around dbus to encapsulate org.bluez.adapter interface.

    :param str adapter_path: Object path to bluetooth adapter.
        If not given, can use adapter_id instead.
    :param str adapter_id: Adapter's MAC address to look-up to find
        path e.g., '11:22:33:44:55:66'

    :Properties:

    * **Address(str) [readonly]**: The Bluetooth device address
        of the adapter.
    * **Name(str) [readonly]**: The Bluetooth system name
        (pretty hostname).
        This property is either a static system default
        or controlled by an external daemon providing
        access to the pretty hostname configuration.
    * **Alias(str) [readwrite]**: The Bluetooth friendly name.
        This value can be changed.
        In case no alias is set, it will return the system
        provided name. Setting an empty string as alias will
        convert it back to the system provided name.
        When resetting the alias with an empty string, the
        property will default back to system name.
        On a well configured system, this property never
        needs to be changed since it defaults to the system
        name and provides the pretty hostname. Only if the
        local name needs to be different from the pretty
        hostname, this property should be used as last
        resort.
    * **Class(uint32) [readonly]**: The Bluetooth class of
        device.
        This property represents the value that is either
        automatically configured by DMI/ACPI information
        or provided as static configuration.
    * **Powered(boolean) [readwrite]**: Switch an adapter on or
        off. This will also set the appropriate connectable
        state of the controller.
        The value of this property is not persistent. After
        restart or unplugging of the adapter it will reset
        back to false.
    * **Discoverable(boolean) [readwrite]**: Switch an adapter
        to discoverable or non-discoverable to either make it
        visible or hide it. This is a global setting and should
        only be used by the settings application.
        If DiscoverableTimeout is set to a non-zero
        value then the system will set this value back to
        false after the timer expired.
        In case the adapter is switched off, setting this
        value will fail.
        When changing the Powered property the new state of
        this property will be updated via a
        :py:attr:`.BTInterface.SIGNAL_PROPERTY_CHANGED`
        signal.
        For any new adapter this settings defaults to false.
    * **Pairable(boolean) [readwrite]**: Switch an adapter to
        pairable or non-pairable. This is a global setting and
        should only be used by the settings application.
    * **PairableTimeout(uint32) [readwrite]**:
        The pairable timeout in seconds. A value of zero
        means that the timeout is disabled and it will stay in
        pairable mode forever.
        The default value for pairable timeout should be
        disabled (value 0).
    * **DiscoverableTimeout(uint32) [readwrite]**:
        The discoverable timeout in seconds. A value of zero
        means that the timeout is disabled and it will stay in
        discoverable/limited mode forever.
        The default value for the discoverable timeout should
        be 180 seconds (3 minutes).
    * **Discovering(boolean) [readonly]**:
        Indicates that a device discovery procedure is active.
    * **UUIDs(array{str}) [readonly]**:
        List of 128-bit UUIDs that represents the available
        local services.
    * **Modalias(str) [readonly, optional]**:
        Local Device ID information in modalias format
        used by the kernel and udev.

    See also: :py:class:`.BTManager`
    """

    SIGNAL_DEVICE_FOUND = 'DeviceFound'
    """
    :signal DeviceFound(signal_name, user_arg, device_path): Signal
        notifying when a new device has been found
    """
    SIGNAL_DEVICE_REMOVED = 'DeviceRemoved'
    """
    :signal DeviceRemoved(signal_name, user_arg, device_path):
        Signal notifying when a device has been removed
    """
    SIGNAL_DEVICE_CREATED = 'DeviceCreated'
    """
    :signal DeviceCreated(signal_name, user_arg, device_path):
        Signal notifying when a new device is created
    """
    SIGNAL_DEVICE_DISAPPEARED = 'DeviceDisappeared'
    """
    :signal DeviceDisappeared(signal_name, user_arg, device_path):
        Signal notifying when a device is now out-of-range
    """

    def __init__(self, adapter_path):
        BTInterface.__init__(self, adapter_path, 'org.bluez.Adapter1')
        self._register_signal_name(BTAdapter.SIGNAL_DEVICE_FOUND)
        self._register_signal_name(BTAdapter.SIGNAL_DEVICE_REMOVED)
        self._register_signal_name(BTAdapter.SIGNAL_DEVICE_CREATED)
        self._register_signal_name(BTAdapter.SIGNAL_DEVICE_DISAPPEARED)

    def start_discovery(self):
        """
        This method starts the device discovery session. This
        includes an inquiry procedure and remote device name
        resolving. Use :py:meth:`stop_discovery` to release the sessions
        acquired.

        This process will start emitting :py:attr:`SIGNAL_DEVICE_FOUND`
        and :py:attr:`.SIGNAL_PROPERTY_CHANGED` 'discovering' signals.

        :return:
        :raises dbus.Exception: org.bluez.Error.NotReady
        :raises dbus.Exception: org.bluez.Error.Failed
        """
        return self._interface.StartDiscovery()

    def stop_discovery(self):
        """
        This method will cancel any previous :py:meth:`start_discovery`
        transaction.

        Note that a discovery procedure is shared between all
        discovery sessions thus calling py:meth:`stop_discovery` will
        only release a single session.

        :return:
        :raises dbus.Exception: org.bluez.Error.NotReady
        :raises dbus.Exception: org.bluez.Error.Failed
        :raises dbus.Exception: org.bluez.Error.NotAuthorized
        """
        return self._interface.StopDiscovery()

    def find_device(self, dev_id):
        """
        Returns the object path of device for given address.
        The device object needs to be first created via
        :py:meth:`create_device` or
        :py:meth:`create_paired_device`

        :param str dev_id: Device MAC address to look-up e.g.,
            '11:22:33:44:55:66'
        :return: Device object path e.g.,
            '/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE'
        :rtype: str
        :raises dbus.Exception: org.bluez.Error.DoesNotExist
        :raises dbus.Exception: org.bluez.Error.InvalidArguments
        """
        return self._interface.FindDevice(dev_id)

    def list_devices(self):
        """
        Returns list of device object paths.

        :return: List of device object paths
        :rtype: list
        :raises dbus.Exception: org.bluez.Error.InvalidArguments
        :raises dbus.Exception: org.bluez.Error.Failed
        :raises dbus.Exception: org.bluez.Error.OutOfMemory
        """
        return self._interface.ListDevices()

    def create_paired_device(self, dev_id, agent_path,
                             capability, cb_notify_device, cb_notify_error):
        """
        Creates a new object path for a remote device. This
        method will connect to the remote device and retrieve
        all SDP records and then initiate the pairing.

        If a previously :py:meth:`create_device` was used
        successfully, this method will only initiate the pairing.

        Compared to :py:meth:`create_device` this method will
        fail if the pairing already exists, but not if the object
        path already has been created. This allows applications
        to use :py:meth:`create_device` first and then, if needed,
        use :py:meth:`create_paired_device` to initiate pairing.

        The agent object path is assumed to reside within the
        process (D-Bus connection instance) that calls this
        method. No separate registration procedure is needed
        for it and it gets automatically released once the
        pairing operation is complete.

        :param str dev_id: New device MAC address create
            e.g., '11:22:33:44:55:66'
        :param str agent_path: Path used when creating the
            bluetooth agent e.g., '/test/agent'
        :param str capability: Pairing agent capability
            e.g., 'DisplayYesNo', etc
        :param func cb_notify_device: Callback on success.  The
            callback is called with the new device's object
            path as an argument.
        :param func cb_notify_error: Callback on error.  The
            callback is called with the error reason.
        :return:
        :raises dbus.Exception: org.bluez.Error.InvalidArguments
        :raises dbus.Exception: org.bluez.Error.Failed
        """
        return self._interface.CreatePairedDevice(dev_id,
                                                  agent_path,
                                                  capability,
                                                  reply_handler=cb_notify_device,  # noqa
                                                  error_handler=cb_notify_error)   # noqa

    def remove_device(self, dev_path):
        """
        This removes the remote device object at the given
        path. It will remove also the pairing information.

        :param str dev_path: Device object path to remove
            e.g., '/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE'
        :return:
        :raises dbus.Exception: org.bluez.Error.InvalidArguments
        :raises dbus.Exception: org.bluez.Error.Failed
        """
        return self._interface.RemoveDevice(dev_path)
