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
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

class PulsePoint:
    start_time_pp = time.time()
    #TODO: Log all results, such as errors and importantly the time it takes to run the script
    """Gets all the dates and times that are needed for this class"""
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
    location_of_file = "/Users/noah.p/Documents/Daily_Reports_July_12/PulsePoint_July_12/"
    #location_of_file = "/Users/noah.p/Desktop/TestFolder/"


    dict_T = {
        'TaboolaVideo$5': "Pulse_Point_Direct_Desktop_BTU_Standard_5",
        'TaboolaVideo$6': "Pulse_Point_Direct_Desktop_BTU_Standard_6",
        'TaboolaVideo$7': "Pulse_Point_Direct_Desktop_BTU_Standard_7"
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
        """Login to website and navigate to report page
        :param browser:
        :return:
        """
        try:
            url = "https://exchange.pulsepoint.com/AccountMgmt/Login.aspx?app=publisher&ReturnUrl=%2fPublisher%2fReports.aspx#/Reports"
            loginPage = browser.get(url)
        except Exception:
            raise Exception("Error- PulsePoint: Failed to load page")
        try:
            try:
                alertOnPage = browser.wait.until(EC.visibility_of_element_located((By.ID, "announcementContainer")))
                print("Announcement: " + alertOnPage.text)
            except:
                pass

            #username = browser.find_element_by_id("UserName")
            #password = browser.find_element_by_id("Password")
            username = browser.wait.until(EC.visibility_of_element_located((By.ID, "UserName")))
            password = browser.wait.until(EC.visibility_of_element_located((By.ID, "Password")))
            signInButton = browser.wait.until(EC.element_to_be_clickable((By.ID, "LoginButton")))

            # Type in username and password
            username.send_keys("Taboola_VideoTag")
            password.send_keys("Belk09po")
            # Find sign in button and try to click it
            try:
                signInButton.click()
                print("Logged in successfully")
            except ElementNotVisibleException:
                signInButton = browser.wait.until(EC.visibility_of_element_located((By.ID, "loginButton")))
                signInButton.click()
        except TimeoutException:
            print("Login Box or Button not found on PulsePoint website")
            print("Login Failed")


    def fillInDateAndRunReport(self,browser,end_date):
        """
        Fill in the date for the website and click it
        :param: browser, end_date
        :return:
        """
        date_from = browser.wait.until(EC.visibility_of_element_located((By.ID, "dateFrom")))
        date_from.clear()
        date_from.send_keys(end_date)

        # Put in the date for date to
        date_to = browser.wait.until(EC.visibility_of_element_located((By.ID, "dateTo")))
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
            runReportButton = browser.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
            for btn in runReportButton:
                if btn.text == "RUN REPORT":
                    runReportButton.send_keys(Keys.ENTER)

    def getData(self,browser):
        """
        Webscrape the data and export to .csv files
        :return name, impressions and revenue lists:
        """
        # Tries to find by class name and if fails tries another method by id and parsing a string to get the data.
        try:
            name_col = browser.wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "nameCol")))
            rev_col = browser.wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "revenueCol")))
            paid_imps_col = browser.wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "paidImpsCol")))

        except:
            try:
                reports_data_container = browser.wait.until(EC.visibility_of_element_located((By.ID, "reports-data-container")))
                name_list2 = []
                imp_list2 = []
                rev_list2 = []
                reports_data_container = browser.wait.until(EC.visibility_of_element_located((By.ID, "reports-data-container")))
                sleep(3)
                rsd = reports_data_container.text
                reports_data_containers = rsd.splitlines()
                if len(reports_data_containers) < 11:
                    sleep(5)
                    reports_data_containers = rsd.splitlines()

                t5 = reports_data_containers[30:43]
                t6 = reports_data_containers[43:56]
                t7 = reports_data_containers[56:68]

                name_list2.append(t5[0])
                name_list2.append(t6[0])
                name_list2.append(t7[0])
                imp_list2.append(t5[9])
                imp_list2.append(t6[9])
                imp_list2.append(t7[9])
                rev_list2.append(t5[7])
                rev_list2.append(t6[7])
                rev_list2.append(t7[7])

                return name_list2,imp_list2,rev_list2
            except Exception:
                raise Exception("Error- PulsePoint: Failed to find table data")

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


        return name_list, imp_list, rev_list


    def makeCSV(self,location_of_file, dict_T, name_list,imp_list,rev_list,end_date,date_post):

        numberOfItems = len(name_list)

        # Write to csv file
        q = 0
        while q < numberOfItems:
            try:
                name_of_file = name_list[q].text
                imp = imp_list[q].text.replace(",", "")
                rev = rev_list[q].text.replace("$", "")
            except:
                name_of_file = name_list[q]
                imp = imp_list[q].replace(",","")
                rev = rev_list[q].replace("$","")

            name_of_file = name_of_file.replace(" ","")

            with open(location_of_file + dict_T[name_of_file] + "|" + date_post.replace(" ", "_") + ".csv", "w") as csv_file:
                fileWriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                fileWriter.writerow(["Date", "Impressions", "Revenue"])
                fileWriter.writerow([end_date, imp, rev])
            q += 1
def main():
    pp = PulsePoint(PulsePoint.end_date,PulsePoint.date_post, PulsePoint.location_of_file,PulsePoint.dict_T)
    browser = pp.init_browser()
    pp.lookup(browser)
    pp.fillInDateAndRunReport(browser, pp.end_date)
    name_list, imp_list, rev_list = pp.getData(browser)
    if len(name_list) is 0 or len(imp_list) is 0 or len(rev_list) is 0:
        name_list_final, imp_list_final, rev_list_final = pp.getData(browser)
    pp.makeCSV(pp.location_of_file, pp.dict_T, name_list, imp_list, rev_list, pp.end_date, pp.date_post)
    browser.quit()
    print("Done!")
    print("PulsePoint program took --- %s seconds ---" % (time.time() - PulsePoint.start_time_pp))

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
