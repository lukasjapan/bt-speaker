from __future__ import unicode_literals

import dbus
import types
import pprint

from exceptions import BTSignalNameNotRecognisedException

class Signal():
    """
    Encapsulation of user callback wrapper for signals
    fired by dbus.  This allows us to prepend the signal
    name and the user callback argument.

    :param str signal: Signal name
    :param func user_callback: User-defined callback function to
        call when the signal triggers
    :param user_arg: User-defined callback argument to be passed
        as callback function
    """
    def __init__(self, signal, user_callback, user_arg):
        self.signal = signal
        self.user_callback = user_callback
        self.user_arg = user_arg

    def signal_handler(self, *args):
        """
        Method to call in order to invoke the user callback.

        :param args: list of signal-dependent arguments
        :return:
        """
        self.user_callback(self.signal, self.user_arg, *args)


class BTSimpleInterface:
    """
    Wrapper around dbus to encapsulated a BT simple interface
    entry point (i.e., has no signals or properties).

    :param str path: Object path pertaining to the interface to open
                     e.g., '/org/bluez/985/hci0'
    :param str addr: dbus address of the interface instance to open
                     e.g., 'org.bluez.Adapter'

    .. note:: This class should always be sub-classed with a concrete
        implementation of a bluez interface which has no signals or
        properties.
    """
    def __init__(self, path, addr):
        self._dbus_addr = addr
        self._bus = dbus.SystemBus()
        self._object = self._bus.get_object('org.bluez', path)
        self._interface = dbus.Interface(self._object, addr)
        self._path = path


# This class is not intended to be instantiated directly and should be
# sub-classed with a concrete implementation for an interface
class BTInterface(BTSimpleInterface):
    """
    Wrapper around DBus to encapsulated a BT interface
    entry point e.g., an adapter, a device, etc.

    :param str path: Object path pertaining to the interface to open
                     e.g., '/org/bluez/985/hci0'
    :param str addr: dbus address of the interface instance to open
                     e.g., 'org.bluez.Adapter'

    .. note:: This class should always be sub-classed with a concrete
        implementation of a bluez interface which has both signals
        and properties.
    """

    SIGNAL_PROPERTY_CHANGED = 'PropertiesChanged'
    """
    :signal PropertyChanged(sig_name, user_arg, prop_name, prop_value):
        Signal notifying when a property has changed.
    """

    def __init__(self, path, addr):
        BTSimpleInterface.__init__(self, path, addr)
        self._signals = {}
        self._signal_names = []
        self._properties = dbus.Interface(self._object, 'org.freedesktop.DBus.Properties')
        self._register_signal_name(BTInterface.SIGNAL_PROPERTY_CHANGED)
        # # uncomment to reverse engineer dbus signals
        # self._bus.add_signal_receiver(self._property_changed, sender_keyword='sender',
        #                                                       destination_keyword='destination',
        #                                                       interface_keyword='interface',
        #                                                       member_keyword='member',
        #                                                       path_keyword='path',
        #                                                       message_keyword='message')

    def _property_changed(self, *args, **named_args):
        print('--------------------------')
        for arg in args: print(arg)
        for key in named_args.keys(): print("%s: %s" % (key, named_args[key]))

    def _register_signal_name(self, name):
        """
        Helper function to register allowed signals on this
        instance.  Need only be called once per signal name and must be done
        for each signal that may be used via :py:meth:`add_signal_receiver`

        :param str name: Signal name to register e.g.,
            :py:attr:`SIGNAL_PROPERTY_CHANGED`
        :return:
        """
        self._signal_names.append(name)

    def add_signal_receiver(self, callback_fn, signal, user_arg):
        """
        Add a signal receiver callback with user argument

        See also :py:meth:`remove_signal_receiver`,
        :py:exc:`.BTSignalNameNotRecognisedException`

        :param func callback_fn: User-defined callback function to call when
            signal triggers
        :param str signal: Signal name e.g.,
            :py:attr:`.BTInterface.SIGNAL_PROPERTY_CHANGED`
        :param user_arg: User-defined callback argument to be passed with
            callback function
        :return:
        :raises BTSignalNameNotRecognisedException: if the signal name is
            not registered
        """
        if (signal in self._signal_names):
            s = Signal(signal, callback_fn, user_arg)
            self._signals[signal] = s
            self._bus.add_signal_receiver(s.signal_handler, signal, path=self._path)
        else:
            raise BTSignalNameNotRecognisedException

    def remove_signal_receiver(self, signal):
        """
        Remove an installed signal receiver by signal name.

        See also :py:meth:`add_signal_receiver`
        :py:exc:`exceptions.BTSignalNameNotRecognisedException`

        :param str signal: Signal name to uninstall
            e.g., :py:attr:`SIGNAL_PROPERTY_CHANGED`
        :return:
        :raises BTSignalNameNotRecognisedException: if the signal name is
            not registered
        """
        if (signal in self._signal_names):
            s = self._signals.get(signal)
            if (s):
                self._bus.remove_signal_receiver(s.signal_handler,
                                                 signal,
                                                 dbus_interface=self._dbus_addr)  # noqa
                self._signals.pop(signal)
        else:
            raise BTSignalNameNotRecognisedException

    def get_property(self, name):
        """
        Helper to get a property value by name or all
        properties as a dictionary.

        See also :py:meth:`set_property`

        :param str name: defaults to None which means all properties
            in the object's dictionary are returned as a dict.
            Otherwise, the property name key is used and its value
            is returned.
        :return: Property value by property key, or a dictionary of
            all properties
        :raises KeyError: if the property key is not found in the
            object's dictionary
        :raises dbus.Exception: org.bluez.Error.DoesNotExist
        :raises dbus.Exception: org.bluez.Error.InvalidArguments
        """
        self._properties.Get(self._dbus_addr, name)

    def set_property(self, name, value):
        """
        Helper to set a property value by name, translating to correct
        dbus type

        See also :py:meth:`get_property`

        :param str name: The property name in the object's dictionary
            whose value shall be set.
        :param value: Properties new value to be assigned.
        :return:
        :raises KeyError: if the property key is not found in the
            object's dictionary
        :raises dbus.Exception: org.bluez.Error.DoesNotExist
        :raises dbus.Exception: org.bluez.Error.InvalidArguments
        """
        self._properties.Set(self._dbus_addr, name, value)
