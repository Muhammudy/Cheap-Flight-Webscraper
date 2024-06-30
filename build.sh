#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Chrome
if [[ ! -d /opt/render/project/.render/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p /opt/render/project/.render/chrome
  wget -P /opt/render/project/.render/chrome https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x /opt/render/project/.render/chrome/google-chrome-stable_current_amd64.deb /opt/render/project/.render/chrome
  rm /opt/render/project/.render/chrome/google-chrome-stable_current_amd64.deb
else
  echo "...Using Chrome from cache"
fi

# Install ChromeDriver
if [[ ! -f /opt/render/project/.render/chromedriver ]]; then
  echo "...Downloading ChromeDriver"
  wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
  unzip /tmp/chromedriver.zip chromedriver -d /opt/render/project/.render
  rm /tmp/chromedriver.zip
else
  echo "...Using ChromeDriver from cache"
fi

# Add Chrome to PATH
export PATH="/opt/render/project/.render/chrome/opt/google/chrome:$PATH"
export CHROME_PATH="/opt/render/project/.render/chrome/opt/google/chrome"
export CHROMEDRIVER_PATH="/opt/render/project/.render/chromedriver"

# Install Python dependencies
pip install -r requirements.txt
