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

class Optimatic:

    #TODO: Make sure I check what day it is,because if it is a monday the weekend days must be done as well.
    #Also the calender is weird so got to go back a month

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

    loginPage = browser.get('https://publishers.optimatic.com/Portal2/default.aspx')

    username = browser.find_element_by_id("txtUserName")
    password = browser.find_element_by_id("txtPassword")


    username.send_keys("")
    password.send_keys("")
    # Find sign in button
    signInButton = browser.find_element_by_tag_name("button")
    #click the sign in button
    signInButton.click()

    reportsPage = browser.get("https://publishers.optimatic.com/Portal2/reports/")
    delay = 3
    # Here is a list of all the buttons on the page
    AllButtonsOnHeader = browser.find_elements_by_class_name('menuLabel')
    numOfButtons = AllButtonsOnHeader.__len__()
    i = 0
    for button in AllButtonsOnHeader:
        if(button.text == "REPORTING"):
            break
        else:
            i += 1
    reportingButton = AllButtonsOnHeader[i]

    #click the reporting button
    reportingButton.click()

    waitForIt = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'headerTitle')))
    print("Page is ready!")

    select_report_type_btn = browser.find_element_by_class_name('headerTitle')
    select_report_type_btn.click()

    all_list_containers = browser.find_elements_by_class_name('label')

    domain_btn = all_list_containers[2].click()

    all_list_containers = browser.find_elements_by_class_name('label')

    containers_list_dict = {

         "HK": "Taboola APAC HK",
        "ID": "Taboola APAC ID",
        "JP": "Taboola APAC JP",
        "MY": "Taboola APAC MY",
        "MY3.5": "Taboola APAC MY $3 floor",
       "PH": "Taboola APAC PH",
       "SG": "Taboola APAC SG",
        "SG3.5": "Taboola APAC SG $3 floor",
        "TH": "Taboola APAC TH"

    }

    calendar_chart = browser.find_element_by_class_name('calendarLabel')
    calendar_chart.click()

    calender_date = browser.find_elements_by_class_name('ui-state-default')
    numberOfDaysInMonth = len(calender_date) / 2
    numberOfDaysInMonth = int(numberOfDaysInMonth)

    # 2 calenders and 30 days c1: 0:1 - 29:30 and c2: 30:1 - 60:30
    # if 31 days c1: 0:1 - 30:31 and c2: 31:1 - 62:31
    calender_dates = browser.find_elements_by_xpath('//a[@href="'+'#'+'"]')
    two_days_past = the_time.day - 2
    counter = 1

    first_half_cal = calender_date[:len(calender_date)//2]
    second_half_cal = calender_date[len(calender_date)//2:]

    # Check if current date is the 1st then got to go back a month, one day
    yesterday = the_time.day - 1
    if(yesterday == 1):
        one_month_past = browser.find_elements_by_class_name('ui-datepicker-prev')
        # Right calender
        one_month_past[0].click()
        # Left calender
        one_month_past[1].click()


    first_cal_date = first_half_cal[two_days_past - 1]
    second_cal_date = second_half_cal[two_days_past - 1]

    first_cal_date.click()
    second_cal_date.click()

    # Get the 'ok' button and click it
    ok_btn = browser.find_elements_by_class_name('button')
    ok_btn[len(ok_btn) - 1].click()

    # Split the list to get the taboolas I would like
    select_report_type_DropDownList = all_list_containers[5:14]
    numberOfTaboolas = len(select_report_type_DropDownList)
    time.sleep(3)
    q = 0
    while(q < numberOfTaboolas):
        # After the first taboola is done the buttons need to be reloaded
        if(q > 0):
            time.sleep(2)
            change_taboola = browser.find_elements_by_class_name("headerListTitles")
            change_taboola[1].click()
            all_list_containers = browser.find_elements_by_class_name('label')
            select_report_type_DropDownList = all_list_containers[5:14]

        current_Taboola = select_report_type_DropDownList[q].text
        select_report_type_DropDownList[q].click()
        view_report_btn = browser.find_element_by_class_name("labelButton")
        view_report_btn.click()

        # Webscrape the data and export to .csv files
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, "html.parser")
        str_text = soup.text
        try:
            found = re.search("var array = (.+?)}];", str_text).group(1)
        except AttributeError:
            found = ''

        data_list = found.split(",")

        # Ads delivered is paid impressions
        paid_impressions_list = data_list[::4]
        paid_impressions_list = paid_impressions_list[1::2]
        domain_list = data_list[1::8]
        revenue_list = data_list[6::8]
        numberOfElements = len(domain_list)

        # Remove clutter and getting a clean website string
        x = 0
        while(x < numberOfElements):
            domain_list[x] = re.search("'(.+?)'", domain_list[x]).group(1)
            paid_impressions_list[x] = paid_impressions_list[x].split(":").pop().replace(" ", "")
            revenue_list[x] = revenue_list[x].split(":").pop().replace(" ", "")
            x += 1
        # get every 0th, 3rd, and 5th in the array
        location_of_file = "/Users/noah.p/Desktop/TestFolder/"
        indexer = 0
        #TODO: Make this a method parameters(locationOfFile, current_taboola,domain,impression and revenue list)
        # Write to csv file
        with open(location_of_file + current_Taboola + "_" + date_post + ".csv", "w") as csv_file:
            fileWriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            fileWriter.writerow(["Date", "Site", "Impressions", "Revenue"])
            # Write to file
            while(indexer < numberOfElements - 1):
                fileWriter.writerow([end_date, domain_list[indexer], paid_impressions_list[indexer], revenue_list[indexer]])
                indexer += 1
        q += 1
    browser.quit()
    print("Done!")
