import re
import os
import csv
import time
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

class Thrive:
    start_time_tr = time.time()
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


    a_year1 = str(the_time.year % 100)
    a_month1 = str(the_time.month)
    a_day1 = str(the_time.day - 2)
    a_year2 = str(the_time.year % 100)
    a_month2 = str(the_time.month)
    a_day2 = str(the_time.day - 2)


    dict_T = {
        "TaboolaMWJSTier1ENG2": "Thrive_Mobile_2",
        "TaboolaDesktop320x180SPENG3": "Thrive_Direct_Desktop_5"
    }

    location_of_file = "/Users/noah.p/Desktop/DailyReports/"
    logFile = "/Users/noah.p/PycharmProjects/autoReports/DailyReportsLog/Thrive.log/"
    logName = "Thirve"

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

    def start_browser(self):
        """
        Initilizes the browser
        :return the browser:
        """
        # browser = webdriver.Firefox()
        browser = webdriver.PhantomJS()
        browser.set_window_size(1124, 1000)

        browser.wait = WebDriverWait(browser, 5)
        return browser

    def lookup(self, browser,logger):
        """
        Login to website and navigate to report page
        :param browser:
        :return:
        """
        try:
            url = "https://video.springserve.com/"
            loginPage = browser.get(url)
        except:
            logger.error("Thrive:Failed to load page")
            raise Exception("Error-Thrive:Failed to load page")
        try:
            username = browser.wait.until(EC.visibility_of_element_located((By.ID, "user_email")))
            password = browser.wait.until(EC.visibility_of_element_located((By.ID, "user_password")))

            usernameThrive = "eedo.b@taboola.com"
            passwordThrive = "taboolaspring22!"
            # Type in username and password
            username.send_keys(usernameThrive)
            password.send_keys(passwordThrive)

            # Find sign in button and try to click it
            signInButton = browser.wait.until(EC.element_to_be_clickable((By.NAME, "commit")))
            try:
                signInButton.click()
                reportPage = "https://video.springserve.com/reports"
                browser.get(reportPage)
                if browser.current_url == reportPage:
                    print("Logged in successfully")
            except ElementNotVisibleException:
                signInButton = browser.wait.until(EC.element_to_be_clickable((By.ID, "loginButton")))
                signInButton.click()
        except TimeoutException:
            logger.error(TimeoutException)
            print("Login Box or Button not found on Thrive website")
            print("Login Failed")

    def getData(self, browser,logger):
        """
        Gets the data from the site
        :param browser:
        :return:
        """
        # Get the report page and run the report
        date_report_page = "https://video.springserve.com/reports?date_range=Custom&custom_date_range=" + Thrive.a_month1 + "%2F" + Thrive.a_day1 + "%2F" + Thrive.a_year1 + "+00%3A00+-+" +Thrive.a_month2 + "%2F" + Thrive.a_day2 + "%2F" + Thrive.a_year2 + "+23%3A00&interval=Day&timezone=America%2FNew_York&dimensions%5B%5D=supply_tag_id"
        browser.get(date_report_page)
        # If not loaded correctly try again
        if not (browser.current_url == date_report_page):
            sleep(3)
            browser.get(date_report_page)

        try:
            runReportButton = browser.wait.until(EC.element_to_be_clickable((By.NAME, "commit")))
            try:
                runReportButton.click()
            except Exception:
                logger.error("Thrive: Failed to click run report button")
                raise Exception("Error-Thrive: Failed to click run report button")
        except Exception:
            logger.error("Thrive: Failed to find run report button")
            raise Exception("Error-Thrive: Failed to find run report button")

        try:
            sleep(2)
            # table_row_data = browser.find_elements_by_tag_name("tr")
            table_row_data = browser.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
            # Sleep more if table is not fully loaded( try at most 3 more times
            y = 0
            while (len(table_row_data) < 15 and y < 3):
                sleep(3)
                table_row_data = browser.find_elements_by_tag_name("tr")
                y += 1
        except Exception:
            logger.error("Thrive: the table was not found")
            raise Exception("Error-Thrive: the table was not found")

        # Get the data I want
        table_row_data = table_row_data[12:]
        # Remove the totals row
        del table_row_data[-1]

        rev_list = []
        imp_list = []
        name_list = []
        try:
            sleep(4)
            for table_row in table_row_data:
                table_row = table_row.text
                current_row = table_row.split(" ")
                lengthOfTRow = len(current_row)
                name = current_row[3:13]
                #name = name[0] + "_" + name[1] + "_" + name[2] + "_" + name[3] + "_" + name[4] + "_" + name[5] + name[6] + "_" + name[7] + "_" + name[8] + "_" + name[9]
                name = "".join(name)
                name = name.replace('|', "")
                imp = current_row[16].replace(",", "")
                rev = current_row[18].replace('$', "")
                rev_list.append(rev)
                imp_list.append(imp)
                name_list.append(name)
        except Exception:
            logger.error("Thrive: Some of the table data was not correctly scraped")
            raise Exception("Error-Thrive: Some of the table data was not correctly scraped")
        # Save screen shot
        screenShot = browser.save_screenshot(filename="/Users/noah.p/PycharmProjects/autoReports/DailyReportsLog/ThirveData.png")
        return name_list, imp_list, rev_list


def main():
    tr = Thrive(Thrive.end_date, Thrive.date_post, Thrive.location_of_file, Thrive.dict_T)
    pp = PulsePoint(tr.end_date, tr.date_post, tr.location_of_file, tr.dict_T)
    browser = tr.start_browser()
    logger = pp.logToFile(browser, Thrive.logFile, Thrive.logName)
    tr.lookup(browser,logger)
    name_list_final, imp_list_final, rev_list_final = tr.getData(browser,logger)
    # If the return lists are empty then there must be an error so try again
    if len(name_list_final) is 0 or len(imp_list_final) is 0 or len(rev_list_final) is 0:
        name_list_final, imp_list_final, rev_list_final = tr.getData(browser,logger)
    pp.makeCSV(tr.location_of_file, tr.dict_T, name_list_final, imp_list_final, rev_list_final,tr.end_date, tr.date_post)
    browser.quit()


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
