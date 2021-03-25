from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from getpass import getpass
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from pycookiecheat import chrome_cookies
from pathlib import Path
import requests
import re 
import pickle
import os
import json

path = Path(__file__).parent

def save_cookies(driver, location):

    pickle.dump(driver.get_cookies(), open(location, "wb"))


def load_cookies(driver, location, url=None):

    cookies = pickle.load(open(location, "rb"))
    driver.delete_all_cookies()
    # have to be on a page before you can add any cookies, any page - does not matter which
    driver.get("https://ebay.com" if url is None else url)
    for cookie in cookies:
        if isinstance(cookie.get('expiry'), float):#Checks if the instance expiry a float 
            cookie['expiry'] = int(cookie['expiry'])# it converts expiry cookie to a int 
        driver.add_cookie(cookie)


def delete_cookies(driver, domains=None):

    if domains is not None:
        cookies = driver.get_cookies()
        original_len = len(cookies)
        for cookie in cookies:
            if str(cookie["domain"]) in domains:
                cookies.remove(cookie)
        if len(cookies) < original_len:  # if cookies changed, we will update them
            # deleting everything and adding the modified cookie object
            driver.delete_all_cookies()
            for cookie in cookies:
                driver.add_cookie(cookie)
    else:
        driver.delete_all_cookies()





url="https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&ru=https%3A%2F%2Fwww.ebay.com%2Fn%2F"

#cookies = chrome_cookies(url, cookies_location)
#r = requests.get(url, cookies=cookies)


username = input("Enter your username: ")
password = input("Enter your password: ")
year = input("Enter Tax Year: ")

breakpoint()

chrome = webdriver.Chrome()
chrome.get(url)
action = ActionChains(chrome)

#Load Cookies
""" cookies = pickle.load(open("cookies.pkl", "rb"))
if cookies
    for cookie in cookies:
        chrome.add_cookie(cookie) """

try:
    cookies = pickle.load(open("cookies.pkl", "rb"))
except (OSError, IOError) as e:
    foo = 3
    pickle.dump( chrome.get_cookies() , open("cookies.pkl","wb"))

""" cookies_filename = "cookies.txt"
file_exists = os.path.isfile(path / cookies_filename) 
if not file_exists:
    f = open(cookies_location, "w") """

breakpoint()

#--------Login----------

username_textbox = chrome.find_element_by_id("userid")
username_textbox.send_keys(username)

login_button = chrome.find_element_by_name("signin-continue-btn")
login_button.submit()

breakpoint()
#chrome.implicitly_wait(10)

password_textbox = chrome.find_element_by_id("pass")
password_textbox.send_keys(password)

login_button = chrome.find_element_by_name("sgnBt")
login_button.submit()

#save_cookies(chrome, cookies_location)

#chrome.implicitly_wait(10)
breakpoint()

#--------Purchase page----------

#Open My Ebay dropdown
myebay_link_dropdown = chrome.find_element_by_xpath("//a[@href='https://www.ebay.com/mys/home?source=GBH']")
action.move_to_element(myebay_link_dropdown).perform()

#Click Purchase History
purchase_history_link = chrome.find_element_by_xpath("//a[@href='https://www.ebay.com/myb/PurchaseHistory']")
purchase_history_link.click()

chrome.implicitly_wait(10)

#Open year dropdown
year_link_dropdown = chrome.find_element_by_css_selector("button.ssixtyDays")
year_link_dropdown.click()

#Select orders 2020
selected_year = chrome.find_element_by_partial_link_text(year)
selected_year.click()


#Get current cookies to save
""" current_cookies = chrome.get_cookies()
if os.stat(current_cookies).st_size > 0:
    load_cookies(chrome, cookies_location)
chrome.get(url) """

items = chrome.find_elements_by_xpath("//a[@title='View order details']")
breakpoint()

""" pagination = chrome.find_elements_by_class_name(".pagination__item")
print(len(pagination))
breakpoint()

paginations = chrome.find_elements_by_class_name("pagination__item")
print(len(paginations)) """

#find list of paginations
pagination = chrome.find_elements_by_css_selector("a.pg")
print('----Pagination length is')
print(len(pagination))
breakpoint()

for page in pagination:
    #click on the page to new tab
    
    page.click()
    #find list of items to view order details
    items = chrome.find_elements_by_xpath("//a[@title='View order details']")
    print('----Item length is')
    print(len(items))
    breakpoint()
    for item in items:
        # Open item in a new window
        print("-------item-> "+str(item))
        chrome.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        #item.click()
        #item.send_keys(Keys.COMMAND + 't') 
        
        #Switch to new window
        #chrome.switch_to.window(chrome.window_handles[1])
        print("Current Page Title is : %s" %chrome.title)
        # save it as pdf to local file
        #Close window
        chrome.close()
        chrome.switch_to.window(chrome.window_handles[0])
        print("Current Page Title is : %s" %chrome.title)
        breakpoint()
        #chrome.execute_script("window.open('');") """
    


#Save cookies
pickle.dump( chrome.get_cookies() , open("cookies.pkl","wb"))
