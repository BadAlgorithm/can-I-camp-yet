from bs4 import BeautifulSoup
from fbchat import Client
from fbchat.models import *
import os
import pprint
import requests
import time

printer = pprint.PrettyPrinter(indent=4)
camping_homepage = 'https://qpws.usedirect.com/QPWS/Default.aspx'
try_again = True
booking_disabled_message = 'close camping'


def notify():
    email = os.environ.get('FB_EMAIL')
    password = os.environ.get('FB_PASSWORD')
    group_chat_id = os.environ.get('GROUP_CHAT_ID')
    message_link = "Check now: " + camping_homepage
    client = Client(email, password)
    client.send(Message(text='BOT: CAMP BOOKINGS MAY BE OPEN AGAIN!!!'), thread_id=group_chat_id,
                thread_type=ThreadType.GROUP)
    time.sleep(3)
    client.send(Message(text=message_link),
                thread_id=group_chat_id,
                thread_type=ThreadType.USER)
    client.logout()


def check_campsites():
    page = requests.get(camping_homepage)
    soup = BeautifulSoup(page.content, 'html.parser')
    paragraphs = soup.find_all('p')
    paragraph_text = ''.join([paragraph.text for paragraph in paragraphs])
    can_book = booking_disabled_message not in paragraph_text
    print("Can book: {}".format(can_book))
    if can_book:
        notify()
        try_again = False
    else:
        print('not yet')


def start():
    while try_again:
        check_campsites()
        time.sleep(30)
    exit(0)


start()
