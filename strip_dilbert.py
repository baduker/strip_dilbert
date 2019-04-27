#!/usr/bin/python3.6

import os
import requests
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta

DEFAULT_DIR_NAME = "dilbert"
COMICS_DIRECTORY = os.path.join(os.getcwd(), DEFAULT_DIR_NAME)

BASE_URL = "https://dilbert.com/strip/"

d1 = date(1989, 4, 16)  # start date
d2 = date(1989, 4, 30)  # end date

def grab_comic_strip_url(start_date, end_date):
  full_url = []
  delta = end_date - start_date
  for day in range(delta.days + 1):
    full_url.append(BASE_URL+str(start_date + timedelta(day)))
  return full_url


def get_download_src_url(session, response):
  soup = bs(response.text, 'html.parser')
  for div in soup.find_all('div', class_="img-comic-container"):
    for a in div.find_all('a', class_="img-comic-link"):
      for img in a.find_all('img', src=True):
        return img['src']

def download_dilbert(s, u):
  filne_name = u.split('/')[-1]
  with open(os.path.join(COMICS_DIRECTORY, filne_name), "wb") as file:
    response = s.get(u)
    file.write(response.content)

url_list = grab_comic_strip_url(d1, d2)

os.mkdir(DEFAULT_DIR_NAME)

for url in url_list:
  session = requests.Session()
  response = session.get(url)
  download_url = "http:" + get_download_src_url(session, response)
  download_dilbert(session, download_url)

print("Files downloaded!")