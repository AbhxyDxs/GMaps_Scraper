# Web Scraper for Google Maps

Python-based web scraper that extracts details from Google Maps using Selenium and BeautifulSoup.

## Features

 - Automates search for tthe given purpose.

 - Extracts details such as name, phone number, address, and website.

 - Saves the data in a CSV file.

## Requirements

Ensure you have the following installed on your system before running the script.

### 1. Install Python

Download and install Python from the [official website](https://www.python.org/downloads/). Make sure to add Python to your system PATH during installation.

### 2. Install pip (Package Manager)

Pip is included in most Python installations. Verify by running:
```sh
python --version
pip --version
```

If pip is not installed, install it manually:
```sh
python -m ensurepip --default-pip
```
### 3. Install Google Chrome

Download and install the latest version of Google Chrome.

### 4. Install ChromeDriver

 - Find the version of your Chrome browser by visiting: `chrome://settings/help`

 - Download the matching [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads) and extract it.

 - Place `chromedriver.exe` in the same directory as the script or add its path to system variables.

### 5. Install Required Python Packages

Run the following command to install the required dependencies:
```sh
pip install selenium beautifulsoup4 pandas
```
## Usage

Clone this repository or download the script.
```sh
git clone https://github.com/AbhxyDxs/GMaps_Scraper.git
cd GMaps_Scraper
```
Run the script using Python:
```sh
python ScraperFinal.py
```
## Customization

 - Modify the purpose variable in the script to search for different businesses or locations.

 - Change the limit parameter in scrape_travel_companies(limit=10) to adjust the number of results scraped.

## Output

The script will generate a CSV file containing the extracted business details.

## Troubleshooting

 - Ensure ChromeDriver version matches your Chrome browser version.

 - If scraping fails, increase time.sleep() values to handle slower internet speeds.

 - Run the script as an administrator if permission errors occur.

## Disclaimer

This script is for educational and research purposes only. Scraping Google Maps may violate their terms of service. Use responsibly.