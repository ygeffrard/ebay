from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Screenshot import Screenshot_Clipping
from time import sleep  
from getpass import getpass
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium_cookies import CookieHandler
from pathlib import Path
from datetime import *
from dateutil.parser import *
import requests
import re 
import pickle
import os


path = Path(__file__).parent


url="https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&ru=https%3A%2F%2Fwww.ebay.com%2Fn%2F"


# chrome_options = Options()
# chrome_options.add_argument("--user-data-dir=chrome-data")
chrome = webdriver.Chrome()
cookie_handler = CookieHandler(chrome,url, overwrite=True, filename="ebaycooks", wait_time=5)
loaded_cookies = cookie_handler.load_cookies()

#chrome.get(url)
saved_cookies = cookie_handler.save_cookies()
action = ActionChains(chrome)
year = input("Enter Tax Year: ")
receifly_url = ""

def login():
    
    password = input("Enter your password: ")

    #--------Username----------
    def username():
        username = input("Enter your username: ")
        username_textbox = chrome.find_element_by_id("userid")
        username_textbox.send_keys(username)
        login_button = chrome.find_element_by_name("signin-continue-btn")
        login_button.submit()
        return;

    username()

    #--------Password----------
    def password():
        password_textbox = chrome.find_element_by_id("pass")
        password_textbox.send_keys(password)
        login_button = chrome.find_element_by_name("sgnBt")
        login_button.submit()
    
    password()

    def set_receipt_app_url():
        receifly_url = input("Enter your receipt application url: ")

    set_receipt_app_url()
    return;


login()

#--------Purchase page----------

#Open My Ebay dropdown
myebay_link_dropdown = chrome.find_element_by_xpath("//a[@href='https://www.ebay.com/mys/home?source=GBH']")
action.move_to_element(myebay_link_dropdown).perform()

#Click Purchase History
purchase_history_link = chrome.find_element_by_xpath("//a[@href='https://www.ebay.com/myb/PurchaseHistory']")
purchase_history_link.click()


#Open year dropdown
year_link_dropdown = chrome.find_element_by_css_selector("button.ssixtyDays")
year_link_dropdown.click()

#Select orders 2020
selected_year = chrome.find_element_by_partial_link_text(year)
selected_year.click()

sleep(1)
#-------find list of paginations
pagination = chrome.find_elements_by_css_selector("a.pg")

page_counter=1
item_counter = 1
order_ids = []
for page in pagination:
    #click on the page to new tab
    if(page_counter > 1):
        page.click()
    sleep(3)
    #find list of items to view order details
    items = chrome.find_elements_by_xpath("//a[@title='View order details']")

    for item in items:
        chrome.execute_script("window.open('"+item.get_attribute('href')+"','new window')")
        #sleep(1)
        chrome.switch_to.window(chrome.window_handles[1])
        #WebDriverWait(chrome,5).until(EC.visibility_of(By.XPath("//*[@id='orderDetails']")
        sleep(5)
        #Grab Order Number
        current_order_id = chrome.find_element_by_xpath("//span[@data-test-id='orderId']/*[@class='ng-binding']").text        
 
        #If not store it
        if current_order_id not in order_ids:
            order_ids.append(current_order_id)
            #Grab title
            item_elements = chrome.find_elements_by_css_selector("[data-ng-repeat='uniqueItemId in package.uniqueItemIds'] h4 a") #grab all elements
            item_titles = ''
            if (len(item_elements) > 1):
                for item_element in item_elements:
                    item_titles += ' '.join(item_element.text.split()[:4])
                    if item_element != item_elements[-1]:
                        item_titles += ", "
            else:
                item_titles = ' '.join(item_elements[0].text.split()[:4])
            print(item_titles)
          
            #Grab Date
            item_date = chrome.find_element_by_id('orderPaymentDate').text
            #Grab Dollar Amount
            item_amount = chrome.find_element_by_id('orderTotalCost').text.strip().lstrip("$")

            sleep(1)
            ob=Screenshot_Clipping.Screenshot()
            img_url=ob.full_Screenshot(chrome, str(path) + "/" , image_name='Ebay-'+str(item_counter)+'.png')

            sleep(1)
            #Open Receipt Window
            chrome.execute_script("window.open('"+receifly_url+"','_blank')")
            chrome.switch_to.window(chrome.window_handles[2])
            #Push Photo to Receifly
            chrome.find_element_by_id("receiptImage").send_keys(img_url)
            #Push to Company "Home"
            chrome.find_element_by_id("accountingCompany").send_keys("Home")
            #Push Merchant "Ebay"
            chrome.find_element_by_id("merchantName").send_keys("Ebay")
            #Push Date
            item_date_object = parse(item_date).strftime('%Y-%m-%d')
            chrome.execute_script("arguments[0].value = '"+item_date_object+"';", chrome.find_element_by_id("purchaseDate")) 
            #Push Category "Repair and Maintenance"
            chrome.find_element_by_id("categoryName").send_keys("Repair and Maintenance")
            #Push Dollar Amount
            chrome.execute_script("arguments[0].value = '"+item_amount+"';", chrome.find_element_by_id("purchaseAmount")) 
            #Submit Receipt
            chrome.find_element_by_name("submitReceipt").click()
            sleep(2)
            chrome.close()
            chrome.switch_to.window(chrome.window_handles[1])

        item_counter += 1
        chrome.close()
        chrome.switch_to.window(chrome.window_handles[0])
    page_counter += 1
        
print "All Done"
#Save cookies
saved_cookies = cookie_handler.save_cookies()

