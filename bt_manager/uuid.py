from __future__ import unicode_literals
from exceptions import BTUUIDNotSpecifiedException


_BASE_UUID = '00000000-0000-1000-8000-00805F9B34FB'


class BTUUID:
    """
    This class encapsulates a UUID (universally unique identifier)
    which is a 128-bit value.  It is represented as a hex string of
    the form `ZZZZYYYY-BBBB-BBBB-BBBB-VVVVVVVVVVVV` although
    typically UUIDs are referenced only by the 16-bit `YYYY` part
    since this is generally sufficient to uniquely identify
    the services/protocols that form part of the bluetooth
    standard.

    When creating a UUID as 16-bits only, the `YYYY` nibbles are
    set accordingly with the remaining nibbles set automatically
    using the base UUID which is
    `00000000-0000-1000-8000-00805F9B34FB`.

    When creating a UUID as 32-bits, the uppermost 8 nibbles shall
    be set instead.

    Otherwise a fully qualified 128-bit UUID is assumed to be
    provided.

    For ease of use, optionally, a human readable name and
    description can be provided with the UUID.  It is encouraged
    that this is done as UUIDs are otherwise hard to read.

    :param str uuid: Optional full 128-bit UUID string of the
        form `ZZZZYYYY-BBBB-BBBB-BBBB-VVVVVVVVVVVV`
    :param str uuid16: Optional 16-bit UUID string of the form
        `YYYY`.  Base UUID is used to populate unset bits.
    :param str uuid32: Optional 32-bit UUID string of the form
        `ZZZZYYYY`.    Base UUID is used to populate unset
        bits.
    :param str name: Optional string providing a unique name
        for the UUID.
    :param str desc: Optional string providing a description
        of the UUID.
    :raises BTUUIDNotSpecifiedException: if neither a uuid,
        uuid16 nor uuid32 is provided.
    """
    def __init__(self, uuid=None, uuid16=None,
                 uuid32=None, name=None, desc=None):
        self.name = name
        self.desc = desc
        if (uuid):
            self.uuid = uuid.upper()
        elif (uuid16):
            self.uuid = _BASE_UUID[0:4] + uuid16[0:4].upper() + _BASE_UUID[8:]
        elif (uuid32):
            self.uuid = uuid32[0:8].upper() + _BASE_UUID[8:]
        else:
            raise BTUUIDNotSpecifiedException

    @property
    def uuid16(self):
        """
        Returns the 16-bit part of the UUID string i.e., given
        a UUID of the form `ZZZZYYYY-BBBB-BBBB-BBBB-VVVVVVVVVVVV`
        it shall return `YYYY`
        """
        return self.uuid[4:8]

    @property
    def uuid32(self):
        """
        Returns the 32-bit part of the UUID string i.e., given
        a UUID of the form `ZZZZYYYY-BBBB-BBBB-BBBB-VVVVVVVVVVVV`
        it shall return `ZZZZYYYY`
        """
        return self.uuid[0:8]

    def __repr__(self):
        return '<uuid:' + self.uuid + ' name:' + \
            str(self.name) + ' desc:' + str(self.desc) + '>'


class BTUUID16(BTUUID):
    """
    Shortened-form UUID allowing only 16-bit UUID to be
    created.  Refer to :py:class:`BTUUID` for details.
    """
    def __init__(self, uuid, name, desc=None):
        BTUUID.__init__(self, uuid16=uuid, name=name, desc=desc)


class BTUUID32(BTUUID):
    """
    Shortened-form UUID allowing only 32-bit UUID to be
    created.  Refer to :py:class:`BTUUID` for details.
    """
    def __init__(self, uuid, name, desc=None):
        BTUUID.__init__(self, uuid32=uuid, name=name, desc=desc)


BASE_UUID = BTUUID(uuid=_BASE_UUID, name='BASE_UUID',
                   desc='Base Universally Unique Identifier')
"""
:data BASE_UUID: The base UUID which takes the value of
    `00000000-0000-1000-8000-00805F9B34FB`
"""
