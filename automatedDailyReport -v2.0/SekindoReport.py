import time
from time import sleep
from PulsePointReport import PulsePoint
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

"""
Author - Noah Potash 07/15/2017
"""


class Sekindo:
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

    # Get dates to add to url to get report

    dayMonthYear = str(end_date).split("/")
    a_month = dayMonthYear[0].zfill(2)
    a_day = dayMonthYear[1].zfill(2)
    a_year = dayMonthYear[2]


    the_time = datetime.now()
    location_of_file = "/Users/noah.p/Desktop/DailyReports/"

    logFile = "/Users/noah.p/PycharmProjects/autoReports/DailyReportsDataLog/AutoDailyManualReportslogs.log/"
    logName = "Sekindo"

    dict_T = {
        "TaboolaUSLP": "Sekindo_Direct_Desktop_US_LP",
        "TaboolaUSLPJS": "Sekindo_Direct_Desktop_US_LP_Jscript",
        "TaboolaBRDTJS": "Sekindo_Direct_DT_BRMX_LP_JS",
        "TaboolaENLPJS": "Sekindo_Direct_Tier1_LP_JS"
    }

    def __init__(self, a_year, a_month,a_day, date_post, location_of_file, dict_T):
        """
        Constructor
        :param end_date:
        :param date_post:
        :param location_of_file:
        :param dict_T:
        """
        self.a_year = a_year
        self.a_month = a_month
        self.a_day = a_day
        self.date_post = date_post
        self.location_of_file = location_of_file
        self.dict_T = dict_T

    def start_browser(self):
        """
        Initilizes the browser
        :return the browser:
        """
        browser = webdriver.Firefox()
        browser.wait = WebDriverWait(browser, 5)
        return browser


    def lookup(self,browser,logger):
        """Login to website and navigate to report page
        :param browser:
        :return:
        """
        try:
            url = "https://console.sekindo.com/console/login.php"
            loginPage = browser.get(url)
            logger.info("Sekindo site loaded")
        except Exception:
            logger.error("Error- Sekindo: Failed to load page")
            raise Exception("Error- Sekindo: Failed to load page")
        try:

            username = browser.wait.until(EC.visibility_of_element_located((By.ID, "username")))
            password = browser.wait.until(EC.visibility_of_element_located((By.ID, "password")))
            signInButton = browser.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
            signInButton = browser.find_elements_by_tag_name("button")

            # Find the login button
            for loginbtn in signInButton:
                if loginbtn.text == "Login":
                    # Found it
                    signInButton = loginbtn
                    break


            # Type in username and password
            username.send_keys("")
            sleep(1)
            password.send_keys("")
            # Find sign in button and try to click it
            try:
                sleep(3)
                signInButton.click()
                sleep(3)
                if browser.current_url == "https://console.sekindo.com/console/publishers/multispaces.php":
                    print("Logged in successfully")
                    logger.info("Logged in successfully")
                    #browser.get("https://console.sekindo.com/console/publishers/multispaces.php")
                else:
                    # try again to login and click login button
                    signInButton.click()
            except ElementNotVisibleException:
                signInButton = browser.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
                signInButton.click()
        except TimeoutException:
            logger.error(TimeoutException)
            logger.error("Login Box or Button not found on Sekindo website")
            logger.error("Login Failed")
            print("Login Box or Button not found on Sekindo website")
            print("Login Failed")





    def fillInDateAndRunReport(self,browser,a_year,a_month,a_day,logger):

        # get this page: https://console.sekindo.com/console/publishers/multispaces.php
        """
        Fill in the date for the website and click it
        :param: browser, end_date
        :return:
        """
        sleep(3)
        dropDownBtns = browser.find_elements_by_tag_name("option")
        while len(dropDownBtns) is 0:
            dropDownBtns = browser.find_elements_by_tag_name("option")

        for dataBtn in dropDownBtns:
            if dataBtn.text == "Custom":
                #Found the correct button so click it
                dataBtn.click()
                break

        # finds the date box
        dates_cal = browser.find_elements_by_class_name("sekindoRedBorder")
        fromDay = dates_cal[0]
        toDay = dates_cal[1]
        # Format is yyyy-dd-mm
        fromDay.send_keys(a_year + "-" + a_month + "-" + a_day)
        toDay.send_keys(a_year + "-" + a_month + "-" + a_day)



    def getData(self,browser,logger):
        """
        Webscrape the data and export to .csv files
        :return name, impressions and revenue lists:
        """
        try:
            # Forces loader to throw an exception so that is when the page has fully loaded
            while len(loader) > 0:
                loader = browser.wait.until(EC.visibility_of_all_elements_located((By.ID, "frotateG_01")))
                sleep(6)
        except:
            try:
                sleep(2)
                # Find the reports data
                # Once the exception is caught. It is know that the page is ready to be scraped
                #sleep(6)
                dropDownBtns = browser.find_elements_by_tag_name("option")
                # FInd the number of values on page and expand it to the max so
                for numBtn in dropDownBtns:
                    if numBtn.text == "250":
                        # Found the correct button so click it
                        numBtn.click()
                        break
            except:
                # Tries to find by tag name "table" and if fails tries another method by another tag name
                try:
                    sleep(3)
                    reportsPage = browser.find_element_by_tag_name("sekindo-quick-stats")
                    reportsPageData2 = reportsPage.text
                    reportsPageDataList = reportsPageData2.splitlines()
                    reportsPageData = reportsPage.text

                except:
                    logger.error("Failed to find table data")
                    raise Exception("Error- Sekindo: Failed to find table data")

        name_list2 = []
        imp_list = []
        rev_list = []
        sleep(10)
        tableData = browser.find_elements_by_tag_name("table")
        tableDataList = tableData[0].text.splitlines()
        data_list = tableDataList

        name_list = data_list[7::2]
        imp_rev_list = data_list[8::2]
        the_length = len(imp_rev_list)

        # The campaigns
        the_name_list = ["TaboolaUSLP","TaboolaUSLPJS", "TaboolaBRDTJS","TaboolaENLPJS"]

        # Loops through all data to single out impressions and revenue to correspond to name/domain/reportname
        i = 0
        while i < the_length:
            current_name = name_list[i].split(" ")
            current_data = imp_rev_list[i].split(" ")
            # Delete the id (which is not needed)
            del current_name[0]
            current_name = "".join(current_name)
            # Only add the values that correctly correspond to the correct names.
            if current_name in the_name_list:
                name_list2.append(current_name)
                imp_list.append(current_data[2])
                rev_list.append(current_data[4])
            i += 1
        #Save screen shot
        sleep(6)
        # Scroll down to bottom of page
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        screenShot = browser.save_screenshot(filename="/Users/noah.p/PycharmProjects/autoReports/DailyReportsDataLog/SekindoData.png")

        return name_list2, imp_list, rev_list




def main():
    """
    Main method
    :return:
    """
    sk = Sekindo(Sekindo.a_year,Sekindo.a_month,Sekindo.a_day,Sekindo.date_post, Sekindo.location_of_file,Sekindo.dict_T)
    pp = PulsePoint(Sekindo.end_date, Sekindo.date_post, Sekindo.location_of_file,Sekindo.dict_T)
    browser = sk.start_browser()
    logger = pp.logToFile(browser, Sekindo.logFile, Sekindo.logName)
    sk.lookup(browser, logger)
    sk.fillInDateAndRunReport(browser, sk.a_year,sk.a_month,sk.a_day, logger)
    name_list, imp_list, rev_list = sk.getData(browser, logger)
    if len(name_list) is 0 or len(imp_list) is 0 or len(rev_list) is 0:
        name_list, imp_list, rev_list = sk.getData(browser, logger)

    pp.makeCSV(sk.location_of_file, sk.dict_T, name_list, imp_list, rev_list, sk.end_date, sk.date_post)
    browser.quit()

if __name__ == "__main__":
    main()
