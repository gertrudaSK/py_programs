import csv
from bs4 import BeautifulSoup
import requests
import re
import os
import pathlib
import pandas as pd
import smtplib
from email.message import EmailMessage
from email_settings import email_address, password


def best_deals():
    file = pathlib.Path('shoes_offers.csv')
    if file.exists():
        try:
            os.remove('shoes_offers_past.csv')
        except FileNotFoundError:
            pass
        os.rename('shoes_offers.csv', 'shoes_offers_past.csv')
    else:
        pass
    check_prices()


def clean_number(text):
    pattern = re.compile(r'\d+.\d{2}')
    result = pattern.findall(text)
    return result[0]


def check_prices():
    try:
        with open('shoes_offers.csv', 'r+')as f:
            f.close()
    except:
        with open('shoes_offers.csv', 'a', newline='')as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Brand', 'Price Current', 'Price Before', 'Description'])
            file.close()

    try:
        for n in range(1, 4):
            source = requests.get(
                f'https://www.fashiola.co.uk/cheap/boys/shoes/?mt=8|8.5|25|26&p={n}&prmax=30&prmin=10&sale=70').text
            soup = BeautifulSoup(source, 'html.parser')
            blocks = soup.find_all('li', class_='item')

            with open('shoes_offers.csv', 'a', encoding="UTF-8", newline='')as file:
                csv_writer = csv.writer(file)
                for block in blocks:
                    brand = block.find('div', class_='brandtitle').span.text
                    price_cur = block.find('div', class_='price sale').span.text
                    price_current = clean_number(price_cur)
                    price_bef = block.find('del', class_='before').text
                    price_before = clean_number(price_bef)
                    description = block.find('span', class_='title').text
                    csv_writer.writerow([brand, price_current, price_before, description])
    except Exception:
        pass
    compare_prices()


def send_email():
    message = '''
    Hey!

    Check out the best prices. See attached file!
    '''

    email = EmailMessage()
    email['from'] = "Chuck's Computer"
    email['to'] = email_address
    email['subject'] = 'The price has already dropped!'

    email.set_content(message)

    with open('best_prices.csv', 'rb') as f:
        content = f.read()
        filename = f.name
        email.add_attachment(
            content,
            maintype='text/plain',
            subtype='plain',
            filename=filename)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(email_address, password)
        smtp.send_message(email)


def compare_prices():
    try:
        f1 = pd.read_csv('shoes_offers.csv', encoding='ISO-8859-1')
        f2 = pd.read_csv('shoes_offers_past.csv', encoding='ISO-8859-1')
        new = pd.merge(f1, f2, on=['Description', 'Price Before'])
        new['price_difference'] = new['Price Current_x'] - new['Price Current_y']
        drop_price = new.loc[new['price_difference'] <= -1]
        w = new.loc[new['price_difference'] <= -10]
        if not w.empty:
            w.to_csv('best_prices.csv', index=False)
            send_email()

        drop_price.to_csv('compare_prices.csv', index=False)
    except FileNotFoundError:
        pass


best_deals()
