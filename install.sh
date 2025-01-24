#!/bin/bash

# Exit on error
set -e

echo "Starting installation process..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed"
fi

# Check if Python 3.6.1 is installed via pyenv
if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    brew install pyenv
    
    # Add pyenv to shell
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    
    source ~/.zshrc
else
    echo "pyenv is already installed"
fi

# Install Python 3.6.1
echo "Installing Python 3.6.1..."
pyenv install -s 3.6.1
pyenv global 3.6.1

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download and install chromedriver matching Chrome version
echo "Checking Chrome version..."
CHROME_VERSION=$(defaults read /Applications/Google\ Chrome.app/Contents/Info.plist CFBundleShortVersionString)
CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1)

echo "Installing chromedriver for Chrome version $CHROME_MAJOR_VERSION..."
cd /tmp
curl -LO "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/mac-x64/chromedriver-mac-x64.zip"
unzip -o chromedriver-mac-x64.zip
sudo mv chromedriver-mac-x64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm -rf chromedriver-mac-x64*

echo "Installation complete! You can now run the script using:"
echo "python main.py"
