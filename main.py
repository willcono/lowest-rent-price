import json
from bs4 import BeautifulSoup
from twilio.rest import Client
import requests

with open("config.json","r") as raw:
    data = json.load(raw)

ACCOUNT_SID = data["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = data["TWILIO_AUTH_TOKEN"]
TWILIO_NUM = data["TWILIO_NUM"]
MY_NUM = data["MY_NUM"]

ZILLOW_URL = "https://www.zillow.com/pasadena-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-118.23032913037108%2C%22east%22%3A-118.03326186962889%2C%22south%22%3A34.07181676286283%2C%22north%22%3A34.29306395703698%7D%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A47019%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22price%22%3A%7B%22min%22%3Anull%2C%22max%22%3A423030%7D%2C%22mp%22%3A%7B%22min%22%3Anull%2C%22max%22%3A2400%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3Anull%7D%2C%22baths%22%3A%7B%22min%22%3A1%2C%22max%22%3Anull%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

headers = {
    "User-Agent": data["USER_AGENT"],
    "Accept-Language": data["ACCEPT_LANGUAGE"]
}
response = requests.get(url=ZILLOW_URL, headers=headers)
response.raise_for_status()
data = response.text

soup = BeautifulSoup(data, "html.parser")

right_panel = soup.find('ul', class_='List-c11n-8-84-3__sc-1smrmqp-0 StyledSearchListWrapper-srp__sc-1ieen0c-0 doa-doM fgiidE photo-cards').find_all('li')
links = list(filter(None, [link.find('a')['href'] if link.find('a') else None for link in right_panel]))
addresses = list(filter(None, [address.find('address').get_text() if address.find('address') else None for address in right_panel]))
prices = list(filter(None, [price.find('span').get_text().strip("/mo") if price.find('span') else None for price in right_panel]))

msg_dict = []
for link, address, price in zip(links, addresses, prices):
    apt_data = {
        "Address": address,
        "Price": price,
        "Link": link,
    }
    msg_dict.append(apt_data)

# print(msg_dict)

int_prices = []
def compare_prices(prices):
    for price in prices:
        price = price.strip("$").replace(",","")
        if "+" in price:
            plus_index = price.find("+")
            price = price[:plus_index]
            int_prices.append(int(price))
        int_prices.append(int(price))

compare_prices(prices)
lowest_price = sorted(int_prices)[0]
def get_apartment(lowest_price, msg_dict):
    for location in msg_dict:
        full_price = str(lowest_price)[0] + "," + str(lowest_price)[1:]

        if str(full_price) in location["Price"]:
            return location
apartment = get_apartment(lowest_price,msg_dict)

formatted_message = ("Lowest apartment for today in Pasadena alert!\n"
                    f"Price: {apartment['Price']}\n"
                     f"Address: {apartment['Address']}\n"
                     f"Link: {apartment['Link']}\n"
                     )

client = Client(ACCOUNT_SID, AUTH_TOKEN)

message = client.messages \
    .create(
    body=formatted_message,
    from_='+'+TWILIO_NUM,
    to='+'+MY_NUM
)
print(message.status)