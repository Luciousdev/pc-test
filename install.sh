#!/bin/bash

# set some colors
CNT="[\033[1;36mNOTE\033[0m]"
COK="[\033[1;32mOK\033[0m]"
CER="[\033[1;31mERROR\033[0m]"
CAT="[\033[1;37mATTENTION\033[0m]"
CWR="[\033[1;35mWARNING\033[0m]"
CAC="[\033[1;33mACTION\033[0m]"

if [ -f /etc/os-release ]; then
    . /etc/os-release

    # Check the value of the ID variable for Arch-based distributions
    if [[ "$ID" == "arch" || "$ID_LIKE" == *"arch"* ]]; then
        echo -e "\033[1A\033[K$COK - Detected Arch-based Linux distribution"
        if [ ! -f /sbin/yay ]; then  
            echo -en "$CNT - Configuring yay."
            git clone https://aur.archlinux.org/yay.git &>> $INSTLOG
            cd yay
            makepkg -si --noconfirm &>> ../$INSTLOG &
            show_progress $!
            if [ -f /sbin/yay ]; then
                echo -e "\033[1A\033[K$COK - yay configured"
                cd ..
                
                echo -en "$CNT - Updating yay."
                yay -Suy --noconfirm &>> $INSTLOG &
                show_progress $!
                echo -e "\033[1A\033[K$COK - yay updated."
            else
                echo -e "\033[1A\033[K$CER - yay install failed, please check the install.log"
                exit
            fi
        else 
            echo -e "\033[1A\033[K$COK - yay already configured"
        fi

        if [command -v python3 >/dev/null 2>&1 && echo Python 3 is installed ]; then
            echo -e "\033[1A\033[K$COK - Python 3 is installed"
        else
            echo -e "\033[1A\033[K$CWR - Installing python version 3.10"
            yay -S --noconfirm --needed python310 
            exit
        fi

        # install the packages
        echo -en "$CNT - Installing packages."
        pip install -r requirements.txt
        echo -e "\033[1A\033[K$COK - Packages installed."

        echo -en "$CNT - Running python script."
        python get-data.py
        exit

    elif [[ "$ID" == "debian" || "$ID_LIKE" == *"debian"* ]]; then
        echo "[OK] - Detected Debian-based Linux distribution"
        
    else
        echo "Unknown distribution"
    fi
else
    echo "[ERROR] - Couldn't determine the distribution"
fi
