import os
import requests
from bs4 import BeautifulSoup
import lxml
from smtplib import SMTP

# target_url = input("Enter link of your target product: ")
target_url = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
# target_price = input("Enter your target price: ")
target_price = 119.95
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 "
                        "Safari/537.36", "Accept-Language": "en-US,en;q=0.9"}

response = requests.get(target_url, headers=header)
sp = BeautifulSoup(response.content, "lxml")
current_price = sp.select_one("#priceblock_ourprice").getText().split("$")[1]
product_title = sp.select_one("#productTitle").getText().strip()

if current_price <= target_price:
    sender_email = os.environ["SENDER_EMAIL"]
    sender_pass = os.environ["SENDER_EMAIL_PASS"]
    receiver_email = "example@yourdomain.com"
    message = (f"Subject:Amazon Price Alert!\n\n{product_title} is now ${current_price}\n{target_url}").encode("UTF-8")

    with SMTP("smtp.mail.yahoo.com") as connection:
        connection.starttls()
        connection.login(user=sender_email, password=sender_pass)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=message
        )
