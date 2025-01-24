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

# Detect the full Chrome version
FULL_CHROME_VERSION=$($STORAGE_DIR/chrome/opt/google/chrome/chrome --version | awk '{print $3}')
echo "DEBUG: Full Chrome version detected: $FULL_CHROME_VERSION"

# Extract major version
CHROME_VERSION=$(echo "$FULL_CHROME_VERSION" | cut -d'.' -f1)
echo "...Detected Chrome major version: $CHROME_VERSION"

# Fallback to a known stable ChromeDriver version if detection fails
KNOWN_CHROMEDRIVER_VERSION="114.0.5735.90"  # Replace with another version if needed
if [[ $CHROME_VERSION -eq 132 ]]; then
  echo "WARN: Detected invalid Chrome version. Falling back to a known stable ChromeDriver version."
  CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/${KNOWN_CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
else
  # Use dynamically detected version
  CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0.0/chromedriver_linux64.zip"
fi

# Download ChromeDriver
if [[ ! -f $STORAGE_DIR/chromedriver ]]; then
  echo "...Downloading ChromeDriver from $CHROMEDRIVER_URL"
  wget -P ./ "$CHROMEDRIVER_URL" || {
    echo "ERROR: Failed to download ChromeDriver. Exiting."
    exit 1
  }
  unzip chromedriver_linux64.zip -d $STORAGE_DIR/chrome
  rm chromedriver_linux64.zip
  mv $STORAGE_DIR/chrome/chromedriver $STORAGE_DIR/
fi

# Increase shared memory for Chrome
echo "...Increasing shared memory for Chrome"
mount -o remount,size=2G /dev/shm || true

# Install Python dependencies
pip install -r requirements.txt
