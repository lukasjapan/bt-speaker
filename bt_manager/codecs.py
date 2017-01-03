from __future__ import unicode_literals
from collections import namedtuple
from bt_manager import ffi
import os

A2DP_CODECS = {'SBC': 0x00,
               'MPEG12': 0x01,
               'MPEG24': 0x02,
               'ATRAC': 0x03,
               }
"""
Enumeration of codec types supported by A2DP profile
"""

SBCCodecConfig = namedtuple('SBCCodecConfig',
                            'channel_mode frequency allocation_method '
                            'subbands block_length min_bitpool '
                            'max_bitpool')
"""
Named tuple collection of SBC A2DP audio profile properties
"""


class SBCSamplingFrequency:
    """Indicates with which sampling frequency the SBC
    frame has been encoded."""
    FREQ_16KHZ = (1 << 3)
    FREQ_32KHZ = (1 << 2)
    FREQ_44_1KHZ = (1 << 1)
    FREQ_48KHZ = 1
    ALL = 0xF


class SBCBlocks:
    """The block size with which the stream has been encoded"""
    BLOCKS_4 = (1 << 3)
    BLOCKS_8 = (1 << 2)
    BLOCKS_12 = (1 << 1)
    BLOCKS_16 = 1
    ALL = 0xF


class SBCChannelMode:
    """Indicate with which channel mode the frame has been
    encoded. The number of channels depends on this information."""
    CHANNEL_MODE_MONO = (1 << 3)
    CHANNEL_MODE_DUAL = (1 << 2)
    CHANNEL_MODE_STEREO = (1 << 1)
    CHANNEL_MODE_JOINT_STEREO = 1
    ALL = 0xF


class SBCAllocationMethod:
    """Indicates how the bit pool is allocated to different
    subbands. Either it is based on the loudness of the sub
    band signal or on the signal to noise ratio."""
    SNR = (1 << 1)
    LOUDNESS = 1
    ALL = 0x3


class SBCSubbands:
    """indicates the number of subbands with which the frame
    has been encoded"""
    SUBBANDS_4 = (1 << 1)
    SUBBANDS_8 = 1
    ALL = 0x3


class SBCCodec:
    """
    Python cass wrapper around CFFI calls into the SBC codec
    implemented in C.  The main API is defined by sbc.h with
    additional functions added to encapsulate an SBC payload
    as part of an RTP packet.  The API extensions for RTP
    are designed to work directly with bluetooth media
    transport file descriptors for the A2DP profile.  So,
    the basic idea is that this class is instantiated as
    part of a media endpoint implementation in order to
    encode or decode data carried on the media transport.

    .. note:: You need two separate instantiations of this
        class if you wish to encode and decode at the same
        time.  Although the class implementation is the same,
        the underlying C implementation requires separate
        `sbc_t` instances.

    :param namedtuple config: Media endpoint negotiated
        configuration parameters.  These are not used
        directly by the codec here but translated to
        parameters usable by the codec. See
        :py:class:`.SBCCodecConfig`
    """

    def __init__(self, config):

        import sys

        try:
            self.codec = ffi.dlopen('./librtpsbc.so')
        except:
            print 'Exception:', sys.exc_info()[0]

        self.config = ffi.new('sbc_t *')
        self.ts = ffi.new('unsigned int *', 0)
        self.seq_num = ffi.new('unsigned int *', 0)
        self._init_sbc_config(config)
        self.codec.sbc_init(self.config, 0)

    def _init_sbc_config(self, config):
        """
        Translator from namedtuple config representation to
        the sbc_t type.

        :param namedtuple config: See :py:class:`.SBCCodecConfig`
        :returns:
        """
        if (config.channel_mode == SBCChannelMode.CHANNEL_MODE_MONO):
            self.config.mode = self.codec.SBC_MODE_MONO
        elif (config.channel_mode == SBCChannelMode.CHANNEL_MODE_STEREO):
            self.config.mode = self.codec.SBC_MODE_STEREO
        elif (config.channel_mode == SBCChannelMode.CHANNEL_MODE_DUAL):
            self.config.mode = self.codec.SBC_MODE_DUAL_CHANNEL
        elif (config.channel_mode == SBCChannelMode.CHANNEL_MODE_JOINT_STEREO):
            self.config.mode = self.codec.SBC_MODE_JOINT_STEREO

        if (config.frequency == SBCSamplingFrequency.FREQ_16KHZ):
            self.config.frequency = self.codec.SBC_FREQ_16000
        elif (config.frequency == SBCSamplingFrequency.FREQ_32KHZ):
            self.config.frequency = self.codec.SBC_FREQ_32000
        elif (config.frequency == SBCSamplingFrequency.FREQ_44_1KHZ):
            self.config.frequency = self.codec.SBC_FREQ_44100
        elif (config.frequency == SBCSamplingFrequency.FREQ_48KHZ):
            self.config.frequency = self.codec.SBC_FREQ_48000

        if (config.allocation_method == SBCAllocationMethod.LOUDNESS):
            self.config.allocation = self.codec.SBC_AM_LOUDNESS
        elif (config.allocation_method == SBCAllocationMethod.SNR):
            self.config.allocation = self.codec.SBC_AM_SNR

        if (config.subbands == SBCSubbands.SUBBANDS_4):
            self.config.subbands = self.codec.SBC_SB_4
        elif (config.subbands == SBCSubbands.SUBBANDS_8):
            self.config.subbands = self.codec.SBC_SB_8

        if (config.block_length == SBCBlocks.BLOCKS_4):
            self.config.blocks = self.codec.SBC_BLK_4
        elif (config.block_length == SBCBlocks.BLOCKS_8):
            self.config.blocks = self.codec.SBC_BLK_8
        elif (config.block_length == SBCBlocks.BLOCKS_12):
            self.config.blocks = self.codec.SBC_BLK_12
        elif (config.block_length == SBCBlocks.BLOCKS_16):
            self.config.blocks = self.codec.SBC_BLK_16

        self.config.bitpool = config.max_bitpool
        self.config.endian = self.codec.SBC_LE

    def encode(self, fd, mtu, data):
        """
        Encode the supplied data (byte array) and write to
        the media transport file descriptor encapsulated
        as RTP packets.  The encoder will calculate the
        required number of SBC frames and encapsulate as
        RTP to fit the MTU size.

        :param int fd: Media transport file descriptor
        :param int mtu: Media transport MTU size as returned
            when the media transport was acquired.
        :param array{byte} data: Data to encode and send
            over the media transport.
        :return:
        """
        self.codec.rtp_sbc_encode_to_fd(self.config,
                                        ffi.new('char[]',
                                                data),
                                        len(data),
                                        mtu,
                                        self.ts,
                                        self.seq_num,
                                        fd)

    def decode(self, fd, mtu, max_len=2560):
        """
        Read the media transport descriptor, depay
        the RTP payload and decode the SBC frames into
        a byte array.  The maximum number of bytes to
        be returned may be passed as an argument and all
        available bytes are returned to the caller.

        :param int fd: Media transport file descriptor
        :param int mtu: Media transport MTU size as returned
            when the media transport was acquired.
        :param int max_len: Optional.  Set maximum number of
            bytes to read.
        :return data: Decoded data bytes as an array.
        :rtype: array{byte}
        """
        output_buffer = ffi.new('char[]', max_len)
        sz = self.codec.rtp_sbc_decode_from_fd(self.config,
                                               output_buffer,
                                               max_len,
                                               mtu,
                                               fd)
        return ffi.buffer(output_buffer[0:sz])
