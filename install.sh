#!/bin/bash +x
set -e

# This script has been tested with the "2017-11-29-raspbian-stretch-lite.img" image.
#check root privileges
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
###############
echo "Installing dependencies..."
apt-get update
apt-get --yes --force-yes install git bluez python python-gobject python-cffi python-dbus python-alsaaudio python-configparser sound-theme-freedesktop vorbis-tools
echo "done."

# Add btspeaker user if not exist already
echo
echo "Adding btspeaker user..."
id -u btspeaker &>/dev/null || useradd -m btspeaker -G audio
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
ln /opt/bt-speaker/config.ini.default /etc/bt_speaker/config.ini
ln /opt/bt-speaker/hooks.default/connect /etc/bt_speaker/hooks/connect
ln /opt/bt-speaker/hooks.default/disconnect /etc/bt_speaker/hooks/disconnect
ln /opt/bt-speaker/bt_speaker.service /etc/systemd/system/bt_speaker.service



#Menu
opt=""
while [[ $opt != "End" ]]; do
	#clear
	echo '####################  Menu Config options  ####################'
	PS3='Config options: '
	options=("Audio" "Pincode" "Bluetooth" "Bluetooth Enable/Disable" "End")
	select opt in "${options[@]}"
	do
		"Audio")
		    #select audio output
                        echo -e "-------Audio config integrate Raspbery card-------\n"
			AudioOuput="auto,headphones,hdmi,go back"
			oldIFS=$IFS
			IFS=$','
			choices=($AudioOuput)
			IFS=$oldIFS
			PS3="Select your audio output :"
			select answer in "${choices[@]}"; do
			    for item in "${choices[@]}"; do
			       if [[ $item == $answer ]]; then
				    echo "Audio output select:"$answer
		                    break 2;
			       fi
			    done
			done
			if [[ $answer == "go back" ]]; then
			   break
			fi

			Aoutput=$answer
			Pulsedef="/etc/pulse/default.pa"
			if test -f "$Pulsedef"; then
				if  grep -q "load-module module-alsa-sink device=" "$Pulsedef" ; then
                    	           sed -i "s/load-module module-alsa-sink device=             \
				   /load-module module-alsa-sink device=hw:0,0/g" "$Pulsedef"
                  		else
                                   echo -e "load-module module-alsa-sink device=hw:0,0" >> "$Pulsedef"
			       fi
			else
			 echo -e "load-module module-alsa-sink device=hw:0,0" >> "$Pulsedef"
			fi

			if [[ $Aoutput == "auto" ]]; then
			     amixer cset numid=3 0
			else
			     if [[ $Aoutput == "hdmi" ]]; then
				 amixer cset numid=3 2
			     else
				 if [[ $Aoutput == "headphones" ]]; then
				     amixer cset numid=3 1
				 fi
			     fi	
			fi
		    break
		    ;;


		"Pincode")
			#config pincode
                        echo -e "-------Pincode config-------\n"            
			pincode=""
			chrlen=${#pincode}
			while [[ $chrlen -ne 8 ]]
			do
				read -p "Intro your pincode [8 digits] : " pincode
				chrlen=${#pincode}
				echo $chrlen
			done

			sed -i 's/pincode=......../'pincode="$pincode"'/g' /opt/bt-speaker/config.ini.default
			echo Pincode save: $pincode;
		    break
		    ;;

		"Bluetooth config")
			#config bluetooth
                        echo -e "-------Bluetooth config-------\n"            
			btopt=$(hciconfig -a | grep hci | cut -d":" -f1,4 )
			oldIFS=$IFS
			IFS=$'\n'
			choices=($btopt)
			choices+=('Go back')
			IFS=$oldIFS
			PS3="Select your option :"
			select answer in "${choices[@]}"; do
			    for item in "${choices[@]}"; do
			       if [[ $item == $answer ]]; then
				    echo "Bluetooth:"  $answer 
		                    break 2;
			       fi
			    done
			done
			if [[ $answer == "Go back" ]]; then; break;
			
			hcioutput=$(echo $answer | cut  -d":" -f1
			if [[  $answer ==  *"USB"*  ]]; then
			   while true; do
			   read -p "You want disable the internal bluetoothand use the USB dogle? Y/N: "\
			     response
			   case $response in
        		   [Yy]* ) 
			     #disable internal raspberry bluetooth
                             echo "blacklist btbcm" >> /etc/modprobe.d/bluetooth-blacklist.conf 
                             echo "blacklist hci_uart" >> /etc/modprobe.d/bluetooth-blacklist.conf
			     break;;
			   [Nn]* ) break;;
        		    * ) echo "Please answer yes or no.";;
    		     	   esac
			  done	 		
			fi
		 	 #change config
                          sed -i 's/hci./'$hcioutput'/g' /opt/bt-speaker/config.ini.default

		    break
		    ;;

                "Bluetooth Enable/Disable")
			#Enable/Disable internal bluetooth  
			echo "Enable or Disable internal UAR bluetooth"          
			btopt="disable,enable,Go back"
			oldIFS=$IFS
			IFS=$','
			choices=($btopt)
			IFS=$oldIFS
			PS3="Select your option "
			select answer in "${choices[@]}"; do
			    for item in "${choices[@]}"; do
			       if [[ $item == $answer ]]; then
				    echo "Bluetooth internal:"$answer
		                    break 2;
			       fi
			    done
			done
			Btoutput=$answer
			if [[ $Btoutput == "disable" ]]; then
				#disable internal raspberry bluetooth
				echo "blacklist btbcm" >> /etc/modprobe.d/bluetooth-blacklist.conf 
				echo "blacklist hci_uart" >> /etc/modprobe.d/bluetooth-blacklist.conf	
			fi
			if [[ $Btoutput == "enable" ]]; then
				#enable internal raspberry bluetooth
				rm /etc/modprobe.d/bluetooth-blacklist.conf 
			fi

                    break
                    ;;
		"End")
		    break
		    ;;
		*) echo "invalid option $REPLY";;
	    esac
	done

done

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
