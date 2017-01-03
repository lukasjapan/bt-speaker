from __future__ import unicode_literals

import dbus


class BTSignalNameNotRecognisedException:
    """
    Exception raised for when a signal name is not recognized.
    Check the originating class for a list of supported signal names
    """
    pass


class BTDeviceNotSpecifiedException:
    """
    Exception raised for when a device is not specified
    """
    pass


class BTRejectedException(dbus.DBusException):
    """
    Exception raised to notify that the user rejected
    a pairing attempt.
    """
    _dbus_error_name = "org.bluez.Error.Rejected"


class BTInvalidConfiguration(dbus.DBusException):
    """
    Exception raised to denote an invalid configuration
    parameter
    """
    _dbus_error_name = "org.bluez.Error.InvalidConfiguration"


class BTIncompatibleTransportAccessType(dbus.DBusException):
    """
    Exception raised when attempting to access a media
    transport file descriptor without correct access
    permissions.
    """
    _dbus_error_name = "org.bluez.Error.InvalidConfiguration"


class BTUUIDNotSpecifiedException:
    """
    Exception raised when creating a UUID without providing
    a valid UUID number
    """
    pass
