import re
import time
import csv
#import sendEmail
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from bs4 import BeautifulSoup

class IronSource:
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
    browser = webdriver.Firefox()
    #browser = webdriver.PhantomJS()
    #browser.set_window_size(1124, 1000)

    loginPage = browser.get('https://partners.streamrail.com/#/signin')
    #"https://partners.streamrail.com/#/report?dimension=trafficChannel&endDate=2017-07-08T23%3A59%3A59%2B00%3A00&sortAsc=false&sortBy=cost&startDate=2017-07-08T00%3A00%3A00%2B00%3A00&type=supply-partner-traffic-channel"
    time.sleep(3)
    loginInputFields = browser.find_elements_by_class_name("ember-text-field")

    # Wait longer if page is not fully loaded
    if(len(loginInputFields) is 0):
        time.sleep(5)
    username = loginInputFields[0]
    password = loginInputFields[1]

    username.send_keys("")
    password.send_keys("")
    # Find sign in button
    signInButton = browser.find_element_by_class_name("btn")

    # Refresh and try to find the button
    if not(signInButton.text == "LOG IN"):
        signInButton = browser.find_element_by_class_name("btn")
    # click the sign in button
    signInButton.click()
    # Get dates to add to url to get report
    a_year = str(the_time.year)
    a_month = str(the_time.month).zfill(2)
    a_day = str(the_time.day - 2).zfill(2)
    a_year2 = str(the_time.year)
    a_month2 = str(the_time.month).zfill(2)
    a_day2 = str(the_time.day - 2).zfill(2)

    delay = 5

    reportsPage = browser.get("https://partners.streamrail.com/#/report?dimension=trafficChannel&endDate=" + a_year +"-"+ a_month +"-" + a_day +"T23%3A59%3A59%2B00%3A00&sortAsc=false&sortBy=cost&startDate=" + a_year2 +"-"+ a_month2 + "-" + a_day2 + "T00%3A00%3A00%2B00%3A00&type=supply-partner-traffic-channel")

    waitForIt = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'sr-table')))
    print("Page is ready!")

    # Here is a list of all the buttons on the page
    table_data = browser.find_element_by_class_name('sr-table')
    table_data = table_data.text
    browser.quit()
    table_data_list = table_data.splitlines()
    table_data2 = table_data_list[20:]
    row = table_data2[1:3]
    row1 = table_data2[6:8]
    row2 = table_data2[11:13]

    paid_impressions_list = [row[0],row1[0],row2[0]]
    revenue_list = [row[1],row1[1],row2[1]]
    taboola_list = table_data_list[2:5]
    numberOfRows = len(taboola_list)

    dict_Name = {
        taboola_list[0]: "IronSource_Direct_Desktop_US-5.5",
        taboola_list[1]: "IronSource_Direct_Desktop_US-6.5",
        taboola_list[2] : "IronSource_Direct_Desktop_US-7.5"
    }

    location_of_file = "/Users/noah.p/Desktop/TestFolder/"
    indexer = 0
    #TODO: Make this a method parameters(locationOfFile, current_taboola,domain,impression and revenue list)
    # Write to csv file
    q = 0
    while(q < numberOfRows):
        with open(location_of_file + dict_Name[taboola_list[q]] + "_" + date_post + ".csv", "w") as csv_file:
            fileWriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            fileWriter.writerow(["Date", "Impressions", "Revenue"])
            # Write to file
            fileWriter.writerow([end_date, paid_impressions_list[q].replace(",",""),revenue_list[q].replace("$","")])
        q +=1

    print("Done!")
