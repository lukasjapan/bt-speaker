from __future__ import unicode_literals

import dbus.service

from .exceptions import BTRejectedException
from .interface import BTInterface

class BTAgentManager(BTInterface):
    def __init__(self):
        BTInterface.__init__(self, '/org/bluez', 'org.bluez.AgentManager1')
        
    def register_agent(self, path, capability=""):
        """
        This registers an agent handler.

        The object path defines the path of the agent
        that will be called when user input is needed.

        Every application can register its own agent and
        for all actions triggered by that application its
        agent is used.

        It is not required by an application to register
        an agent. If an application does chooses to not
        register an agent, the default agent is used. This
        is on most cases a good idea. Only application
        like a pairing wizard should register their own
        agent.

        An application can only register one agent. Multiple
        agents per application is not supported.

        The capability parameter can have the values
        "DisplayOnly", "DisplayYesNo", "KeyboardOnly",
        "NoInputNoOutput" and "KeyboardDisplay" which
        reflects the input and output capabilities of the
        agent.

        If an empty string is used it will fallback to
        "DisplayYesNo".

        Possible errors: org.bluez.Error.InvalidArguments
                 org.bluez.Error.AlreadyExists
        """
        return self._interface.RegisterAgent(path, capability)

    def unregister_agent(self, path):
        """
        This unregisters the agent that has been previously
        registered. The object path parameter must match the
        same value that has been used on registration.

        Possible errors: org.bluez.Error.DoesNotExist
        """
        return self._interface.UnregisterAgent(path)

    def request_default_agent(self, path):
        """
        This requests is to make the application agent
        the default agent. The application is required
        to register an agent.

        Special permission might be required to become
        the default agent.

        Possible errors: org.bluez.Error.DoesNotExist
        """
        return self._interface.RequestDefaultAgent(path)


class BTAgent(dbus.service.Object):
    """
    Simple BT device pairing agent.

    A bluetooth pairing agent is responsible for admitting
    new devices onto the system and registering them
    for subsequent use.  The procedure is abstracted away
    into a service object that implements a few procedures
    depending on the type of pairing scheme in use.

    Different pairing schemes are required since some
    devices do not have displays or keypads allowing
    them to enter passkeys or confirm passkeys.

    The SSP (Secure Simple Pairing) schemes that can
    be supported using this agent are:

    * `Just works`: No user interaction required.
    * `Numeric comparison`: A pass key is displayed which
        the receiving device must confirm with a
        binary yes/no response.
    * `Passkey entry`: A pass key must be entered manually
        which the receiving device must confirm by also
        entering the same pass key.

    The pairing scheme selected will be dependent on
    the `capability` of the agent which is defined
    when the agent is registered via the
    :py:meth:`.BTAdapter.register_agent` method.

    See also: :py:class:`.BTAdapter`
    """

    NOTIFY_ON_RELEASE = 'Release'
    NOTIFY_ON_AUTHORIZE = 'Authorize'
    NOTIFY_ON_REQUEST_PIN_CODE = 'RequestPinCode'
    NOTIFY_ON_REQUEST_PASS_KEY = 'RequestPasskey'
    NOTIFY_ON_DISPLAY_PASS_KEY = 'DisplayPasskey'
    NOTIFY_ON_REQUEST_CONFIRMATION = 'RequestConfirmation'
    NOTIFY_ON_CONFIRM_MODE_CHANGE = 'ConfirmModeChange'
    NOTIFY_ON_CANCEL = 'Cancel'

    def __init__(self,
                 path='/test/agent',
                 auto_authorize_connections=False,
                 default_pin_code='0000',
                 default_pass_key=0,   # Range: 0-999999
                 cb_notify_on_release=None,
                 cb_notify_on_authorize=None,
                 cb_notify_on_request_pin_code=None,
                 cb_notify_on_request_pass_key=None,
                 cb_notify_on_display_pass_key=None,
                 cb_notify_on_request_confirmation=None,
                 cb_notify_on_confirm_mode_change=None,
                 cb_notify_on_cancel=None):

        self.auto_authorize_connections = auto_authorize_connections
        self.default_pin_code = default_pin_code
        self.default_pass_key = default_pass_key
        self.cb_notify_on_release = cb_notify_on_release
        self.cb_notify_on_authorize = cb_notify_on_authorize
        self.cb_notify_on_request_pin_code = cb_notify_on_request_pin_code
        self.cb_notify_on_request_pass_key = cb_notify_on_request_pass_key
        self.cb_notify_on_display_pass_key = cb_notify_on_display_pass_key
        self.cb_notify_on_request_confirmation = \
            cb_notify_on_request_confirmation
        self.cb_notify_on_confirm_mode_change = \
            cb_notify_on_confirm_mode_change
        self.cb_notify_on_cancel = cb_notify_on_cancel
        self._path = path
        bus = dbus.SystemBus()
        super(BTAgent, self).__init__(bus, path)

    # Service object entry points defined below here
    @dbus.service.method("org.bluez.Agent1", in_signature="", out_signature="")
    def Release(self):
        if (self.cb_notify_on_release):
            self.cb_notify_on_release(BTAgent.NOTIFY_ON_RELEASE)

    @dbus.service.method("org.bluez.Agent1", in_signature="os",
                         out_signature="")
    def AuthorizeService(self, device, uuid):
        if (self.cb_notify_on_authorize):
            if (not self.cb_notify_on_authorize(BTAgent.NOTIFY_ON_AUTHORIZE,
                                                device,
                                                uuid)):
                raise BTRejectedException('Connection not authorized by user')
        elif (not self.auto_authorize_connections):
            raise BTRejectedException('Auto authorize is off')

    @dbus.service.method("org.bluez.Agent1", in_signature="o",
                         out_signature="s")
    def RequestPinCode(self, device):
        if (self.cb_notify_on_request_pin_code):
            pin_code = self.cb_notify_on_request_pin_code(BTAgent.NOTIFY_ON_REQUEST_PIN_CODE,  # noqa
                                                          device)
            if (pin_code is None):
                raise BTRejectedException('User did not provide PIN code')
        elif (self.default_pin_code is None):
            raise BTRejectedException('No default PIN code set')
        else:
            pin_code = self.default_pin_code
        return dbus.String(pin_code)

    @dbus.service.method("org.bluez.Agent1", in_signature="o",
                         out_signature="s")
    def RequestPasskey(self, device):
        if (self.cb_notify_on_request_pass_key):
            pass_key = self.cb_notify_on_request_pass_key(BTAgent.NOTIFY_ON_REQUEST_PASS_KEY,  # noqa
                                                          device)
            if (pass_key is None):
                raise BTRejectedException('User did not provide pass key')
        elif (self.default_pass_key is None):
            raise BTRejectedException('No default pass key set')
        else:
            pass_key = self.default_pass_key
        return dbus.UInt32(pass_key)

    @dbus.service.method("org.bluez.Agent1", in_signature="ou",
                         out_signature="")
    def DisplayPasskey(self, device, pass_key):
        if (self.cb_notify_on_display_pass_key):
            self.cb_notify_on_display_pass_key(BTAgent.NOTIFY_ON_DISPLAY_PASS_KEY,  # noqa
                                               device, pass_key)

    @dbus.service.method("org.bluez.Agent1", in_signature="ou",
                         out_signature="")
    def RequestConfirmation(self, device, pass_key):
        if (self.cb_notify_on_request_confirmation):
            if (not self.cb_notify_on_request_confirmation(BTAgent.NOTIFY_ON_REQUEST_CONFIRMATION,  # noqa
                                                           device, pass_key)):
                raise \
                    BTRejectedException('User confirmation of pass key negative')  # noqa

    @dbus.service.method("org.bluez.Agent1", in_signature="s", out_signature="")
    def ConfirmModeChange(self, mode):
        if (self.cb_notify_on_confirm_mode_change):
            if (not self.cb_notify_on_confirm_mode_change(BTAgent.NOTIFY_ON_CONFIRM_MODE_CHANGE,  # noqa
                                                          mode)):
                raise \
                    BTRejectedException('User mode change confirmation negative')  # noqa

    @dbus.service.method("org.bluez.Agent1", in_signature="", out_signature="")
    def Cancel(self):
        if (self.cb_notify_on_cancel):
            self.cb_notify_on_cancel(BTAgent.NOTIFY_ON_CANCEL)
