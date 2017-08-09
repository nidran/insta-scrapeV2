# getList libraries
from __future__ import division
import codecs   # encoding
from collections import defaultdict
import json
import os
import re  
import sys
import time
try:
    from urlparse import urljoin
    from urllib import urlretrieve
except ImportError:
    from urllib.parse import urljoin
    from urllib.request import urlretrieve

import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# HOST
HOST = 'http://www.instagram.com'

# FOLLOWERS/FOLLOWING RELATED
CSS_EXPLORE = "a[href='/explore/']"
CSS_LOGIN = "a[href='/accounts/login/']"
CSS_FOLLOWERS = "a[href='/{}/followers/']"
CSS_FOLLOWING = "a[href='/{}/following/']"
FOLLOWER_PATH = "//div[contains(text(), 'Followers')]"
FOLLOWING_PATH = "//div[contains(text(), 'Following')]"

# JAVASCRIPT COMMANDS
SCROLL_UP = "window.scrollTo(0, 0);"
SCROLL_DOWN = "window.scrollTo(0, document.body.scrollHeight);"



class InstagramCrawler(object):
    """
        Crawler class
    """
    def __init__(self, headless=True):
        if headless:
            print("headless mode on , incase you want to use PhantomJS instead of Firefox")
            self._driver = webdriver.PhantomJS()
        else:
            self._driver = webdriver.Firefox()
        self._driver.implicitly_wait(10)
        self.data = defaultdict(list)

    def login(self, authentication=None):
        """
            authentication: path to authentication json file or type in command line
        """
        self._driver.get(urljoin(HOST, "accounts/login/"))

        if authentication:
            print("Username and password loaded from {}".format(authentication))
            with open(authentication, 'r') as fin:
                auth_dict = json.loads(fin.read())
            # Input username
            username_input = WebDriverWait(self._driver, 5).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            username_input.send_keys(auth_dict['username'])
            # Input password
            password_input = WebDriverWait(self._driver, 5).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            password_input.send_keys(auth_dict['password'])
            # Submit
            password_input.submit()
        else:
            print("Type your username and password by hand to login!")
            print("You have a minute to do so!")

        print("")
        WebDriverWait(self._driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CSS_EXPLORE))
        )

    def quit(self):
        self._driver.quit()

    def crawl(self, dir_prefix, query, crawl_type, number, caption, authentication):
        print("dir_prefix: {}, query: {}, crawl_type: {}, number: {}, caption: {}, authentication: {}"
              .format(dir_prefix, query, crawl_type, number, caption, authentication))
      

        if crawl_type in ["followers", "following"]:
            # Need to login first before crawling followers/following
            print("You will need to login to crawl {}".format(crawl_type))
            self.login(authentication)
            self.browse_target_page(query)
            self.scrape_followers_or_following(crawl_type, query, number)
        else:
            print("Unknown crawl type: {}".format(crawl_type))
            self.quit()
            return

        # Save to directory
        print("Saving...")
        self.download_and_save(dir_prefix, query, crawl_type)

        # Quit driver
        print("Quitting driver...")
        self.quit()

    def browse_target_page(self, query):        
        relative_url = query
        target_url = urljoin(HOST, relative_url)
        self._driver.get(target_url)    
    
    def scrape_followers_or_following(self, crawl_type, query, number):
        print("Scraping {}...".format(crawl_type))
        if crawl_type == "followers":
            FOLLOW_ELE = CSS_FOLLOWERS
            FOLLOW_PATH = FOLLOWER_PATH
        elif crawl_type == "following":
            FOLLOW_ELE = CSS_FOLLOWING
            FOLLOW_PATH = FOLLOWING_PATH

        # Locate follow list
        follow_ele = WebDriverWait(self._driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, FOLLOW_ELE.format(query)))
        )

        # when no number defined, check the total items
        if number is 0:
            number = int(filter(str.isdigit, str(follow_ele.text)))
            print("getting all " + str(number) + " items")

        # open desired list
        follow_ele.click()

        title_ele = WebDriverWait(self._driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, FOLLOW_PATH))
        )
        List = title_ele.find_element_by_xpath(
            '..').find_element_by_tag_name('ul')
        List.click()

        # Loop through list till target number is reached
        num_of_shown_follow = len(List.find_elements_by_xpath('*'))
        while len(List.find_elements_by_xpath('*')) < number:
            element = List.find_elements_by_xpath('*')[-1]
            # Work around for now => should use selenium's Expected Conditions!
            try:
                element.send_keys(Keys.PAGE_DOWN)
            except Exception as e:
                time.sleep(0.1)

        follow_items = []
        for ele in List.find_elements_by_xpath('*')[:number]:
            follow_items.append(ele.text.split('\n')[0])

        self.data[crawl_type] = follow_items

    def download_and_save(self, dir_prefix, query, crawl_type):
        # Check if is hashtag
        dir_name = query
        dir_path = os.path.join(dir_prefix, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        print("Saving to directory: {}".format(dir_path))

    
        # Save followers/following
        filename = crawl_type + '.txt'
        filepath = os.path.join(dir_path, filename)
        if len(self.data[crawl_type]):
            with codecs.open(filepath, 'w', encoding='utf-8') as fout:
                for fol in self.data[crawl_type]:
                    fout.write(fol + '\n')


def main():
    #   Parsing Arguments  #
    parser = argparse.ArgumentParser(description='Instagram Crawler')
    parser.add_argument('-d', '--dir_prefix', type=str,
                        default='./data/', help='directory to save results')
    parser.add_argument('-q', '--query', type=str, default='instagram',
                        help="target to scrape")
    parser.add_argument('-t', '--crawl_type', type=str,
                        default='photos', help="Options: 'followers' | 'following'")
    parser.add_argument('-n', '--number', type=int, default=0,
                        help='Number of posts to download: integer')
    parser.add_argument('-l', '--headless', action='store_true',
                        help='If set, will use PhantomJS driver to run script as headless')
    parser.add_argument('-a', '--authentication', type=str, default=None,
                        help='path to authentication json file')
    args = parser.parse_args()
    #  End Argparse #

    crawler = InstagramCrawler(headless=args.headless)
    crawler.crawl(dir_prefix=args.dir_prefix,
                  query=args.query,
                  crawl_type=args.crawl_type,
                  number=args.number,
                  caption=args.caption,
                  authentication=args.authentication)


if __name__ == "__main__":
    main()
