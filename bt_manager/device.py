from __future__ import unicode_literals

from interface import BTInterface
from adapter import BTAdapter
from exceptions import BTDeviceNotSpecifiedException


class BTGenericDevice(BTInterface):
    """
    Generic BT device which has its own interface bus address but is
    associated with a BT adapter.

    :param str addr: Interface address e.g., 'org.bluez.Device'
    :param str dev_path: Optional fully qualified device object path
        e.g., '/org/bluez/985/hci0/dev_00_11_67_D2_AB_EE'
    :param str adapter_path: Optional fully qualified adapter object
        path if using dev_id e.g., '/org/bluez/985/hci0'
    :param str adapter_id: Optional adapter device ID if using dev_id
        e.g. 'hci0' or '11:22:33:44:55:66'
    :param str dev_id: Optional device ID to look-up object path
        e.g. '11:22:33:44:55:66'
    :raises BTDeviceNotSpecifiedException:
        if the device address was not specified unambiguously.

    .. note:: This class should always be sub-classed with a concrete
        implementation of a bluez interface.
    """
    def __init__(self, addr, dev_path=None, adapter_path=None,
                 adapter_id=None, dev_id=None):
        if (dev_path):
            path = dev_path
        elif (dev_id):
            if (adapter_id or adapter_path):
                adapter = BTAdapter(adapter_path=adapter_path,
                                    adapter_id=adapter_id)
            else:
                adapter = BTAdapter()
            path = adapter.find_device(dev_id)
        else:
            raise BTDeviceNotSpecifiedException
        BTInterface.__init__(self, path, addr)


class BTDevice(BTGenericDevice):
    """
    Wrapper around dbus to encapsulate the org.bluez.Device interface.
    Refer to :py:class:`BTGenericDevice` for init arguments.

    :Properties:

    * **Address(str) [readonly]**: The Bluetooth device address of the
        remote device.
    * **Name(str) [readonly]**: The Bluetooth remote name. This value can
        not be changed. Use the Alias property instead.
    * **Icon(str) [readonly]**: Proposed icon name according to the
        freedesktop.org icon naming specification.
    * **Class(str) [readonly]**: The Bluetooth class of device of the remote
        device.
    * **UUIDs(list{str}) [readonly]**: List of 128-bit UUIDs that represents
        the available remote services.
    * **Paired(boolean) [readonly]**: Indicates if the remote device is paired.
    * **Connected(boolean) [readonly]**: Indicates if the remote device is
        connected.
    * **Trusted(boolean) [readwrite]**: Indicates if the remote device is
        trusted.
    * **Alias(str) [readwrite]**: The name alias for the remote device. The
        alias can be used to have a different friendly name for the remote
        device. In case no alias is set, it will return the remote device name.
        Setting an empty string as alias will convert it back to the remote
        device name. When reseting the alias with an empty string, the emitted
        :py:attr`.SIGNAL_PROPERTY_CHANGED` signal will show the remote
        name again.
    * **Nodes(list{str}) [readonly]**: List of device node object paths.
    * **Adapter(str) [readonly]**: The object path of the adpater the device
        belongs to.
    * **LegacyPairing(boolean) [readonly]**: Set to true if the device only
        supports the pre-2.1 pairing mechanism. This property is useful in the
        :py:attr`.SIGNAL_DEVICE_FOUND` signal to anticipate whether legacy
        or simple pairing will occur. Note that this property can exhibit
        false-positives in the case of Bluetooth 2.1 (or newer) devices that
        have disabled Extended Inquiry Response support.
    * **Blocked(boolean) [readonly]**: Set to true if the device is blocked.
    * **Product(uint16) [readonly]**: Product code identifier.
    * **Vendor(uint16) [readonly]**: Product vendor identifier.
    * **Services(list{str}) [readonly]**: TBD.
    """

    SIGNAL_DISCONNECT_REQUESTED = 'DisconnectRequested'
    """
    :signal DisconnectRequested(signal_name, user_arg): This signal will be
        sent when a low level disconnection to a remote device has been
        requested. The actual disconnection will happen 2 seconds later.
    """
    SIGNAL_NODE_CREATED = 'NodeCreated'
    """
    :signal NodeCreated(signal_name, user_arg, node_path): Signal notifying
        when a new device node has been created.
    """
    SIGNAL_NODE_REMOVED = 'NodeRemoved'
    """
    :signal NodeRemoved(signal_name, user_arg, node_path): Signal notifying
        when a device node has been removed.
    """

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Device',
                                 *args, **kwargs)
        self._register_signal_name(BTDevice.SIGNAL_DISCONNECT_REQUESTED)
        self._register_signal_name(BTDevice.SIGNAL_NODE_CREATED)
        self._register_signal_name(BTDevice.SIGNAL_NODE_REMOVED)

    def discover_services(self, pattern=''):
        """
        This method starts the service discovery to retrieve
        remote service records.

        Refer to :py:class:`.BTDiscoveryInfo` to decode each XML service
        record.

        :param str pattern: can be used to specify specific UUIDs.
            An empty string will look for the public browse group.
        :return: a dictionary with the record handles as keys and
            the service record in XML format as values. The key is
            uint32 and the value a string for this dictionary.
        :rtype: dict
        :raises dbus.Exception: org.bluez.Error.NotReady
        :raises dbus.Exception: org.bluez.Error.Failed
        :raises dbus.Exception: org.bluez.Error.InProgress
        """
        return self._interface.DiscoverServices(pattern)

    def cancel_discovery(self):
        """
        This method will cancel any previous :py:meth:`discover_services`
        transaction.

        :return:
        :raises dbus.Exception: org.bluez.Error.NotReady
        :raises dbus.Exception: org.bluez.Error.Failed
        :raises dbus.Exception: org.bluez.Error.NotAuthorized
        """
        return self._interface.CancelDiscovery()

    def disconnect(self):
        """
        This method disconnects a specific remote device by
        terminating the low-level ACL connection. The use of
        this method should be restricted to administrator
        use.

        A :py:attr:`.SIGNAL_DISCONNECT_REQUESTED` signal will be
        sent and the actual disconnection will only happen 2
        seconds later.
        This enables upper-level applications to terminate
        their connections gracefully before the ACL connection
        is terminated.

        :return:
        :raises dbus.Exception: org.bluez.Error.NotConnected
        """
        return self._interface.Disconnect()
