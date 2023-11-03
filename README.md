Lowest Rent Finder

Overview

This Python script checks the lowest price for apartments for rent on Zillow, based on a specified link with filters. The script uses BeautifulSoup for web scraping to extract relevant information.

Prerequisites

Before running the script, make sure you have the following:

Python installed (version 3.6 or higher)
Required Python packages installed (requests, beautifulsoup4, twilio)

Configuration

Create a config.json file in the root of your project with the following structure:

json
Copy code
{
  "TWILIO_ACCOUNT_SID": "your_twilio_account_sid",
  "TWILIO_AUTH_TOKEN": "your_twilio_auth_token",
  "TWILIO_NUM": "your_twilio_phone_number",
  "MY_NUM": "your_phone_number",
  "USER_AGENT": "your_user_agent",
  "ACCEPT_LANGUAGE": "your_accept_language"
}
Replace the placeholder values with your actual Twilio credentials, phone numbers, user agent, and accept language.

How to Run

Open a terminal or command prompt.
Navigate to the project directory.
Run the script:
bash
Copy code
python main.py
The script will fetch the data, analyze it, and send a Twilio SMS with information about the lowest-priced apartment meeting your criteria.


