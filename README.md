# strip_dilbert
A simple comic strip scraper for dilbert.com
~~~
     _        _             _ _ _ _               _   
    | |      (_)           | (_) | |             | |  
 ___| |_ _ __ _ _ __     __| |_| | |__   ___ _ __| |_ 
/ __| __| '__| | '_ \   / _` | | | '_ \ / _ \ '__| __|
\__ \ |_| |  | | |_) | | (_| | | | |_) |  __/ |  | |_ 
|___/\__|_|  |_| .__/   \__,_|_|_|_.__/ \___|_|   \__|
               | |                                    
               |_|                 version: 0.7 | 2019
~~~

**What is strip_dilbert.py?**

*strip_dilbert* is a simple image scraper written in Python for the well-known [dilbert.com](https://dilbert.com) comic website.

**What does it do?**

The idea is to download the dilbert comic strip(s) for any day that the comics have been published, starting from 16th April 1989 all the way till now.

The script has a number of options, letting the user get the comics for the current week or month, for example.

## Here's what the main menu contains:

:+1: all features implemented and working!

1. **Today's comic strip:** *Downloads the comic for today* 
2. **This week's strips:** *Downloads the comics for the current week - up till the current day* 
3. **Last week's strips:** *Downloads the comics for last week* 
4. **This month's strips:** *Downloads the comics for the current month - up till the current day* 
5. **Last month's strips:** *Downloads all the comics for the previous month* 
6. **Custom date range:** *Let's the user set the download date range (16/Apr/1989 - NOW)* 

So, hopefully there are going to be some opportutnies for you with this script. ;)

[![opportunity.png](https://assets.amuniversal.com/505f94006cbc01301d46001dd8b71c47)](https://dilbert.com/strip/2009-09-24)

## WORK PROGRESS:

- [x] DONE! :collision:
- [ ] TO-DO :shit:

**What's been done and what is still to be done:**
- [x] Implement custom date range menu item (it's working but kinda slow)
- [x] Implement all the main menu items
- [x] Comment all the code
- [x] Write a proper counting method for available comic strips
- [x] Reorder ale the methods and implement `if __name__ == '__main__':`
- [x] Improve the `os.mkdir(DEFAULT_DIR_NAME)` method to accept that the folder exists already
- [x] Add `get random comic strip` method
- [x] Improve the performance of the `download_engine()` method to get all the dilberts
- [ ] Implement a list of source URL's with the date/name of the comic and find a way to store it
- [x] Improve / change the progress bar