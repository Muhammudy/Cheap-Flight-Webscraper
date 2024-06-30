#!/usr/bin/env bash
set -o errexit

CHROME_PATH=/opt/render/project/bin/chrome/opt/google/chrome/

if [[ ! -d $CHROME_PATH ]]; then
    echo "...Downloading Chrome Binary..."
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P /tmp
    echo "...Installing Chrome Binary..."
    mkdir -p /opt/render/project/bin/chrome
    dpkg -x /tmp/google-chrome-stable_current_amd64.deb /opt/render/project/bin/chrome
    rm /tmp/google-chrome-stable_current_amd64.deb
    export PATH="${PATH}:${CHROME_PATH}"
fi

CHROMEDRIVER_PATH=/opt/render/project/bin/chromedriver

if [[ ! -d $CHROMEDRIVER_PATH ]]; then
    echo "...Downloading Chromedriver..."
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
    unzip /tmp/chromedriver.zip chromedriver -d /opt/render/project/bin
    rm /tmp/chromedriver.zip
    export PATH="${PATH}:${CHROMEDRIVER_PATH}"
fi

pip install -r requirements.txt
