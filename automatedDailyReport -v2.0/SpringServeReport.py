import time
import logging
import csv
from datetime import datetime
from datetime import timedelta
from time import sleep
from selenium import webdriver
from PulsePointReport import PulsePoint
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0


class SpringServe:
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

    a_year1 = str(the_time.year % 100)
    a_month1 = str(the_time.month)
    a_day1 = str(the_time.day - 2)
    a_year2 = str(the_time.year % 100)
    a_month2 = str(the_time.month)
    a_day2 = str(the_time.day - 2)

    location_of_file = "/Users/noah.p/Desktop/DailyReports/"

    logFile = "/Users/noah.p/PycharmProjects/autoReports/DailyReportsLog/SpringServe.log/"
    logName = "SpringServe"


    dict_T = {"Taboola-MX$1Floor": "Taboola MX $1 Floor".replace(" ", "_"), "TaboolaAUS$2.5Floor": "Taboola AUS $2.5 Floor".replace(" ", "_"),
               "Taboola-JS-AUS$2.5Floor": "Taboola-JS-AUS $2.5 Floor".replace(" ", "_"),
               "TaboolaBR$1Floor": "Taboola BR $1 Floor".replace(" ", "_"),
               "TaboolaAnglo+FR+DESP$4Floor": "Taboola Anglo +FR +DE SP $4 Floor".replace(" ", "_"),
               "Taboola-JS-Anglo+FR+DESP$4Floor": "Taboola-JS-Anglo +FR +DE SP $4 Floor".replace(" ", "_")
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

    def start_browser(self):
        """
        Initilizes the browser
        :return the browser:
        """
        #browser = webdriver.Firefox()
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
        except Exception:
            raise Exception("Error- SpringServe:Failed to load page")

        try:
            username = browser.wait.until(EC.visibility_of_element_located((By.ID, "user_email")))
            password = browser.wait.until(EC.visibility_of_element_located((By.ID, "user_password")))

            # Type in username and password
            username.send_keys("or.ben@taboola.com")
            password.send_keys("Orben1234!")

            # Find sign in button and try to click it
            signInButton = browser.wait.until(EC.element_to_be_clickable((By.NAME, "commit")))
            try:
                signInButton.click()
                reportPage = "https://video.springserve.com/reports"
                browser.get(reportPage)
                if browser.current_url == reportPage:
                    print("Logged in successfully")
                    logger.info("Logged in successfully")
            except ElementNotVisibleException:
                signInButton = browser.wait.until(EC.visibility_of_element_located((By.ID, "loginButton")))
                signInButton.click()
        except TimeoutException:
            logger.error("Login Box or Button not found on SpringServe website")
            logger.error("Login Failed")
            print("Login Box or Button not found on SpringServe website")
            print("Login Failed")

    def getData(self, browser,logger):
        """
        Gets the data from the site
        :param browser:
        :return:
        """
        # Get the report page and run the report
        date_report_page = "https://video.springserve.com/reports?date_range=Custom&custom_date_range=" + SpringServe.a_month1 + "%2F" + SpringServe.a_day1 + "%2F" + SpringServe.a_year1 + "+00%3A00+-+" + SpringServe.a_month2 + "%2F" + SpringServe.a_day2 + "%2F" + SpringServe.a_year2 + "+23%3A00&interval=Day&timezone=America%2FNew_York&dimensions%5B%5D=supply_tag_id"
        browser.get(date_report_page)
        # If not loaded correctly try again
        if not(browser.current_url == date_report_page):
            sleep(3)
            browser.get(date_report_page)

        try:
            runReportButton = browser.wait.until(EC.element_to_be_clickable((By.NAME, "commit")))
            try:
                runReportButton.click()
            except Exception:
                logger.error("SpringServe: Failed to click run report button")
                raise Exception("Error- SpringServe: Failed to click run report button")
        except Exception:
            logger.error("SpringServe: Failed to find run report button")
            raise Exception("Error- SpringServe: Failed to find run report button")

        try:
            sleep(2)
            #table_row_data = browser.find_elements_by_tag_name("tr")
            table_row_data = browser.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
            # Sleep more if table is not fully loaded(try at most 3 more times)
            y = 0
            while(len(table_row_data) < 17 and y < 3):
                sleep(3)
                table_row_data = browser.find_elements_by_tag_name("tr")
                y += 1
        except Exception:
            logger.error("SpringServe: the table was not found")
            raise Exception("Error- SpringServe: the table was not found")

        # Get the data I want
        table_row_data = table_row_data[10:]
        # Remove the totals row
        del table_row_data[-1]

        rev_list = []
        imp_list = []
        name_list = []
        try:
            for table_row in table_row_data:
                table_row = table_row.text
                current_row = table_row.split(" ")
                lengthOfTRow = len(current_row)

                if(lengthOfTRow is 15):
                    name = current_row[3:6]
                    #name = name[0] + name[1] + name[2]
                    name = "".join(name)
                    imp = current_row[9]
                    rev = current_row[11]
                    rev_list.append(rev)
                    imp_list.append(imp)
                    name_list.append(name)

                elif(lengthOfTRow is 16):
                    name = current_row[3:7]
                    #name = name[0] + name[1] + name[2] + name[3]
                    name = "".join(name)
                    imp = current_row[10]
                    rev = current_row[12]
                    rev_list.append(rev)
                    imp_list.append(imp)
                    name_list.append(name)

                elif(lengthOfTRow is 19):
                    name = current_row[3:10]
                    #name = name[0] + name[1] + name[2] + name[3] + name[4] + name[5] + name[6]
                    name = "".join(name)
                    imp = current_row[13]
                    rev = current_row[15]
                    rev_list.append(rev)
                    imp_list.append(imp)
                    name_list.append(name)

                else:
                    logger.error("SpringServe: Some Table data was not found and might be missing")
                    print("Error- SpringServe: Some Table data was not found and might be missing")
        except Exception:
            logger.error("SpringServe: Some of the table data was not correctly scraped")
            print("Error- SpringServe: Some of the table data was not correctly scraped")

        # Save screen shot
        screenShot = browser.save_screenshot(filename="/Users/noah.p/PycharmProjects/autoReports/DailyReportsLog/SpringServeData.png")
        return name_list, imp_list, rev_list


def main():
    """
    Main method
    :return:
    """
    ssr = SpringServe(SpringServe.end_date, SpringServe.date_post, SpringServe.location_of_file, SpringServe.dict_T)
    pp = PulsePoint(ssr.end_date, ssr.date_post, ssr.location_of_file, ssr.dict_T)

    browser = ssr.start_browser()
    logger = pp.logToFile(browser, SpringServe.logFile, SpringServe.logName)
    ssr.lookup(browser,logger)
    name_list_final, imp_list_final, rev_list_final = ssr.getData(browser,logger)
    # If the return lists are empty then there must be an error so try again
    if len(name_list_final) is 0 or len(imp_list_final) is 0 or len(rev_list_final) is 0:
        name_list_final, imp_list_final, rev_list_final = ssr.getData(browser,logger)
    pp.makeCSV(ssr.location_of_file, ssr.dict_T, name_list_final, imp_list_final, rev_list_final,ssr.end_date, ssr.date_post)
    browser.quit()

if __name__ == "__main__":
    main()
