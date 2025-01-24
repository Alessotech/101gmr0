#!/usr/bin/env bash
# Exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/.render

# Install Chrome if not already installed
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

# Detect the full Chrome version (e.g., 114.0.5735.90)
FULL_CHROME_VERSION=$($STORAGE_DIR/chrome/opt/google/chrome/chrome --version | awk '{print $3}')
echo "...Detected full Chrome version: $FULL_CHROME_VERSION"

# Extract only the major version (e.g., 114)
CHROME_VERSION=$(echo "$FULL_CHROME_VERSION" | cut -d'.' -f1)
echo "...Detected Chrome major version: $CHROME_VERSION"

# Download the matching ChromeDriver version
if [[ ! -f $STORAGE_DIR/chromedriver ]]; then
  echo "...Downloading ChromeDriver for Chrome version $CHROME_VERSION"
  wget -P ./ "https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0.0/chromedriver_linux64.zip"
  unzip chromedriver_linux64.zip -d $STORAGE_DIR/chrome
  rm chromedriver_linux64.zip
  mv $STORAGE_DIR/chrome/chromedriver $STORAGE_DIR/
fi

# Install Python dependencies
pip install -r requirements.txt
