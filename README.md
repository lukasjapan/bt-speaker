# BT-Speaker

A simple Bluetooth Speaker Daemon designed for the Raspberry Pi 3.

## Installation

Quick Installation for Raspbian:

```bash
sudo -i
bash <(curl -s https://raw.githubusercontent.com/lukasjapan/bt-speaker/master/install.sh)
```

For details refer to the comments in the [install script](https://github.com/lukasjapan/bt-speaker/blob/master/install.sh).

Depending on your application, you might also want to send all audio to the headphone jack.
This can be done by `raspi-config`:

`Advanced Options` -> `Audio` -> `Force 3.5mm ('headphone') jack`

_Note_: Bt-speaker has been made with the default raspbian audio configuration in mind.
If you are using external sound cards or have installed a sound daemon (like PulseAudio or Jack) you might need to adjust the config file accordingly.

## Usage

The BT-Speaker daemon does not behave like a typical bluetooth device.
Once a client disconnects, the speaker will immediately allow other clients to connect.
This means that the quickest device may claim the speaker and no real bluetooth pairing occurs.
The bright side of this logic is that no button for unpairing is needed.

The speakers name will default to the hostname of your Raspberry Pi.
BT-Speaker does not manage this value.
You are advised to change the hostname according to your needs.

## Config

The default settings of BT-Speaker can be overridden in `/etc/bt_speaker/config.ini`.

Section | Key | Default Value | Description
------------ | ------------- | ------------- | -------------
bt_speaker | play_command | aplay -f cd - | The raw audio in CD Format (16bit little endian, 44100Hz, stereo) is piped to this command.
bt_speaker | connect_command | ogg123 /usr/share/sounds/freedesktop/stereo/service-login.oga | Command that is called when an audio device connects to BT-Speaker
bt_speaker | disconnect_command | ogg123 /usr/share/sounds/freedesktop/stereo/service-logout.oga | Command that is called when an audio device disconnects from BT-Speaker
bluez | device_path | /org/bluez/hci0 | The DBUS path where BT-Speaker can find the bluetooth device
bluez | discoverable | 0 | Disable BT device discovery mode so unknown media sources could not connect. Pair at the beginning and later hide
sonoff | timeout | 15 | Timeout value to wait before switching off media center
sonoff | url_switch_on | http://192.168.1.42/control?cmd=event,T1 | HTTP control command to swtich on Sonoff controller
sonoff | url_switch_off | http://192.168.1.42/control?cmd=event,T0 | HTTP control command to swtich off Sonoff controller
alsa | mixer | PCM | The volume of this mixer will be set from AVRCP messages (Remote volume control). "None" value for DAC audio cards that do not support software mixers
alsa | id | 0 | The alsa id of the mixer control
alsa | cardindex | 0 | The alsa cardindex of the soundcard

The settings in the alsa section specify on which alsa mixer ([more info here](https://larsimmisch.github.io/pyalsaaudio/libalsaaudio.html#mixer-objects)) volume changes are applied.
You need to adjust these settings if you are using an external sound card.

This also support functionality to make controlled post request into power switch (like Sonoff) to turn on or off media center. BT-Speaker daemon now will turn on your media center if someone connects to daemon via Bluetooth and will turn it off after timeout value seconds if connection is dropped and noone else connected. More information how to setup Sonoff switch can be found ([here](http://www.instructables.com/id/Control-Sonoff-From-Raspberry-Pi/))

Example of `/etc/bt_speaker/config.ini`:

```ini
[bt_speaker]
play_command = aplay -f cd -
connect_command = ogg123 /usr/share/sounds/freedesktop/stereo/service-login.oga
disconnect_command = ogg123 /usr/share/sounds/freedesktop/stereo/service-logout.oga

[bluez]
device_path = /org/bluez/hci0
discoverable = 0

[sonoff]
timeout = 15
url_switch_on = http://192.168.1.42/control?cmd=event,T1
url_switch_off = http://192.168.1.42/control?cmd=event,T0

[alsa]
mixer = PCM
id = 0
cardindex = 0
```

## Details of Implementation

The BT-Speaker daemon has been written in Python and works with Bluez5.
It talks to the Bluez daemon via the [Bluez DBUS interface](https://git.kernel.org/cgit/bluetooth/bluez.git/tree/doc).

### Bluetooth profiles

BT-Speaker will register itself as an [A2DP](https://en.wikipedia.org/wiki/List_of_Bluetooth_profiles#Advanced_Audio_Distribution_Profile_.28A2DP.29) capable device and route the received audio fully decoded to ALSAs `aplay` command.

Changes in volume are detected via messages from the [AVRCP](https://en.wikipedia.org/wiki/List_of_Bluetooth_profiles#Audio.2FVideo_Remote_Control_Profile_.28AVRCP.29) profile and are applied directly to the ALSA master volume.

### Notice about Bluetooth device class

Some of TV's will filter out BT-Speaker running RaspberryPi as bluetooth device class will not advertise itself as a speaker. Although BT-Manager does not support to change class you can change it manually after launching BT-Speaker. Launch BT-Speaker and type below and you should then be able to discover your BT-Speaker via your TV:

```ini
pi@raspberrypi:~ $ sudo hciconfig hci0 class 0x240408
```

You can also monitor changed via typing "sudo bluetoothctl" and then "show". More about Bluetooth class can be found ([here](http://bluetooth-pentest.narod.ru/software/bluetooth_class_of_device-service_generator.html))

### Partial Bluez5 port of BT-Manager

The great [BT-Manager](https://github.com/liamw9534/bt-manager) library does (currently) only work with Bluez4.
Changes in the Bluez DBUS API [from version 4 to 5](http://www.bluez.org/bluez-5-api-introduction-and-porting-guide/) were huge and fully porting BT-Manager would have been a too heavy task.
So instead, I extracted all relevant parts and ported them to Bluez5 as good as I could.
Documentation and probably lots of other parts there have yet to be adjusted, so refer to [that code](bt_manager) with caution.

### About the audio stream

The following describes some internals of the audio stream that is transferred via bluetooth.

#### Format

The [Light of Dawn blog](http://www.lightofdawn.org/blog/?viewCat=Bluetooth) describes the format very accurate:

> As it turns out, the audio data is compressed with [SBC codec](http://en.wikipedia.org/wiki/SBC_%28codec%29).
> But I can't just use "sbcdec" tool from SBC package to decode it, as the audio data is encapsulated in A2DP packets, not naked SBC-compressed audio data.
> A2DP packets are RTP packets (referenced by [A2DP specification](https://www.bluetooth.org/en-us/specification/adopted-specifications), and detailed in [this IETF draft](http://tools.ietf.org/html/draft-ietf-payload-rtp-sbc-04)) containing A2DP Media Payload.
> We need to extract the SBC audio data, pass it through SBC decompressor, and only then we get raw audio data that can be sent to ALSA.

Unfortunately there is no media player (or at least I didn't find any) that could handle this 'SBC in RTP' format natively.
However, BT-Manager already provided a C library that takes care of the decoding process.
The decoded output is raw audio data in CD format (16 bit little endian, 44100Hz, stereo) and can be piped to ALSA as mentioned in the blog.

#### Decoding

The C library for the decoding process is located in the [codecs](codecs) folder.
Its functions are called via [Python CFFI](http://cffi.readthedocs.io/en/latest/).
BT-Speaker provides the binary for ARM already, so there is no need to compile the codec manually.

However, if you need to do so for some reason, please be aware that the Makefile has been adjusted by the following:

1. The default `PLATFORM` setting has been changed to `armv6`
1. The `-O3` flag has been added

