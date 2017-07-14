import re
import os
import csv
import time
import requests
#import sendEmail
from time import sleep
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from PulsePointReport import PulsePoint
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

class IronSource:
    start_time_irs = time.time()
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

    # Get dates to add to url to get report
    a_year = str(the_time.year)
    a_month = str(the_time.month).zfill(2)
    a_day = str(the_time.day - 2).zfill(2)
    a_year2 = str(the_time.year)
    a_month2 = str(the_time.month).zfill(2)
    a_day2 = str(the_time.day - 2).zfill(2)

    location_of_file = "/Users/noah.p/Documents/Daily_Reports_July_12/IronSource-July_12/"
    #location_of_file = "/Users/noah.p/Desktop/TestFolder/"

    # Don't edit name of entires they are name with extra spaces and whitespace on purpose
    dict_T = {
        "Taboola-Mix-US-85_15-$5.5Floor": "IronSource_Direct_Desktop_US-5.5",
        "Taboola-Mix-US-$6.5-RON": "IronSource_Direct_Desktop_US-6.5",
        "Taboola-Large-US-$7.5": "IronSource_Direct_Desktop_US-7.5"
    }

    def __init__(self, end_date, date_post, location_of_file, dict_T):
        """
        Constructor
        :param end_date:
        :param date_post:
        :param location_of_file:
        :param dict_T:
        """
        self.end_date = end_date
        self.date_post = date_post
        self.location_of_file = location_of_file
        self.dict_T = dict_T

    def init_browser(self):
        """
        Initilizes the browser
        :return the browser:
        """
        browser = webdriver.Firefox()
        browser.wait = WebDriverWait(browser, 5)
        return browser

    def lookup(self,browser):
        """Login to the website """

        try:
            loginPage = "https://partners.streamrail.com/#/signin"
            browser.get(loginPage)
            # "https://partners.streamrail.com/#/report?dimension=trafficChannel&endDate=2017-07-08T23%3A59%3A59%2B00%3A00&sortAsc=false&sortBy=cost&startDate=2017-07-08T00%3A00%3A00%2B00%3A00&type=supply-partner-traffic-channel"
            sleep(3)
            loginInputFields = browser.find_elements_by_class_name("ember-text-field")
        except:
            raise Exception("ERROR-Iron:Failed to load page")
        try:
            # Wait longer if page is not fully loaded
            if (len(loginInputFields) is 0):
                time.sleep(5)
            username = loginInputFields[0]
            password = loginInputFields[1]

            username.send_keys("TaboolaEedo")
            password.send_keys("Taboola123!")
            # Find sign in button
            signInButton = browser.find_element_by_class_name("btn")

            # Refresh and try to find the button
            if not (signInButton.text == "LOG IN"):
                signInButton = browser.find_element_by_class_name("btn")
            # click the sign in button
            try:
                signInButton.click()
                print("Logged in successfully")
            except ElementNotVisibleException:
                signInButton = browser.wait.until(EC.element_to_be_clickable((By.ID, "loginButton")))
                signInButton.click()
        except TimeoutException:
            print("Login Box or Button not found on IronSource website")
            print("Login Failed")

    def getData(self, browser):
        """
        Gets the data from the site
        :param browser:
        :return:
        """

        # Get the report page and run the report
        reportsPage = "https://partners.streamrail.com/#/report?dimension=trafficChannel&endDate=" + IronSource.a_year + "-" + IronSource.a_month + "-" + IronSource.a_day + "T23%3A59%3A59%2B00%3A00&sortAsc=false&sortBy=cost&startDate=" + IronSource.a_year2 + "-" + IronSource.a_month2 + "-" + IronSource.a_day2 + "T00%3A00%3A00%2B00%3A00&type=supply-partner-traffic-channel"
        try:
            browser.get(reportsPage)
        except Exception:
            raise Exception("ERROR-Iron:Unable to load Iron source reports page")

        sleep(2)
        waitForIt = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'sr-table')))
        print("Page is ready!")
        try:
            # Here is a list of all the buttons on the page
            table_data = browser.find_element_by_class_name('sr-table')
            table_data = table_data.text
            browser.quit()

            table_data_list = table_data.splitlines()
            table_data2 = table_data_list[20:]
            row = table_data2[1:3]
            row1 = table_data2[6:8]
            row2 = table_data2[11:13]
        except Exception:
            raise Exception("ERROR-Iron: Unable to get data from table")

        try:
            paid_impressions_list = [row[0], row1[0], row2[0]]
            revenue_list = [row[1], row1[1], row2[1]]
            taboola_list = table_data_list[2:5]
            numberOfRows = len(taboola_list)
        except Exception:
            raise Exception("ERROR-Iron: rows did not load or are empty or can not be found")

        return taboola_list, paid_impressions_list, revenue_list


def main():
    irs = IronSource(IronSource.end_date, IronSource.date_post, IronSource.location_of_file, IronSource.dict_T)
    pp = PulsePoint(irs.end_date, irs.date_post, irs.location_of_file, irs.dict_T)

    browser = irs.init_browser()
    irs.lookup(browser)
    name_list_final, imp_list_final, rev_list_final = irs.getData(browser)
    # If the return lists are empty then there must be an error so try again
    if len(name_list_final) is 0 or len(imp_list_final) is 0 or len(rev_list_final) is 0:
        name_list_final, imp_list_final, rev_list_final = irs.getData(browser)
    pp.makeCSV(irs.location_of_file, irs.dict_T, name_list_final, imp_list_final, rev_list_final, irs.end_date,irs.date_post)
    #browser.quit()
    print("IronSource program took --- %s seconds ---" % (time.time() - IronSource.start_time_irs))
    print("Done!")

if __name__ == "__main__":
    main()
