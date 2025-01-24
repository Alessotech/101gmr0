#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src # Return to project directory
else
  echo "...Using Chrome from cache"
fi

# Download ChromeDriver matching the installed Chrome version
CHROME_VERSION=$($STORAGE_DIR/chrome/opt/google/chrome/chrome --version | awk '{print $3}' | cut -d'.' -f1)
echo "...Detected Chrome version: $CHROME_VERSION"

if [[ ! -f $STORAGE_DIR/chromedriver ]]; then
  echo "...Downloading ChromeDriver"
  wget -P ./ "https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0/chromedriver_linux64.zip"
  unzip chromedriver_linux64.zip -d $STORAGE_DIR/chrome
  rm chromedriver_linux64.zip
  mv $STORAGE_DIR/chrome/chromedriver $STORAGE_DIR/
fi

# Install Python dependencies
pip install -r requirements.txt
