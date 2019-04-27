#!/usr/bin/python3.6

import re
import os
import requests
from bs4 import BeautifulSoup as bs

DEFAULT_DIR_NAME = "dilbert"
COMICS_DIRECTORY = os.path.join(os.getcwd(), DEFAULT_DIR_NAME)

BASE_URL = "https://dilbert.com/"
DATE = "1989-04-16"

SEARCH_DATE = BASE_URL+DATE
COMIC_PATTERN = re.compile(r'https://assets.amuniversal.com/.+')

def grab_url(s, r):
  counter = 0
  soup = bs(response.text, 'html.parser')
  for div in soup.find_all('div', class_="img-comic-container"):
    for a in div.find_all('a', class_="img-comic-link"):
      for img in a.find_all('img', src=True):
        return img['src']

def download_dilber(s, u):
	filne_name = u.split('/')[-1]
	with open(os.path.join(COMICS_DIRECTORY, filne_name), "wb") as file:
		response = s.get(u)
		file.write(response.content)

session = requests.Session()
response = session.get(SEARCH_DATE)

url = "http:" + grab_url(session, response)

os.mkdir(DEFAULT_DIR_NAME)

download_dilber(session, url)

