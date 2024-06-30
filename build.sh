#!/usr/bin/env bash
set -o errexit

# Download and install Chrome
if [[ ! -d /opt/render/project/bin/chrome ]]; then
  echo "...Downloading Chrome"
  wget -P /tmp https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  mkdir -p /opt/render/project/bin/chrome
  dpkg -x /tmp/google-chrome-stable_current_amd64.deb /opt/render/project/bin/chrome
  rm /tmp/google-chrome-stable_current_amd64.deb
fi

# Download and install Chromedriver
if [[ ! -f /opt/render/project/bin/chromedriver ]]; then
  echo "...Downloading Chromedriver"
  wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
  unzip /tmp/chromedriver.zip chromedriver -d /opt/render/project/bin
  rm /tmp/chromedriver.zip
fi

# Install Python packages
pip install -r requirements.txt
