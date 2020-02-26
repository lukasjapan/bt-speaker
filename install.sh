#!/bin/bash +x
set -e

# This script has been tested with the "2017-11-29-raspbian-stretch-lite.img" image.
#check root privileges
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
###############
echo "Checking if bt_speaker.service is running..."
if [ "`systemctl is-active bt_speaker.service`" == "active" ]; then
  echo  "Stop service .."
  systemctl stop bt_speaker.service
  systemctl disable bt_speaker.service
fi
#################################
echo "Installing dependencies..."
apt-get update
apt-get --yes --force-yes install git bluez python python-gobject python-cffi python-dbus python-alsaaudio python-configparser sound-theme-freedesktop vorbis-tools libasound2-dev libavformat-dev libavcodec-dev  pulseaudio pulseaudio-module-bluetooth
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
  git clone https://github.com/amerinoj/bt-speaker.git
  cd bt-speaker && git checkout ${1:master}
fi
echo "done."  

# Prepare default config
sudo -u btspeaker pulseaudio  --start
sudo -u btspeaker pulseaudio  --kill 

mkdir -p /etc/bt_speaker/hooks
Etcfg="/etc/bt_speaker/config.ini"      
Hookc="/etc/bt_speaker/hooks/connect"
Hookd="/etc/bt_speaker/hooks/disconnect"
Srvf="/etc/systemd/system/bt_speaker.service"
if test -f "$Etcfg"; then
    rm $Etcfg
fi
if test -f "$Hookc"; then
    rm $Hookc
fi
if test -f "$Hookd"; then
    rm $Hookd
fi
if test -f "$Srvf"; then
    rm $Srvf
fi

ln /opt/bt-speaker/config.ini.default $Etcfg
ln /opt/bt-speaker/hooks.default/connect $Hookc
ln /opt/bt-speaker/hooks.default/disconnect $Hookd


# Config pulse audio
Pulsedef="/etc/pulse/default.pa"
Pulsenew="/home/btspeaker/.config/pulse/default.pa"
if test -f "$Pulsedef"; then

        sudo -u btspeaker cp $Pulsedef $Pulsenew

	if  grep -q "load-module module-alsa-sink device=" "$Pulsedef" ; then
                 sed -i "s/load-module module-alsa-sink device=             \
                 /load-module module-alsa-sink device=hw:0,0/g" "$Pulsenew"
        else
                 echo -e "load-module module-alsa-sink device=hw:0,0" >> "$Pulsenew"
        fi
else
        echo -e "ERROR DEFAULT PULSEAUDIO CONFIG NO FOUND"
fi
#disable to default
sed -i "/load-module module-bluetooth-policy/c\#load-module module-bluetooth-policy" "$Pulsenew"
sed -i "/load-module module-bluetooth-discover/c\#load-module module-bluetooth-discover" "$Pulsenew"
sed -i "/load-module module-bluetooth-policy/c\#load-module module-bluetooth-policy" "/etc/pulse/default.pa"
sed -i "/load-module module-bluetooth-discover/c\#load-module module-blueth-discover" "/etc/pulse/default.pa"

#Menu
opt=""
while [[ $opt != "End" ]]; do
	#clear
	echo '####################  Menu Config options  ####################'
	PS3='Config options: '
	options=("Audio" "Pincode" "Bluetooth config" "Bluetooth Enable/Disable" "Headset Enable/Disable" "End")
	select opt in "${options[@]}"
	do
	   case $opt in
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

			if [[ $Aoutput == "auto" ]]; then
			     sudo -u btspeaker amixer cset numid=3 0
			else
			     if [[ $Aoutput == "hdmi" ]]; then
				 sudo -u btspeaker amixer cset numid=3 2
			     else
				 if [[ $Aoutput == "headphones" ]]; then
				     sudo -u btspeaker amixer cset numid=3 1
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
                        echo  "-------Bluetooth config-------\n"            
			btopt="$(hciconfig -a | grep hci | cut -d":" -f1,4)"
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

			if [[ $answer == "Go back" ]]; then
			   break;
			fi
			
			hcioutput="$(echo "$answer" | cut  -d":" -f1)"
			if [[  $answer ==  *"USB"*  ]]; then
			   while true; do
			   read -p "You want disable the internal bluetooth and use the USB dogle? Y/N: "\
			     response
			   case $response in
        		   [Yy]* ) 
			     #disable internal raspberry bluetooth
                             echo "blacklist btbcm" >> /etc/modprobe.d/bluetooth-blacklist.conf 
                             echo "blacklist hci_uart" >> /etc/modprobe.d/bluetooth-blacklist.conf
                             echo
                             echo "NOTICE: "
                             echo "REBOOT THE SYSTEM and LAUNCH THE INSTALLATION AGAIN"
                             echo "RE-ENTER AGAIN IN [ Bluetooth config ]"
			     break;;
			   [Nn]* ) break;;
        		    * ) echo "Please answer yes or no.";;
    		     	   esac
			  done
			  else
				(hcitool cmd 0x3F 0x01C 0x01 0x02 0x00 0x01 0x01 &)	 		
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
                                echo
                                echo "NOTICE:"
                                echo "REBOOT THE SYSTEM and LAUNCH THE INSTALLATION AGAIN"
                                echo "RE-ENTER AGAIN IN [ Bluetooth config ]" 	
			fi
			if [[ $Btoutput == "enable" ]]; then
				#enable internal raspberry bluetooth
				rm /etc/modprobe.d/bluetooth-blacklist.conf 
			fi

                    break
                    ;;
                "Headset Enable/Disable")
                        #Enable/Disable headset in pulseaudio  
                        echo -e "\n!!! Before enable headset profile make sure have a mic in your system !!!\n"          
                        hsopt="disable,enable,Go back"
                        oldIFS=$IFS
                        IFS=$','
                        choices=($hsopt)
                        IFS=$oldIFS
                        PS3="Select your option "
                        select answer in "${choices[@]}"; do
                            for item in "${choices[@]}"; do
                               if [[ $item == $answer ]]; then
                                    echo "Headset:"$answer
                                    break 2;
                               fi
                            done
                        done
			if [[ $answer == "Go back" ]]; then
			  break
          		fi
                        if [[ $answer == "disable" ]]; then
                          #disable bluetooth pulse audio profile
                          sed -i "/load-module module-bluetooth-policy/c\#load-module module-bluetooth-policy" "$Pulsenew"
			  sed -i "/load-module module-bluetooth-discover/c\#load-module module-bluetooth-discover" "$Pulsenew"
			  sed -i "/ExecStartPre=pulseaudio -D/c\#ExecStartPre=pulseaudio -D" /opt/bt-speaker/bt_speaker.service
                        fi
                        if [[ $answer == "enable" ]]; then
                            #enable bluetooth pulse audio profile
                           sed -i "/load-module module-bluetooth-policy/c\load-module module-bluetooth-policy" "$Pulsenew"
			   sed -i "/load-module module-bluetooth-discover/c\load-module module-bluetooth-discover" "$Pulsenew"
			   sed -i "/ExecStartPre=pulseaudio -D/c\ExecStartPre=pulseaudio -D" /opt/bt-speaker/bt_speaker.service
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
  ln /opt/bt-speaker/bt_speaker.service /etc/systemd/system/bt_speaker.service
  systemctl daemon-reload
  systemctl enable bt_speaker.service
  systemctl start bt_speaker.service
  systemctl status bt_speaker.service  --full --no-pager
echo "done."

# Finished
echo
echo "BT-Speaker has been installed."
echo "Reboot the system  to finish."

