# HCM Realestate Scraper

## Introduction
This is a web scraping tool designed to extract real estate information from realestate websites. The scraper uses Selenium WebDriver with Chrome in headless mode to automatically collect property listings data including titles, prices, and locations.

## Installation

### Prerequisites
- macOS
- Google Chrome browser
- Python 3.6.1 (will be installed via the installation script)

### Installation Steps
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd BDS
   ```

2. Make the installation script executable:
   ```bash
   chmod +x install.sh
   ```

3. Run the installation script:
   ```bash
   ./install.sh
   ```

The installation script will automatically:
- Install Homebrew (if not already installed)
- Install pyenv and Python 3.6.1
- Install required Python packages
- Download and install the appropriate chromedriver version
- Set up all necessary environment variables

## Usage

To run the scraper:
```bash
python main.py
```

The script will:
1. Launch Chrome in headless mode
2. Navigate to the specified realestate URL
3. Extract property information including:
   - Property titles
   - Prices
   - Locations
4. Print the extracted information to the console

### Output Format
For each property listing, the output will be formatted as:
```
Title: [Property Title]
Price: [Price]
Location: [Location]
----------------------------------------
```

## Note
This tool is for educational purposes only. Please ensure you comply with BatDongSan.com.vn's terms of service and implement appropriate delays between requests to avoid overwhelming their servers.