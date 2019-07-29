#!/usr/bin/python3.6

"""
A simple comic strip scraper for dilbert.com
"""

import os
import subprocess
import random
import time
import sys
import threading
import colorama
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup as bs
from dateutil.relativedelta import relativedelta


LOGO = """
     _        _             _ _ _ _               _
    | |      (_)           | (_) | |             | |
 ___| |_ _ __ _ _ __     __| |_| | |__   ___ _ __| |_
/ __| __| '__| | '_ \   / _` | | | '_ \ / _ \ '__| __|
\__ \ |_| |  | | |_) | | (_| | | | |_) |  __/ |  | |_ 
|___/\__|_|  |_| .__/   \__,_|_|_|_.__/ \___|_|   \__|
               | |                                    
               |_|                        version: 0.9
"""
DEFAULT_DIR_NAME = "my_dilberts"
COMICS_DIRECTORY = os.path.join(os.getcwd(), DEFAULT_DIR_NAME)
BASE_URL = "https://dilbert.com/strip/"
FIRST_COMIC = date(1989, 4, 16)  # The earliest dilbert comic strip published
NEWEST_COMIC = date.today()


def clear_screen():
    """
    Clears terminal screen
    """
    os.system("cls" if os.name == "nt" else "clear")


def print_progress(
                    iteration, total, prefix='',
                    suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in % complete (Int)
    bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' %
                    (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def human_readable_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def show_logo():
    """
    Displays the ascii logo
    """
    clear_screen()
    bad_colors = ['BLACK', 'LIGHTBLACK_EX', 'RESET']
    colorama.init(autoreset=True)
    codes = vars(colorama.Fore)
    colors = [codes[color] for color in codes if color not in bad_colors]
    colored_logo = [random.choice(colors) + line for line in LOGO.split('\n')]
    print('\n'.join(colored_logo))


def show_main_menu():
    """
    Main download menu
    """
    today = get_today()
    this_week_start, this_week_end = get_this_week()
    comics_this_week = available_comics(this_week_start, this_week_end)
    last_week_start, last_week_end = get_last_week()
    comics_last_week = available_comics(last_week_start, last_week_end)
    this_month_start, this_month_end = get_this_month()
    comics_this_month = available_comics(this_month_start, this_month_end)
    last_month_start, last_month_end = get_last_month()
    comics_last_month = available_comics(last_month_start, last_month_end)

    print("Choose a menu item to download:\n")
    print(f"1. Today's comic strip: {today}")
    print(f"2. This week's strips:  {this_week_start} - {this_week_end} | {comics_this_week} comic(s)")
    print(f"3. Last week's strips:  {last_week_start} - {last_week_end} | {comics_last_week} comics")
    print(f"4. This month's strips: {this_month_start} - {this_month_end} | {comics_this_month} comic(s)")
    print(f"5. Last month's strips: {last_month_start} - {last_month_end} | {comics_last_month} comics")
    print("6. Random comic strip:  ????-??-??")
    print(f"7. Custom date range:  Any date between {FIRST_COMIC} - {NEWEST_COMIC}")
    print("-"*20)
    print("0. Type 0 to Exit.\n")


def get_menu_item(min_range, max_range):
    """
    Takes and checks the main menu selection input
    """
    while True:
        try:
            menu_item = int(input("Type your selection here: "))
        except ValueError:
            print("\nError: expected a number! Try again.\n")
            continue
        if menu_item < min_range:
            print("\nSorry, that didn't work! Try again.\n")
            continue
        elif menu_item > max_range:
            print("\nNo such menu item! Try again.\n")
            continue
        elif menu_item == 0:
            sys.exit()
        else:
            break
    return menu_item


def handle_main_menu(menu_item):
    """
    Handles the main menu and invokes the download engine
    """
    today = get_today()
    number_of_all_dilberts = get_number_of_dilberts_till_now()

    if menu_item == 1:
        download_engine(today, today)
    elif menu_item == 2:
        download_engine(*get_this_week())
    elif menu_item == 3:
        download_engine(*get_last_week())
    elif menu_item == 4:
        download_engine(*get_this_month())
    elif menu_item == 5:
        download_engine(*get_last_month())
    elif menu_item == 6:
        random_comic_date = generate_random_date()
        download_engine(random_comic_date, random_comic_date)
    elif menu_item == 7:
        clear_screen()
        print("NOTE!")
        print(f"Since {FIRST_COMIC.strftime('%d/%b/%Y')}, there has been {number_of_all_dilberts} comics published.")
        print("If you want to download all of them it might take a while.\n")
        print(f"1. Download all comics ({number_of_all_dilberts})!")
        print("2. Enter a custom date range.")
        print("-"*20)
        print("0. Type 0 to Exit.\n")
        handle_minor_menu(get_menu_item(0, 2))


def handle_minor_menu(menu_item):
    """
    Handles the minor menu and invokes the custom date range download engine
    """
    if menu_item == 1:
        download_engine(FIRST_COMIC, NEWEST_COMIC)
    elif menu_item == 2:
        first_strip_date = get_comic_strip_start_date()
        last_strip_date = get_comic_strip_end_date()
        download_engine(first_strip_date, last_strip_date)


def get_today():
    """
    Returns today's date
    """
    today = date.today()
    return today


def get_this_week():
    """
    Returns dates for current week
    """
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    delta = (today - week_start).days
    week_end = week_start + timedelta(days=delta)
    return week_start, week_end


def get_last_week():
    """
    Returns last week's date range
    """
    today = date.today()
    last_week_start = today - timedelta(days=today.weekday(), weeks=1)
    last_week_end = last_week_start + timedelta(days=6)
    return last_week_start, last_week_end


def get_this_month():
    """
    Returns dates for current month
    """
    today = date.today()
    first_day_of_this_month = today.replace(day=1)
    return first_day_of_this_month, today


def get_last_month():
    """
    Returns last month's date range
    """
    today = date.today()
    today_month_ago = today - relativedelta(months=1)
    first_day_of_previous_month = date(
        today_month_ago.year, today_month_ago.month, 1)
    last_day_of_the_previous_month = date(
        today.year, today.month, 1) - relativedelta(days=1)
    return first_day_of_previous_month, last_day_of_the_previous_month


def generate_random_date():
    return FIRST_COMIC + (NEWEST_COMIC - FIRST_COMIC) * random.random()


def get_number_of_dilberts_till_now():
    """
    Counts all the comic strips published since April 16th, 1989
    """
    today = date.today()
    delta = (today - FIRST_COMIC).days + 1
    return delta


def available_comics(start_date, end_date):
    return (end_date - start_date).days + 1


def validate_date():
    while True:
        year, month, day = map(int, input(">> ").split("/"))
        user_date = date(year, month, day)
        if user_date < FIRST_COMIC:
            print("The oldest comic is from 1989/04/16. Try again.")
            continue
        elif user_date > NEWEST_COMIC:
            print("You can't download anything from the future yet!")
            continue
        else:
            break
    return user_date


def get_comic_strip_start_date():
    """
    Asks for initial comic strip date for custom date range
    """
    print("Type a dilbert comic start date in YYYY/MM/DD format:")
    return validate_date()


def get_comic_strip_end_date():
    """
    Asks for final comic strip date for custom date range
    """
    print("Type a dilbert comic end date in YYYY/MM/DD format:")
    return validate_date()


def get_comic_strip_url(start_date, end_date):
    """
    Outputs the comic strip date url
    in the https://dilbert.com/YYYY-MM-DD format
    """
    delta = end_date - start_date
    return [BASE_URL+str(start_date + timedelta(day))
            for day in range(delta.days + 1)]


def get_image_comic_url(response):
    """
    Fetches the comic strip image source url based on the strip url
    """
    soup = bs(response.text, 'html.parser')
    for div in soup.find_all('div', class_="img-comic-container"):
        for a in div.find_all('a', class_="img-comic-link"):
            for img in a.find_all('img', src=True):
                return "https:" + img['src']


def download_dilbert(url):
    """
    Downloads and saves the comic strip
    """
    filne_name = url.split('/')[-1]
    with open(os.path.join(COMICS_DIRECTORY, filne_name), "wb") as file:
        response = requests.get(url)
        file.write(response.content)


def download_engine(first_comic_strip_date, last_comic_strip_date):
    """
    Based on the strip url, fetches the comic image source and downloads it
    """
    start = time.time()

    url_list = get_comic_strip_url(
        first_comic_strip_date, last_comic_strip_date)

    os.makedirs(DEFAULT_DIR_NAME, exist_ok=True)
    counter = 1
    for url in url_list:
        print_progress(
                        counter,
                        len(url_list),
                        prefix="Fetching: " + url[8:],
                        suffix='', bar_length=30)
        response = requests.get(url)
        download_url = get_image_comic_url(response)

        thread = threading.Thread(
            target=download_dilbert, args=(download_url,))
        thread.start()
        thread.join()
        counter += 1

    end = time.time()
    total_time = human_readable_time(int(end - start))
    print(f"{counter - 1} dilbert comics downloaded in {total_time} seconds!")


def main():
    """
    Encapsulates and executes all methods in the main function
    """
    show_logo()
    show_main_menu()
    the_main_menu_item = get_menu_item(0, 7)
    handle_main_menu(the_main_menu_item)


if __name__ == '__main__':
    main()
