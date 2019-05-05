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
               |_|             version: beta | 05/2019
~~~

**This is work in progress!** *See bottom of the page for details*

*strip_dilbert* is a simple image scrper written in Python for the well-known [dilbert.com](https://dilbert.com) comic website.

**What does it do?**

Well, the idea is to download the dilbert comic strip(s) for any day they've been published, starting from 16th April 1989 all the way till now.

The script will have a number of options, letting the user get the comics for the current week or month, for example.

## Here's what the main menu will have:

:+1: working feature | :-1: feature to be implemented

1. **Today's comic strip:** *Downloads the comic for today* :-1:
2. **This week's strips:** *Downloads the comics for the current week - up till the current day* :-1:
3. **Last week's strips:** *Downloads the comics for last week* :-1:
4. **This month's strips:** *Downloads the comics for the current month - up till the current day* :-1:
5. **Last month's strips:** *Downloads all the comics for the previous month* :-1:
6. **Custom date range:** *Let's the user set the download date range (16/Apr/1989 - NOW)* :+1:

So, hopefully there are going to be some opportutnies for you with this script. ;)

[![opportunity.png](https://assets.amuniversal.com/505f94006cbc01301d46001dd8b71c47)](https://dilbert.com/strip/2009-09-24)

## WORK PROGRESS:

- [x] DONE! :collision:
- [ ] TO-DO :shit:

- [x] Implement custom date range menu item (it's working but kinda slow)
- [ ] Implement all the main menu items
- [ ] Improve the performance of the `download_engine()` method
- [ ] Comment all the code
- [ ] Reorder ale the methods and implement `if __name__ == '__main__':`