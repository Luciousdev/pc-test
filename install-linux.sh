#!/bin/bash

# Set some colors
CNT="[\033[1;36mNOTE\033[0m]"
COK="[\033[1;32mOK\033[0m]"
CER="[\033[1;31mERROR\033[0m]"
CAT="[\033[1;37mATTENTION\033[0m]"
CWR="[\033[1;35mWARNING\033[0m]"
CAC="[\033[1;33mACTION\033[0m]"
CIN="[\033[1;34mINPUT\033[0m]"
CDE="[\033[1;37mDEBUG\033[0m]"
CPR="[\033[1;37mPROGRESS\033[0m]"


LOG_FILE="install.log"
show_progress() {
  local pid=$1
  local delay=0.2
  local spinstr='|/-\'
  while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
    local temp=${spinstr#?}
    printf " [%c]  " "$spinstr"
    local spinstr=$temp${spinstr%"$temp"}
    sleep $delay
    printf "\b\b\b\b\b\b"
  done
  printf "    \b\b\b\b"
}

log_message() {
  local message="$1"
  echo -e "$message"
  echo -e "$message" >> "$LOG_FILE"
}

log_error() {
  local error_message="$1"
  log_message "\033[1A\033[K$CER - $error_message"
  exit 1
}

log_note() {
  local note_message="$1"
  log_message "$CNT - $note_message"
}

log_progress() {
  local progress_message="$1"
  log_message "$CNT - $progress_message"
  printf "    "
  for _ in {1..5}; do
    printf "."
    sleep 0.5
  done
  sleep 0.5  
  printf "\n"
}





if [ -f /etc/os-release ]; then
  . /etc/os-release

  # Check the value of the ID variable for Arch-based distributions
  if [[ "$ID" == "arch" || "$ID_LIKE" == *"arch"* ]]; then
    log_note "Detected Arch-based Linux distribution"
    
    # Check if yay is already installed
    if ! command -v yay >/dev/null 2>&1; then
      log_note "Configuring yay."
      if ! git clone https://aur.archlinux.org/yay.git &>> "$LOG_FILE"; then
        log_error "Failed to clone yay repository. Please check the internet connection and try again."
      fi
      cd yay || log_error "Failed to navigate to yay directory."
      if ! makepkg -si --noconfirm &>> "../$LOG_FILE"; then
        log_error "Failed to build and install yay. Please check the log file for more details."
      fi
      cd ..
      log_note "Updating yay."
      if ! yay -Suy --noconfirm &>> "$LOG_FILE"; then
        log_error "Failed to update yay. Please check the log file for more details."
      fi
    else
      log_note "yay already configured"
    fi
    
    # Check if Python 3 is installed
    if ! command -v python3 >/dev/null 2>&1; then
      log_note "Installing Python 3.10"
      if ! yay -S --noconfirm --needed python310; then
        log_error "Failed to install Python 3.10. Please check the log file for more details."
      fi
    else
      log_note "Python 3 is installed"
    fi

    # Install Python packages
    log_note "Installing packages."
    if ! pip install -r requirements.txt &>> "$LOG_FILE"; then
      log_error "Failed to install Python packages. Please check the log file for more details."
    fi
    log_note "Packages installed."

    log_note "Running python script."
    python get-data.py
    exit

  elif [[ "$ID" == "debian" || "$ID_LIKE" == *"debian"* ]]; then
    log_note "Detected Debian-based Linux distribution"
    
    # Check if Python 3 is installed
    if ! command -v python3 >/dev/null 2>&1; then
      log_note "Installing Python 3.10"
      if ! sudo apt-get update || ! sudo apt-get install -y python3.10; then
        log_error "Failed to install Python 3.10. Please check the log file for more details."
      fi
    else
      log_note "Python 3 is installed"
    fi

    # Install Python packages
    log_note "Installing packages."
    if ! pip install -r requirements.txt &>> "$LOG_FILE"; then
      log_error "Failed to install Python packages. Please check the log file for more details."
    fi
    log_note "Packages installed."

    log_note "Running python script."
    python get-data.py
    exit

  else
    log_error "Unknown distribution"
  fi
else
  log_error "Couldn't determine the distribution. Aborting installation."
fi
