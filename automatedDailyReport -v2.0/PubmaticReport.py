import re
import os
import csv
import time
import logging
from time import sleep
from PulsePointReport import PulsePoint
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

class Pubmatic:
    """Gets all the dates and times that are needed for this class"""
    # Monday is 0 and Sunday is 6
    DayOfTheWeek = datetime.today().weekday()
    # Get the current Date
    currentDate = time.strftime("%m/%d/%Y")
    date_1 = datetime.strptime(currentDate, "%m/%d/%Y")

    # Move the current date back two days
    # In the mm/dd/yyyy format
    end_date = date_1 - timedelta(days=2)
    end_date = end_date.strftime('%m/%d/%Y')

    # This one is in "Month name day, full year ex.July 12,2017
    date_post = datetime.now() - timedelta(days=2)
    date_post = date_post.strftime(("%B %d, %Y"))


    the_time = datetime.now()
    two_days_ago = str(the_time.day - 2)
    location_of_file = "/Users/noah.p/Desktop/DailyReports/"

    logFile = "/Users/noah.p/PycharmProjects/autoReports/DailyReportsLog/AutoDailyManualReportslogs.log/"
    logName = "Pubmatic"


    dict_T = {
        "TaboolaWebLargePlayer$9": "Pubmatic_Direct_Desktop_LP_9",
        "TaboolaWebMediumPlayer$7": "Pubmatic_Direct_Desktop_MP_7",
        "TaboolaWebMediumPlayersecured$6": "Pubmatic_Direct_Desktop_Secured_6",
        "TaboolaWebSmallPlayer$5": "Pubmatic_Direct_Desktop_SP_5",
        "TaboolaMWebLMPlayer$6": "Pubmatic_Direct_MW_LP_6",
        "TaboolaMWebLargePlayer$7": "Pubmatic_Direct_MW_LP_7",
        "TaboolaMWebLargePlayer$8": "Pubmatic_Direct_MW_LP_8",
        "TaboolaMWebMediumPlayer$5": "Pubmatic_Direct_MW_MP_5",
        "TaboolaMWebSmallPlayer$3": "Pubmatic_Direct_MW_SP_3",
        "TaboolaMWebMediumPlayersecured$5": "Pubmatic_Direct_MW_Secured_5"
    }

    def __init__(self,two_days_ago, end_date, date_post, location_of_file, dict_T):
        """
        Constructor
        :param two_days_ago:
        :param end_date:
        :param date_post:
        :param location_of_file:
        :param dict_T:
        """
        self.two_days_ago = two_days_ago
        self.end_date = end_date
        self.date_post = date_post
        self.location_of_file = location_of_file
        self.dict_T = dict_T

    def start_browser(self):
        """
        Initilizes the browser
        :return the browser:
        """
        browser = webdriver.Firefox()
        browser.maximize_window()
        browser.wait = WebDriverWait(browser, 5)
        return browser

    def lookup(self,browser,logger):
        """Login to website and navigate to report page
        :param browser:
        :return:
        """
        try:
            url = "https://apps.pubmatic.com/publisher/"
            loginPage = browser.get(url)
            logger.info("Pubmatic site loaded")
        except TimeoutException:
            logger.error("Error- Pubmatic: Failed to load page")
            raise Exception("Error- Pubmatic: Failed to load page")
        try:
            loginForm = browser.wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME,"input")))
            loginForm = browser.find_elements_by_tag_name("input")

            username = loginForm[0]
            password = loginForm[1]

            signInButton = browser.wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))

            # Type in username and password
            username.send_keys("or.ben@taboola.com")
            password.send_keys("ELwGdKxnyb64")
            # Find sign in button and try to click it
            try:
                signInButton.click()
                print("Logged in successfully")
                logger.info("Logged in successfully")
            except ElementNotVisibleException:
                signInButton = browser.wait.until(EC.visibility_of_element_located((By.ID, "loginButton")))
                signInButton.click()
        except TimeoutException:
            logger.error(TimeoutException)
            logger.error("Login Box or Button not found on Pubmatic website")
            logger.error("Login Failed")
            print("Login Box or Button not found on Pubmatic website")
            print("Login Failed")


    def fillInDateAndRunReport(self,browser,two_days_ago):
        """
        Fill in the date for the website and click it
        :param: browser, end_date
        :return:
        """
        sleep(3)
        analyticsPage = "https://analytics.pubmatic.com/#/?originApp=publisher&resourceType=publisher&signoutUrl=https:%2F%2Fapps.pubmatic.com%2F%2Fpublisher%2F%3FviewName%3Dsignout&apiAuthKey=PubToken&apiAuthValue=68bf3dfba4bc478b9500d644f04499e3&originUrl=https:%2F%2Fapps.pubmatic.com%2F%2Fdashboard%2Fapp%2F%23%2Fpublisher&homeUrl=https:%2F%2Fapps.pubmatic.com%2F%2Fdashboard%2Fapp%2F%23%2Fpublisher&resourceId=156307&opString=5G6QHS07D3Y4DFMJMBR6MYF9JN1K1WKD&loginType=0"
        browser.get(analyticsPage)
        sleep(3)
        reportsPage = "https://analytics.pubmatic.com/#/slice?f=eyJkIjpbInNpdGVJZCIsImRhdGUiXSwibSI6WyJwYWlkSW1wcmVzc2lvbnMiLCJlY3BtIiwicmV2ZW51ZSIsInRvdGFsSW1wcmVzc2lvbnMiXSwiZiI6W1sidCIsInJldmVudWUiLCJ0IiwiMjUiLCIiLCIiLFtdXSxbInQiLCJkYXRlIiwidCIsIjEwIiwiIiwiIixbXV1dLCJ0IjpbMl0sImN0IjpbXSwiYyI6eyJ0IjoiYmFyY2hhcnQiLCJkIjoiIiwiYSI6ImRhdGUiLCJtIjoicmV2ZW51ZSJ9LCJhIjoiZGF0ZSJ9&standardReportId=260"
        browser.get(reportsPage)

        # If it didnt load try again
        if not browser.current_url == reportsPage:
            sleep(3)
            browser.get(reportsPage)
        sleep(3)
        try:
            # Get the date ranges dropdown menu
            date_cal_btn = browser.wait.until(EC.visibility_of_element_located((By.ID,"date-picker-dropdown")))
            # Click the button
            date_cal_btn.click()
        except:
            #Try again
            sleep(5)
            # Get the date ranges dropdown menu
            date_cal_btn = browser.wait.until(EC.visibility_of_element_located((By.ID, "date-picker-dropdown")))
            # Click the button
            date_cal_btn.click()

        # Get all a tags "<a"
        aTags = browser.find_elements_by_tag_name("a")
        # Find custom range button
        for button in aTags:
            if button.text == "Custom Range":
                button.click()
                break

        # Get all the calender dates
        days = browser.find_elements_by_class_name("days-cell")
        # Find and click the date of 2 days ago
        x = 0
        for date in days:
            if date.text == two_days_ago:
                date.click()
                x += 1
                # Found both dates for both calenders so end the loop early
                if x > 1:
                    break

        sleep(2)
        # Find and click the confirm button to finish putting in the dates
        confirmBtn = browser.wait.until(EC.element_to_be_clickable((By.ID, "dialog-submit")))
        confirmBtn.click()
        sleep(1)
        # Scroll down the page to get the table into view
        browser.execute_script("window.scrollTo(0, 800)")

        # Take and save screen shot of table
        screenShot = browser.save_screenshot(filename="/Users/noah.p/PycharmProjects/autoReports/DailyReportsLog/PubmaticData.png")



    def getData(self,browser,logger):
        """
        Webscrape the data and export to .csv files
        :return name, impressions and revenue lists:
        """
        # Tries to find by class name and if fails tries another method by id and parsing a string to get the data.
        try:
            tableData = browser.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "table")))
        except:
            # Try another way to find and get the table data
            try:
                sleep(5)
                tableData = browser.find_elements_by_tag_name("pub-table")
            except Exception:
                logger.error("Pubmatic: Failed to find table data")
                raise Exception("Error- Pubmatic: Failed to find table data")
        # Create the final 3 lists
        name_list = []
        imp_list = []
        rev_list = []

        # Parse the string and get data in the correct 3 above lists
        tableDataText = tableData.text
        tableDataList = tableDataText.splitlines()

        reportName_list = tableDataList[6::5]
        paid_imps_list = tableDataList[7::5]
        revenue_list = tableDataList[9::5]

        theLength = len(reportName_list)

        # Loop through lists to organize the data
        i = 0
        while i < theLength:
            current_name = reportName_list[i].replace("/", "")
            current_imp = paid_imps_list[i]
            current_rev = revenue_list[i]
            # add to final lists
            name_list.append(current_name)
            imp_list.append(current_imp)
            rev_list.append(current_rev)
            i += 1

        return name_list, imp_list, rev_list


def main():
    """
    Main method
    :return:
    """
    pb = Pubmatic(Pubmatic.two_days_ago,Pubmatic.end_date, Pubmatic.date_post, Pubmatic.location_of_file,Pubmatic.dict_T)
    pp = PulsePoint(Pubmatic.end_date, Pubmatic.date_post, Pubmatic.location_of_file, Pubmatic.dict_T)
    browser = pb.start_browser()
    logger = pp.logToFile(browser,Pubmatic.logFile, Pubmatic.logName)
    pb.lookup(browser,logger)
    pb.fillInDateAndRunReport(browser, pb.two_days_ago)
    name_list, imp_list, rev_list = pb.getData(browser, logger)
    if len(name_list) is 0 or len(imp_list) is 0 or len(rev_list) is 0:
        name_list, imp_list, rev_list = pb.getData(browser,logger)

    pp.makeCSV(pb.location_of_file, pb.dict_T, name_list, imp_list, rev_list, pb.end_date, pb.date_post)
    browser.quit()

if __name__ == "__main__":
    main()
