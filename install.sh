#!/bin/bash
set -e

# This script has been tested with the "2017-09-07-raspbian-stretch-lite.img" image.

echo "Installing dependencies..."
apt-get update
apt-get install git bluez python python-requests python-gobject python-cffi python-dbus python-alsaaudio python-configparser sound-theme-freedesktop vorbis-tools
echo "done."

# Add btspeaker user if not exist already
echo
echo "Adding btspeaker user..."
id -u btspeaker &>/dev/null || useradd btspeaker -G audio
# Also add user to bluetooth group if it exists (required in debian stretch)
getent group bluetooth &>/dev/null && usermod -a -G bluetooth btspeaker
echo "done."

# Download bt-speaker to /opt (or update if already present)
echo
cd /opt
if [ -d bt-speaker ]; then
  echo "Updating bt-speaker..."
  cd bt-speaker && git pull
else
  echo "Downloading bt-speaker..."
  git clone https://github.com/lukasjapan/bt-speaker.git
fi
echo "done."

# Install and start bt-speaker daemon
echo
echo "Registering and starting bt-speaker with systemd..."
systemctl enable /opt/bt-speaker/bt_speaker.service
if [ "`systemctl is-active bt_speaker`" != "active" ]; then
  systemctl start bt_speaker
else
  systemctl restart bt_speaker
fi
systemctl status bt_speaker
echo "done."

# Finished
echo
echo "BT-Speaker has been installed."
