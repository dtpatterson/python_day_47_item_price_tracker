import requests
from bs4 import BeautifulSoup
import smtplib
import os

# CONST VARIABLES
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

# URL of item you wish to track
url = "https://www.amazon.com/gp/product/B086PNKX2P/ref=ox_sc_saved_title_1?smid=A28P8QPEPQWVRS&psc=1"

# Can be found at https://myhttpheader.com/
header = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    'Accept-Language': "en-US,en;q=0.9"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

price = soup.find(class_="a-offscreen").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 23.99

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
        connection.starttls()
        result = connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )