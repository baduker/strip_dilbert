#!/usr/bin/python3.6

import os
import time
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta

DEFAULT_DIR_NAME = "dilbert"
COMICS_DIRECTORY = os.path.join(os.getcwd(), DEFAULT_DIR_NAME)

BASE_URL = "https://dilbert.com/strip/"

FIRST_COMIC = date(1989, 4, 16)  # start date

def get_comic_strip_start_date():
	print("Type a dilbert comic start date in YYYY/MM/DD format:")
	while True:
		start_year, start_month, start_day = map(int, input(">> ").split("/"))
		start_date = date(start_year, start_month, start_day)
		if start_date < FIRST_COMIC:
			print("The oldest comic is from 1989/04/16. Try again.")
			continue
		elif start_date > date.today():
			print("You can't download anything from the future yet. Try again.")
			continue
		else:
			break
	return start_date

def get_comic_strip_end_date():
	print("Type a dilbert comic end date in YYYY/MM/DD format:")
	while True:
		end_year, end_month, end_day = map(int, input(">> ").split("/"))
		end_date = date(end_year, end_month, end_day)
		if end_date < FIRST_COMIC:
			print("The oldest comic is from 1989/04/16. Try again.")
			continue
		elif end_date > date.today():
			print("You can't download anything from the future yet. Try again.")
			continue
		else:
			break
	return end_date

def get_comic_strip_url(start_date, end_date):
  full_url = []
  delta = end_date - start_date
  for day in range(delta.days + 1):
    full_url.append(BASE_URL+str(start_date + timedelta(day)))
  return full_url


def get_image_comic_url(session, response):
  soup = bs(response.text, 'html.parser')
  for div in soup.find_all('div', class_="img-comic-container"):
    for a in div.find_all('a', class_="img-comic-link"):
      for img in a.find_all('img', src=True):
        return "http:" + img['src']

def download_dilbert(s, u):
  filne_name = u.split('/')[-1]
  with open(os.path.join(COMICS_DIRECTORY, filne_name), "wb") as file:
    response = s.get(u)
    file.write(response.content)

first_strip_date = get_comic_strip_start_date()
last_strip_date = get_comic_strip_end_date()

start = time.time()

url_list = get_comic_strip_url(first_strip_date, last_strip_date)

os.mkdir(DEFAULT_DIR_NAME)

for url in url_list:
	session = requests.Session()
	response = session.get(url)
	download_url = get_image_comic_url(session, response)

	pbar = tqdm(range(len(url_list)))

	for i in pbar:
		pbar.set_description("Fetching {}".format(url[8:]))
		download_dilbert(session, download_url)
		

end = time.time()

print("Files downloaded in {:.2f} seconds!".format(end - start))