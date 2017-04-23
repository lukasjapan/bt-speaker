#!/bin/bash
set -e

# This script has been tested with the "2017-01-11-raspbian-jessie-lite.img" image.

# Install dependencies
apt-get update
apt-get install git bluez python python-gobject python-cffi python-dbus python-alsaaudio python-configparser sound-theme-freedesktop vorbis-tools

# Add btspeaker user if not exist already
id -u btspeaker &>/dev/null || useradd btspeaker -G audio

# Download bt-speaker to /opt
cd /opt
git clone https://github.com/lukasjapan/bt-speaker.git

# Install and start bt-speaker daemon
systemctl enable /opt/bt-speaker/bt_speaker.service
systemctl start bt_speaker