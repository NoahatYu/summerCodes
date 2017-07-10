import re
import csv
#import sendEmail
import time
from time import sleep
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
class Thrive:
    # TODO: Make sure I check what day it is,because if it is a monday the weekend days must be done as well.
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
    #browser = webdriver.Firefox()
    browser = webdriver.PhantomJS()
    browser.set_window_size(1124, 1000)

    loginPage = browser.get('https://video.springserve.com/')

    username = browser.find_element_by_id("user_email")
    password = browser.find_element_by_id("user_password")

    usernameThrive = ""
    passwordThrive = ""
    # Type in username and password
    username.send_keys(usernameThrive)
    password.send_keys(passwordThrive)

    # Find sign in button
    signInButton = browser.find_element_by_name("commit")
    # click the sign in button
    signInButton.click()

    reportPage = browser.get("https://video.springserve.com/reports")

    a_year1 = str(the_time.year % 100)
    a_month1 = str(the_time.month)
    a_day1 = str(the_time.day - 2)
    a_year2 = str(the_time.year % 100)
    a_month2 = str(the_time.month)
    a_day2 = str(the_time.day - 2)

    # Get the report page and run the report
    date_report_page = "https://video.springserve.com/reports?date_range=Custom&custom_date_range=" + a_month1 +"%2F" + a_day1 + "%2F" + a_year1 + "+00%3A00+-+" + a_month2 + "%2F" + a_day2 + "%2F" + a_year2 + "+23%3A00&interval=Day&timezone=America%2FNew_York&dimensions%5B%5D=supply_tag_id"
    browser.get(date_report_page)
    runReportButton = browser.find_element_by_name("commit")
    runReportButton.click()

    # Webscrape the data and export to .csv files
    sleep(3)
    table_row_data = browser.find_elements_by_tag_name("tr")

    # Sleep more if table is not fully loaded
    if(len(table_row_data) < 15):
        sleep(3)
        table_row_data = browser.find_elements_by_tag_name("tr")

    # Get the data I want
    table_row_data = table_row_data[12:]
    # Remove the totals row
    del table_row_data[-1]

    rev_list = []
    imp_list = []
    name_list = []

    dict_Name = {
       "Taboola_MW_JS__Tier_1_ENG__2": "Thrive_Mobile_2", "Taboola_Desktop__320x180__SP_ENG__3": "Thrive_Direct_Desktop_5"
    }
    sleep(3)
    for table_row in table_row_data:
        table_row = table_row.text
        current_row = table_row.split(" ")
        lengthOfTRow = len(current_row)

        name = current_row[3:13]
        name = name[0] + "_" + name[1] + "_" + name[2] + "_" + name[3] + "_" + name[4] + "_" + name[5] + name[6] + "_" + name[7] + "_" + name[8] + "_" + name[9]
        name = name.replace('|', "")
        imp = current_row[16].replace(",", "")
        rev = current_row[18].replace('$', "")
        rev_list.append(rev)
        imp_list.append(imp)
        name_list.append(name)

        location_of_file = "/Users/noah.p/Desktop/TestFolder/"
        # Write to csv file
        with open(location_of_file + dict_Name[name] + "_" + date_post + ".csv", "w") as csv_file:
            fileWriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            fileWriter.writerow(["Date", "Impressions", "Revenue"])
            fileWriter.writerow([end_date, imp, rev])
    browser.quit()
    print("Done!")
