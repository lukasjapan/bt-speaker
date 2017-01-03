from __future__ import unicode_literals

from uuid import BTUUID16

__SDP = BTUUID16('0001', 'SDP', 'Bluetooth Core Specification')  # noqa
__UDP = BTUUID16('0002', 'UDP', '[NO USE BY PROFILES]')  # noqa
__RFCOMM = BTUUID16('0003', 'RFCOMM', 'RFCOMM with TS 07.10')  # noqa
__TCP = BTUUID16('0004', 'TCP', '[NO USE BY PROFILES]')  # noqa
__TCS_BIN = BTUUID16('0005', 'TCS_BIN', 'Telephony Control Specification / TCS Binary [DEPRECATED]')  # noqa
__TCS_AT = BTUUID16('0006', 'TCS_AT', '[NO USE BY PROFILES]')  # noqa
__ATT = BTUUID16('0007', 'ATT', 'Attribute Protocol')  # noqa
__OBEX = BTUUID16('0008', 'OBEX', 'IrDA Interoperability')  # noqa
__IP = BTUUID16('0009', 'IP', '[NO USE BY PROFILES]')  # noqa
__FTP = BTUUID16('000A', 'FTP', '[NO USE BY PROFILES]')  # noqa
__HTTP = BTUUID16('000C', 'HTTP', '[NO USE BY PROFILES]')  # noqa
__WSP = BTUUID16('000E', 'WSP', '[NO USE BY PROFILES]')  # noqa
__BNEP = BTUUID16('000F', 'BNEP', 'Bluetooth Network Encapsulation Protocol (BNEP)')  # noqa
__UPNP = BTUUID16('0010', 'UPNP', 'Extended Service Discovery Profile (ESDP) [DEPRECATED]')  # noqa
__HIDP = BTUUID16('0011', 'HIDP', 'Human Interface Device Profile (HID)')  # noqa
__HardcopyControlChannel = BTUUID16('0012', 'HardcopyControlChannel', 'Hardcopy Cable Replacement Profile (HCRP)')  # noqa
__HardcopyDataChannel = BTUUID16('0014', 'HardcopyDataChannel', 'See Hardcopy Cable Replacement Profile (HCRP)')  # noqa
__HardcopyNotification = BTUUID16('0016', 'HardcopyNotification', 'Hardcopy Cable Replacement Profile (HCRP)')  # noqa
__AVCTP = BTUUID16('0017', 'AVCTP', 'Audio/Video Control Transport Protocol (AVCTP)')  # noqa
__AVDTP = BTUUID16('0019', 'AVDTP', 'Audio/Video Distribution Transport Protocol (AVDTP)')  # noqa
__CMTP = BTUUID16('001B', 'CMTP', 'Common ISDN Access Profile (CIP) [DEPRECATED]')  # noqa
__MCAPControlChannel = BTUUID16('001E', 'MCAPControlChannel', 'Multi-Channel Adaptation Protocol (MCAP)')  # noqa
__MCAPDataChannel = BTUUID16('001F', 'MCAPDataChannel', 'Multi-Channel Adaptation Protocol (MCAP)')  # noqa
__L2CAP = BTUUID16('0100', 'L2CAP', 'Bluetooth Core Specification')  # noqa

__ServiceDiscoveryServerServiceClassID = BTUUID16('1000', 'ServiceDiscoveryServerServiceClassID', 'Bluetooth Core Specification')  # noqa
__BrowseGroupDescriptorServiceClassID = BTUUID16('1001', 'BrowseGroupDescriptorServiceClassID', 'Bluetooth Core Specification')  # noqa
__PublicBrowseRoot = BTUUID16('1002', 'PublicBrowseRoot', 'Bluetooth Core Specification')  # noqa
__SerialPort = BTUUID16('1101', 'SerialPort', 'Serial Port Profile (SPP) NOTE: __The example SDP record in SPP v1.0 does not include a BluetoothProfileDescriptorList attribute, but some implementations may also use this UUID for the Profile Identifier.')  # noqa
__LANAccessUsingPPP = BTUUID16('1102', 'LANAccessUsingPPP', 'LAN Access Profile [DEPRECATED] NOTE: Used as both Service Class Identifier and Profile Identifier.')  # noqa
__DialupNetworking = BTUUID16('1103', 'DialupNetworking', 'Dial-up Networking Profile (DUN) NOTE: Used as both Service Class Identifier and Profile Identifier.')  # noqa
__IrMCSync = BTUUID16('1104', 'IrMCSync', 'Synchronization Profile (SYNC) NOTE: Used as both Service Class Identifier and Profile Identifier.')  # noqa
__OBEXObjectPush = BTUUID16('1105', 'OBEXObjectPush', 'Object Push Profile (OPP) NOTE: Used as both Service Class Identifier and Profile.')  # noqa
__OBEXFileTransfer = BTUUID16('1106', 'OBEXFileTransfer', 'File Transfer Profile (FTP) NOTE: Used as both Service Class Identifier and Profile Identifier.')  # noqa
__IrMCSyncCommand = BTUUID16('1107', 'IrMCSyncCommand', 'Synchronization Profile (SYNC)')  # noqa
__Headset = BTUUID16('1108', 'Headset', 'Headset Profile (HSP) NOTE: Used as both Service Class Identifier and Profile Identifier.')  # noqa
__CordlessTelephony = BTUUID16('1109', 'CordlessTelephony', 'Cordless Telephony Profile (CTP) NOTE: Used as both Service Class Identifier and Profile Identifier. [DEPRECATED]')  # noqa
__AudioSource = BTUUID16('110A', 'AudioSource', 'Advanced Audio Distribution Profile (A2DP)')  # noqa
__AudioSink = BTUUID16('110B', 'AudioSink', 'Advanced Audio Distribution Profile (A2DP)')  # noqa
__AVRemoteControlTarget = BTUUID16('110C', 'AVRemoteControlTarget', 'Audio/Video Remote Control Profile (AVRCP)')  # noqa
__AdvancedAudioDistribution = BTUUID16('110D', 'AdvancedAudioDistribution', 'Advanced Audio Distribution Profile (A2DP)')  # noqa
__AVRemoteControl = BTUUID16('110E', 'AVRemoteControl', 'Audio/Video Remote Control Profile (AVRCP) NOTE: Used as both Service Class Identifier and Profile Identifier.')  # noqa
__AVRemoteControlController = BTUUID16('110F', 'AVRemoteControlController', 'Audio/Video Remote Control Profile (AVRCP) NOTE: __The AVRCP specification v1.3 and later require that 0x110E also be included in the ServiceClassIDList before 0x110F for backwards compatibility.')  # noqa
__Intercom = BTUUID16('1110', 'Intercom', 'Intercom Profile (ICP) NOTE: Used as both Service Class Identifier and Profile Identifier. [DEPRECATED]')  # noqa
__Fax = BTUUID16('1111', 'Fax', 'Fax Profile (FAX) NOTE: Used as both Service Class Identifier and Profile Identifier. [DEPRECATED]')  # noqa
__HeadsetAudioGateway = BTUUID16('1112', 'HeadsetAudioGateway', 'Headset Profile (HSP)')  # noqa
__WAP = BTUUID16('1113', 'WAP', 'Interoperability Requirements for Bluetooth technology as a WAP, Bluetooth SIG [DEPRECATED]')  # noqa
__WAPCLIENT = BTUUID16('1114', 'WAPCLIENT', 'Interoperability Requirements for Bluetooth technology as a WAP, Bluetooth SIG [DEPRECATED]')  # noqa
__PANU = BTUUID16('1115', 'PANU', 'Personal Area Networking Profile (PAN) NOTE: Used as both Service Class Identifier and Profile Identifier for PANU role.')  # noqa
__NAP = BTUUID16('1116', 'NAP', 'Personal Area Networking Profile (PAN) NOTE: Used as both Service Class Identifier and Profile Identifier for NAP role.')  # noqa
__GN = BTUUID16('1117', 'GN', 'Personal Area Networking Profile (PAN) NOTE: Used as both Service Class Identifier and Profile Identifier for GN role.')  # noqa
__DirectPrinting = BTUUID16('1118', 'DirectPrinting', 'Basic Printing Profile (BPP)')  # noqa
__ReferencePrinting = BTUUID16('1119', 'ReferencePrinting', 'See Basic Printing Profile (BPP)')  # noqa
__BasicImagingProfile = BTUUID16('111A', 'BasicImagingProfile', 'Basic Imaging Profile (BIP)')  # noqa
__ImagingResponder = BTUUID16('111B', 'ImagingResponder', 'Basic Imaging Profile (BIP)')  # noqa
__ImagingAutomaticArchive = BTUUID16('111C', 'ImagingAutomaticArchive', 'Basic Imaging Profile (BIP)')  # noqa
__ImagingReferencedObjects = BTUUID16('111D', 'ImagingReferencedObjects', 'Basic Imaging Profile (BIP)')  # noqa
__Handsfree = BTUUID16('111E', 'Handsfree', 'Hands-Free Profile (HFP) NOTE: Used as both Service Class Identifier and Profile Identifier.')  # noqa
__HandsfreeAudioGateway = BTUUID16('111F', 'HandsfreeAudioGateway', 'Hands-free Profile (HFP)')  # noqa
__DirectPrintingReferenceObjectsService = BTUUID16('1120', 'DirectPrintingReferenceObjectsService', 'Basic Printing Profile (BPP)')  # noqa
__ReflectedUI = BTUUID16('1121', 'ReflectedUI', 'Basic Printing Profile (BPP)')  # noqa
__BasicPrinting = BTUUID16('1122', 'BasicPrinting', 'Basic Printing Profile (BPP)')  # noqa
__PrintingStatus = BTUUID16('1123', 'PrintingStatus', 'Basic Printing Profile (BPP)')  # noqa
__HumanInterfaceDeviceService = BTUUID16('1124', 'HumanInterfaceDeviceService', 'Human Interface Device (HID) NOTE: Used as both Service Class Identifier and Profile Identifier.')  # noqa
__HardcopyCableReplacement = BTUUID16('1125', 'HardcopyCableReplacement', 'Hardcopy Cable Replacement Profile (HCRP)')  # noqa
__HCRPrint = BTUUID16('1126', 'HCRPrint', 'Hardcopy Cable Replacement Profile (HCRP)')  # noqa
__HCRScan = BTUUID16('1127', 'HCRScan', 'Hardcopy Cable Replacement Profile (HCRP)')  # noqa
__CommonISDNAccess = BTUUID16('1128', 'CommonISDNAccess', 'Common ISDN Access Profile (CIP) NOTE: Used as both Service Class Identifier and Profile Identifier. [DEPRECATED]')  # noqa
__VideoConfGateway = BTUUID16('1129', 'VideoConfGateway', 'Video Conference Gateway')  # noqa
__UDIMtClass = BTUUID16('112A', 'UDIMtClass', '[UDI]')  # noqa
__UDITaClass = BTUUID16('112B', 'UDITaClass', '[UDI]')  # noqa
__AudioVideo = BTUUID16('112C', 'AudioVideo', 'Video Conferencing Profile (VCP), Bluetooth SIG')  # noqa
__SIMAccess = BTUUID16('112D', 'SIMAccess', 'SIM Access Profile (SAP) NOTE: Used as both Service Class Identifier and Profile Identifier.')  # noqa
__PhonebookAccessPCE = BTUUID16('112E', 'PhonebookAccessPCE', 'Phonebook Access Profile (PBAP)')  # noqa
__PhonebookAccessPSE = BTUUID16('112F', 'PhonebookAccessPSE', 'Phonebook Access Profile (PBAP)')  # noqa
__PhonebookAccess = BTUUID16('1130', 'PhonebookAccess', 'Phonebook Access Profile (PBAP)')  # noqa
__HeadsetHS = BTUUID16('1131', 'HeadsetHS', 'Headset Profile (HSP) NOTE: See erratum #3507. 0x1108 and 0x1203 should also be included in the ServiceClassIDList before 0x1131 for backwards compatibility.')  # noqa
__MessageAccessServer = BTUUID16('1132', 'MessageAccessServer', 'Message Access Profile (MAP)')  # noqa
__MessageNotificationServer = BTUUID16('1133', 'MessageNotificationServer', 'Message Access Profile (MAP)')  # noqa
__MessageAccessProfile = BTUUID16('1134', 'MessageAccessProfile', 'Message Access Profile (MAP)')  # noqa
__GNSS = BTUUID16('1135', 'GNSS', 'Global Navigation Satellite System Profile (GNSS)')  # noqa
__GNSSServer = BTUUID16('1136', 'GNSSServer', 'Global Navigation Satellite System Profile (GNSS)')  # noqa
__Display3D = BTUUID16('1137', 'Display3D', '3D Synchronization Profile (3DSP)')  # noqa
__Glasses3D = BTUUID16('1138', 'Glasses3D', '3D Synchronization Profile (3DSP)')  # noqa
__Synchronization3D = BTUUID16('1139', 'Synchronization3D', '3D Synchronization Profile (3DSP)')  # noqa
__MPSProfile = BTUUID16('113A', 'MPSProfile', 'Multi-Profile Specification (MPS)')  # noqa
__MPSSC = BTUUID16('113B', 'MPSSC', 'Multi-Profile Specification (MPS)')  # noqa
__PnPInformation = BTUUID16('1200', 'PnPInformation', 'Device Identification (DID) NOTE: Used as both Service Class Identifier and Profile Identifier.')  # noqa
__GenericNetworking = BTUUID16('1201', 'GenericNetworking', 'N/A')  # noqa
__GenericFileTransfer = BTUUID16('1202', 'GenericFileTransfer', 'N/A')  # noqa
__GenericAudio = BTUUID16('1203', 'GenericAudio', 'N/A')  # noqa
__GenericTelephony = BTUUID16('1204', 'GenericTelephony', 'N/A')  # noqa
__UPNPService = BTUUID16('1205', 'UPNPService', 'Enhanced Service Discovery Profile (ESDP) [DEPRECATED]')  # noqa
__UPNPIPService = BTUUID16('1206', 'UPNPIPService', 'Enhanced Service Discovery Profile (ESDP) [DEPRECATED]')  # noqa
__ESDPUPNPIPPAN = BTUUID16('1300', 'ESDPUPNPIPPAN', 'Enhanced Service Discovery Profile (ESDP) [DEPRECATED]')  # noqa
__ESDPUPNPIPLAP = BTUUID16('1301', 'ESDPUPNPIPLAP', 'Enhanced Service Discovery Profile (ESDP)[DEPRECATED]')  # noqa
__ESDPUPNPL2CAP = BTUUID16('1302', 'ESDPUPNPL2CAP', 'Enhanced Service Discovery Profile (ESDP)[DEPRECATED]')  # noqa
__VideoSource = BTUUID16('1303', 'VideoSource', 'Video Distribution Profile (VDP)')  # noqa
__VideoSink = BTUUID16('1304', 'VideoSink', 'Video Distribution Profile (VDP)')  # noqa
__VideoDistribution = BTUUID16('1305', 'VideoDistribution', 'Video Distribution Profile (VDP)')  # noqa
__HDP = BTUUID16('1400', 'HDP', 'Health Device Profile')  # noqa
__HDPSource = BTUUID16('1401', 'HDPSource', 'Health Device Profile (HDP)')  # noqa
__HDPSink = BTUUID16('1402', 'HDPSink', 'Health Device Profile (HDP)')  # noqa

SERVICES = {
    __SDP.uuid16: __SDP,
    __SDP.name: __SDP,
    __UDP.uuid16: __UDP,
    __UDP.name: __UDP,
    __RFCOMM.uuid16: __RFCOMM,
    __RFCOMM.name: __RFCOMM,
    __TCP.uuid16: __TCP,
    __TCP.name: __TCP,
    __TCS_BIN.uuid16: __TCS_BIN,
    __TCS_BIN.name: __TCS_BIN,
    __TCS_AT.uuid16: __TCS_AT,
    __TCS_AT.name: __TCS_AT,
    __ATT.uuid16: __ATT,
    __ATT.name: __ATT,
    __OBEX.uuid16: __OBEX,
    __OBEX.name: __OBEX,
    __IP.uuid16: __IP,
    __IP.name: __IP,
    __FTP.uuid16: __FTP,
    __FTP.name: __FTP,
    __HTTP.uuid16: __HTTP,
    __HTTP.name: __HTTP,
    __WSP.uuid16: __WSP,
    __WSP.name: __WSP,
    __BNEP.uuid16: __BNEP,
    __BNEP.name: __BNEP,
    __UPNP.uuid16: __UPNP,
    __UPNP.name: __UPNP,
    __HIDP.uuid16: __HIDP,
    __HIDP.name: __HIDP,
    __HardcopyControlChannel.uuid16: __HardcopyControlChannel,
    __HardcopyControlChannel.name: __HardcopyControlChannel,
    __HardcopyDataChannel.uuid16: __HardcopyDataChannel,
    __HardcopyDataChannel.name: __HardcopyDataChannel,
    __HardcopyNotification.uuid16: __HardcopyNotification,
    __HardcopyNotification.name: __HardcopyNotification,
    __AVCTP.uuid16: __AVCTP,
    __AVCTP.name: __AVCTP,
    __AVDTP.uuid16: __AVDTP,
    __AVDTP.name: __AVDTP,
    __CMTP.uuid16: __CMTP,
    __CMTP.name: __CMTP,
    __MCAPControlChannel.uuid16: __MCAPControlChannel,
    __MCAPControlChannel.name: __MCAPControlChannel,
    __MCAPDataChannel.uuid16: __MCAPDataChannel,
    __MCAPDataChannel.name: __MCAPDataChannel,
    __L2CAP.uuid16: __L2CAP,
    __L2CAP.name: __L2CAP,
    __ServiceDiscoveryServerServiceClassID.uuid16: __ServiceDiscoveryServerServiceClassID,  # noqa
    __ServiceDiscoveryServerServiceClassID.name: __ServiceDiscoveryServerServiceClassID,  # noqa
    __BrowseGroupDescriptorServiceClassID.uuid16: __BrowseGroupDescriptorServiceClassID,  # noqa
    __BrowseGroupDescriptorServiceClassID.name: __BrowseGroupDescriptorServiceClassID,  # noqa
    __SerialPort.uuid16: __SerialPort,
    __SerialPort.name: __SerialPort,
    __LANAccessUsingPPP.uuid16: __LANAccessUsingPPP,
    __LANAccessUsingPPP.name: __LANAccessUsingPPP,
    __DialupNetworking.uuid16: __DialupNetworking,
    __DialupNetworking.name: __DialupNetworking,
    __IrMCSync.uuid16: __IrMCSync,
    __IrMCSync.name: __IrMCSync,
    __OBEXObjectPush.uuid16: __OBEXObjectPush,
    __OBEXObjectPush.name: __OBEXObjectPush,
    __OBEXFileTransfer.uuid16: __OBEXFileTransfer,
    __OBEXFileTransfer.name: __OBEXFileTransfer,
    __IrMCSyncCommand.uuid16: __IrMCSyncCommand,
    __IrMCSyncCommand.name: __IrMCSyncCommand,
    __Headset.uuid16: __Headset,
    __Headset.name: __Headset,
    __CordlessTelephony.uuid16: __CordlessTelephony,
    __CordlessTelephony.name: __CordlessTelephony,
    __AudioSource.uuid16: __AudioSource,
    __AudioSource.name: __AudioSource,
    __AudioSink.uuid16: __AudioSink,
    __AudioSink.name: __AudioSink,
    __AVRemoteControlTarget.uuid16: __AVRemoteControlTarget,
    __AVRemoteControlTarget.name: __AVRemoteControlTarget,
    __AdvancedAudioDistribution.uuid16: __AdvancedAudioDistribution,
    __AdvancedAudioDistribution.name: __AdvancedAudioDistribution,
    __AVRemoteControl.uuid16: __AVRemoteControl,
    __AVRemoteControl.name: __AVRemoteControl,
    __AVRemoteControlController.uuid16: __AVRemoteControlController,
    __AVRemoteControlController.name: __AVRemoteControlController,
    __Intercom.uuid16: __Intercom,
    __Intercom.name: __Intercom,
    __Fax.uuid16: __Fax,
    __Fax.name: __Fax,
    __HeadsetAudioGateway.uuid16: __HeadsetAudioGateway,
    __HeadsetAudioGateway.name: __HeadsetAudioGateway,
    __WAP.uuid16: __WAP,
    __WAP.name: __WAP,
    __WAPCLIENT.uuid16: __WAPCLIENT,
    __WAPCLIENT.name: __WAPCLIENT,
    __PANU.uuid16: __PANU,
    __PANU.name: __PANU,
    __NAP.uuid16: __NAP,
    __NAP.name: __NAP,
    __GN.uuid16: __GN,
    __GN.name: __GN,
    __DirectPrinting.uuid16: __DirectPrinting,
    __DirectPrinting.name: __DirectPrinting,
    __ReferencePrinting.uuid16: __ReferencePrinting,
    __ReferencePrinting.name: __ReferencePrinting,
    __BasicImagingProfile.uuid16: __BasicImagingProfile,
    __BasicImagingProfile.name: __BasicImagingProfile,
    __ImagingResponder.uuid16: __ImagingResponder,
    __ImagingResponder.name: __ImagingResponder,
    __ImagingAutomaticArchive.uuid16: __ImagingAutomaticArchive,
    __ImagingAutomaticArchive.name: __ImagingAutomaticArchive,
    __ImagingReferencedObjects.uuid16: __ImagingReferencedObjects,
    __ImagingReferencedObjects.name: __ImagingReferencedObjects,
    __Handsfree.uuid16: __Handsfree,
    __Handsfree.name: __Handsfree,
    __HandsfreeAudioGateway.uuid16: __HandsfreeAudioGateway,
    __HandsfreeAudioGateway.name: __HandsfreeAudioGateway,
    __DirectPrintingReferenceObjectsService.uuid16: __DirectPrintingReferenceObjectsService,  # noqa
    __DirectPrintingReferenceObjectsService.name: __DirectPrintingReferenceObjectsService,  # noqa
    __ReflectedUI.uuid16: __ReflectedUI,
    __ReflectedUI.name: __ReflectedUI,
    __BasicPrinting.uuid16: __BasicPrinting,
    __BasicPrinting.name: __BasicPrinting,
    __PrintingStatus.uuid16: __PrintingStatus,
    __PrintingStatus.name: __PrintingStatus,
    __HumanInterfaceDeviceService.uuid16: __HumanInterfaceDeviceService,
    __HumanInterfaceDeviceService.name: __HumanInterfaceDeviceService,
    __HardcopyCableReplacement.uuid16: __HardcopyCableReplacement,
    __HardcopyCableReplacement.name: __HardcopyCableReplacement,
    __HCRPrint.uuid16: __HCRPrint,
    __HCRPrint.name: __HCRPrint,
    __HCRScan.uuid16: __HCRScan,
    __HCRScan.name: __HCRScan,
    __CommonISDNAccess.uuid16: __CommonISDNAccess,
    __CommonISDNAccess.name: __CommonISDNAccess,
    __SIMAccess.uuid16: __SIMAccess,
    __SIMAccess.name: __SIMAccess,
    __PhonebookAccessPCE.uuid16: __PhonebookAccessPCE,
    __PhonebookAccessPCE.name: __PhonebookAccessPCE,
    __PhonebookAccessPSE.uuid16: __PhonebookAccessPSE,
    __PhonebookAccessPSE.name: __PhonebookAccessPSE,
    __PhonebookAccess.uuid16: __PhonebookAccess,
    __PhonebookAccess.name: __PhonebookAccess,
    __HeadsetHS.uuid16: __HeadsetHS,
    __HeadsetHS.name: __HeadsetHS,
    __MessageAccessServer.uuid16: __MessageAccessServer,
    __MessageAccessServer.name: __MessageAccessServer,
    __MessageNotificationServer.uuid16: __MessageNotificationServer,
    __MessageNotificationServer.name: __MessageNotificationServer,
    __MessageAccessProfile.uuid16: __MessageAccessProfile,
    __MessageAccessProfile.name: __MessageAccessProfile,
    __GNSS.uuid16: __GNSS,
    __GNSS.name: __GNSS,
    __GNSSServer.uuid16: __GNSSServer,
    __GNSSServer.name: __GNSSServer,
    __Display3D.uuid16: __Display3D,
    __Display3D.name: __Display3D,
    __Glasses3D.uuid16: __Glasses3D,
    __Glasses3D.name: __Glasses3D,
    __Synchronization3D.uuid16: __Synchronization3D,
    __Synchronization3D.name: __Synchronization3D,
    __MPSProfile.uuid16: __MPSProfile,
    __MPSProfile.name: __MPSProfile,
    __MPSSC.uuid16: __MPSSC,
    __MPSSC.name: __MPSSC,
    __PnPInformation.uuid16: __PnPInformation,
    __PnPInformation.name: __PnPInformation,
    __GenericNetworking.uuid16: __GenericNetworking,
    __GenericNetworking.name: __GenericNetworking,
    __GenericFileTransfer.uuid16: __GenericFileTransfer,
    __GenericFileTransfer.name: __GenericFileTransfer,
    __GenericAudio.uuid16: __GenericAudio,
    __GenericAudio.name: __GenericAudio,
    __GenericTelephony.uuid16: __GenericTelephony,
    __GenericTelephony.name: __GenericTelephony,
    __UPNPService.uuid16: __UPNPService,
    __UPNPService.name: __UPNPService,
    __UPNPIPService.uuid16: __UPNPIPService,
    __UPNPIPService.name: __UPNPIPService,
    __ESDPUPNPIPPAN.uuid16: __ESDPUPNPIPPAN,
    __ESDPUPNPIPPAN.name: __ESDPUPNPIPPAN,
    __ESDPUPNPIPLAP.uuid16: __ESDPUPNPIPLAP,
    __ESDPUPNPIPLAP.name: __ESDPUPNPIPLAP,
    __ESDPUPNPL2CAP.uuid16: __ESDPUPNPL2CAP,
    __ESDPUPNPL2CAP.name: __ESDPUPNPL2CAP,
    __VideoSource.uuid16: __VideoSource,
    __VideoSource.name: __VideoSource,
    __VideoSink.uuid16: __VideoSink,
    __VideoSink.name: __VideoSink,
    __VideoDistribution.uuid16: __VideoDistribution,
    __VideoDistribution.name: __VideoDistribution,
    __HDP.uuid16: __HDP,
    __HDP.name: __HDP,
    __HDPSource.uuid16: __HDPSource,
    __HDPSource.name: __HDPSource,
    __HDPSink.uuid16: __HDPSink,
    __HDPSink.name: __HDPSink,
}
"""
:data dict SERVICES: A dictionary of service UUIDs which allows all
    bluetooth standard-based services to be keyed by either
    their short-form name or their UUID16 value.

    Example:

    ``SERVICES['AudioSource']`` shall return a :py:class:`.BTUUID16`
        denoting the A2DP audio source profile UUID.
    ``SERVICES['110A']`` shall return the same :py:class:`.BTUUID16`
        denoting the A2DP audio source profile UUID.
"""
