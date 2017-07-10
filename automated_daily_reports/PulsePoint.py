import re
import os
import csv
import time
import requests
#import sendEmail
from time import sleep
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

class PulsePoint:
    # Monday is 0 and Sunday is 6
    DayOfTheWeek = datetime.today().weekday()
    # Get the current Date
    currentDate = time.strftime("%m/%d/%Y")
    date_1 = datetime.strptime(currentDate, "%m/%d/%Y")

    # Move the current date back two days
    end_date = date_1 - timedelta(days=2)
    end_date = end_date.strftime('%m/%d/%Y')

    date_post = datetime.now() - timedelta(days=2)
    date_post = date_post.strftime(("%B %d, %Y"))

    the_time = datetime.now()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    the_path = "/Users/noah.p/going_headless/chromedriver"
    #browser = webdriver.Chrome(executable_path=the_path, chrome_options=chrome_options)
    browser = webdriver.Firefox()
    #browser.set_window_size(1500,1250)
    url = "https://exchange.pulsepoint.com/AccountMgmt/Login.aspx?app=publisher&ReturnUrl=%2fPublisher%2fReports.aspx#/Reports"
    loginPage = browser.get(url)

    username = browser.find_element_by_name("UserName")
    password = browser.find_element_by_name("Password")

    # Type in username and password
    username.send_keys("")
    password.send_keys("")

    # Find sign in button
    signInButton = browser.find_element_by_id("LoginButton")
    # click the sign in button
    signInButton.click()

   # reportPage = browser.get("https://exchange.pulsepoint.com/Publisher/Reports.aspx#/Reports")

    sleep(3)

    # Put in the date for date from
    #date_from = browser.find_element_by_xpath("//*[@id='dateFrom']")
    date_from = browser.find_element_by_id("dateFrom")
    date_from.clear()
    date_from.send_keys(end_date)

    # Put in the date for date to
    #date_to = browser.find_element_by_xpath("//*[@id='dateTo']")
    date_to = browser.find_element_by_id("dateTo")
    date_to.clear()
    date_to.send_keys(end_date)

    cal_btns = []
    cal_2_days_inputs = []
    btn_num = 0

    allBtnsOnPage = browser.find_elements_by_class_name("btn")
    numberOfBtns = len(allBtnsOnPage)

    runReportButton = allBtnsOnPage[numberOfBtns-1]
    if runReportButton.text == "RUN REPORT":
        runReportButton.send_keys(Keys.ENTER)
    else:
        runReportButton = browser.find_elements_by_tag_name("button")
        for btn in runReportButton:
            if btn.text == "RUN REPORT":
                runReportButton.send_keys(Keys.ENTER)

    # Webscrape the data and export to .csv files
    sleep(6)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    str_text = soup.text
    str_text = str_text.splitlines()

    str_text = str_text[744:]
    str_text = str_text[142:]

    name_col = browser.find_elements_by_class_name("nameCol")
    rev_col = browser.find_elements_by_class_name("revenueCol")
    paid_imps_col = browser.find_elements_by_class_name("paidImpsCol")

    # Remove all empty strings "" from the list
    i = 0
    while i < len(name_col):
        if (name_col[i].text == ""  and rev_col[i].text == "" and paid_imps_col[i].text == ""):
            del name_col[i]
            del rev_col[i]
            del paid_imps_col[i]
        i +=1
    name_list = name_col[2:]
    rev_list = rev_col[2:]
    imp_list = paid_imps_col[2:]
    numberOfItems = len(name_list)
    dict_Name = {
        name_list[0]: "Pulse_Point_Direct_Desktop_BTU_Standard_5",
        name_list[1]: "Pulse_Point_Direct_Desktop_BTU_Standard_6",
        name_list[2]: "Pulse_Point_Direct_Desktop_BTU_Standard_7"
    }

    location_of_file = "/Users/noah.p/Desktop/TestFolder/"


    # Write to csv file
    q = 0
    while q < numberOfItems:
        name_of_file = name_list[q]
        imp = imp_list[q].text.replace(",","")
        rev = rev_list[q].text.replace("$","")

        with open(location_of_file + dict_Name[name_of_file] + "_" + date_post + ".csv", "w") as csv_file:
            fileWriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            fileWriter.writerow(["Date", "Impressions", "Revenue"])
            fileWriter.writerow([end_date, imp, rev])
        q += 1
    browser.quit()
    print("Done!")
