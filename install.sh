#!/bin/bash +x
set -e

# This script has been tested on 2020/07/19
# OS: Raspbian GNU/Linux 10 (buster)
# Model: Raspberry Pi 3 Model B Rev 1.2

echo "Installing dependencies..."
apt update
apt --yes --force-yes install git bluez python3 python3-gi python3-gi-cairo python3-cffi python3-dbus python3-alsaaudio sound-theme-freedesktop vorbis-tools
echo "done."

# Add btspeaker user if not exist already
echo
echo "Adding btspeaker user..."
id -u btspeaker &>/dev/null || useradd btspeaker -G audio -d /opt/bt_speaker
# Also add user to bluetooth group if it exists (required in debian stretch)
getent group bluetooth &>/dev/null && usermod -a -G bluetooth btspeaker
echo "done."

# Download bt-speaker to /opt (or update if already present)
echo
cd /opt
if [ -d bt-speaker ]; then
  echo "Updating bt-speaker..."
  cd bt-speaker && git pull && git checkout ${1:master}
else
  echo "Downloading bt-speaker..."
  git clone https://github.com/lukasjapan/bt-speaker.git
  cd bt-speaker && git checkout ${1:master}
fi
echo "done."

# Prepare default config
mkdir -p /etc/bt_speaker/hooks
cp -n /opt/bt-speaker/config.ini.default /etc/bt_speaker/config.ini
cp -n /opt/bt-speaker/hooks.default/connect /etc/bt_speaker/hooks/connect
cp -n /opt/bt-speaker/hooks.default/disconnect /etc/bt_speaker/hooks/disconnect
cp -n /opt/bt-speaker/hooks.default/startup /etc/bt_speaker/hooks/startup
cp -n /opt/bt-speaker/hooks.default/track /etc/bt_speaker/hooks/track

# Install and start bt-speaker daemon
echo
echo "Registering and starting bt-speaker with systemd..."
systemctl enable /opt/bt-speaker/bt_speaker.service
if [ "`systemctl is-active bt_speaker`" != "active" ]; then
  systemctl start bt_speaker
else
  systemctl restart bt_speaker
fi
  systemctl status bt_speaker --full --no-pager
echo "done."

# Finished
echo
echo "BT-Speaker has been installed."
