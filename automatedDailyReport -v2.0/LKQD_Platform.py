import time
import csv
from datetime import datetime
from datetime import timedelta
# import sendEmail
from time import sleep
from selenium import webdriver
from PulsePointReport import PulsePoint
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class LKQD:
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

    location_of_file = "/Users/noah.p/Desktop/DailyReports/"

    logFile = "/Users/noah.p/PycharmProjects/autoReports/DailyReportsLog/LKQD.log/"
    logName = "LKQD"

    #browser = webdriver.PhantomJS()
    #browser.set_window_size(1120, 550)

    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    #the_path = "/Users/noah.p/going_headless/chromedriver"
    #browser = webdriver.Chrome(executable_path=the_path, chrome_options=chrome_options)

    dict_T = {
        "TaboolaMWMXIOS$1floor": "SelectMedia_MW_MX-IOS_$1_floor",
        "TaboolaMWJPIOS$2floor": "SelectMedia_MW_JP-IOS_$2_floor",
        "TaboolaMWAUSAndroid$2floor": "SelectMedia_MW_AUS_Android_$2_floor",
        "TaboolaMWSGAndroid$2floor": "SelectMedia_MW_SG-Android_$2_floor",
        "TaboolaMWSGIOS$2floor": "SelectMedia_MW_SG-IOS_$2_floor",
        "TaboolaMWMXAndroid$1floor": "SelectMedia_MW_MX-Android_$1_floor",
        "TaboolaMWHKIOS$1floor": "SelectMedia_MW_HK-IOS_$1_floor",
        "TaboolaMWBRIOS$0.5floor": "SelectMedia_MW_BR-IOS_$0.5_floor",
        "TaboolaMWBRIOS$1floor": "SelectMedia_MW_BR-IOS_$1_floor",
        "TaboolaMWHKAndroid$1floor": "SelectMedia_MW_HK-Android_$1_floor"

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
            loginPage = "https://ui.lkqd.com/login"
            browser.get(loginPage)

        except Exception:
            logger.error("LKQD:Failed to load page")
            raise Exception("Error-LKQD:Failed to load page")
        try:
      
            username = browser.wait.until(EC.visibility_of_element_located((By.ID, "username")))
            password = browser.wait.until(EC.visibility_of_element_located((By.ID, "password")))
            signInButton = browser.wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))

            username.send_keys("")
            password.send_keys("")

            #signInButton = browser.find_element_by_tag_name("button")
            try:
                # Click the sign in button
                signInButton.click()
                logger.info("Logged in")
                print("Logged in successfully")
            except ElementNotVisibleException:
                signInButton = browser.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
                if(signInButton.text == "Sign In"):
                    signInButton.click()
        except TimeoutException:
            logger.error(TimeoutException)
            print("Login Box or Button not found on LKQD website")
            print("Login Failed")

            # delays for 3 seconds
            #sleep(3)

    def fillInDateAndRunReport(self, browser, end_date, logger):
        # Here is a list of all the buttons on the page
        reportTableIsLoaded = browser.find_elements_by_class_name("report-table")
        i = 0
        while len(reportTableIsLoaded) is 0:
            sleep(1)
            reportTableIsLoaded = browser.find_elements_by_class_name("report-table")
            i += 1

        AllButtonsOnReportPage = browser.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".btn")))
        numOfButtons = len(AllButtonsOnReportPage)
        #If not all the buttons loaded wait and try again
        if numOfButtons < 20:
            sleep(5)
            AllButtonsOnReportPage = browser.find_elements_by_css_selector('.btn')

        dailyReportButton = AllButtonsOnReportPage[5]
        try:
            # Click to set to daily report button
            dailyReportButton.click()
            dailyReportButton.send_keys(Keys.ARROW_DOWN)
        except Exception:
            logger.error("LKQD: Unable to click daily report button")
            raise Exception("Error-LKQD: Unable to click daily report button")

        # Find dropdown menu for daily report and click it
        dailyReportDropDownList = browser.find_elements_by_class_name('dropdown-menu')
        while len(dailyReportDropDownList) is 0:
            sleep(1)
            dailyReportDropDownList = browser.wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "dropdown-menu")))
        try:
            # Click the drop down menu button
            dailyReportDropDownList[3].click()
        except Exception:
            logger.error("LKQD: unable to click drop down menu button")
            raise Exception("Error-LKQD: unable to click drop down menu button")
        try:
            # Find the date tab and click on it
            #customDateRangeTab = browser.find_element_by_tag_name('lkqd-date-range')
            customDateRangeTab = browser.wait.until(EC.element_to_be_clickable((By.TAG_NAME, "lkqd-date-range")))
            try:
                customDateRangeTab.click()
            except Exception:
                logger.error("LKQD: unable to click custom range tab button")
                raise Exception("Error-LKQD: unable to click custom range tab button")
        except Exception:
            logger.error("LKQD: Unable to find custom date range tab")
            raise Exception("Error-LKQD: Unable to find custom date range tab")

        # Enter the date in the data field for start date and end data
        sleep(1)
        try:
            #customDateRangeStart = browser.find_element_by_name('daterangepicker_start')
            customDateRangeStart = browser.wait.until(EC.visibility_of_element_located((By.NAME, 'daterangepicker_start')))

            customDateRangeEnd = browser.find_element_by_name('daterangepicker_end')

            #applyButton = browser.find_element_by_class_name('applyBtn')
            applyButton = browser.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "applyBtn")))

            try:
                # Custom range start
                customDateRangeStart.clear()
                customDateRangeStart.send_keys(end_date)
                # Custom range end
                customDateRangeEnd.clear()
                customDateRangeEnd.send_keys(end_date)
                # Hit the apply button
                applyButton.click()
            except Exception:
                logger.error("LKQD: Unable to enter custom date range info and click apply button")
                raise Exception("Error-LKQD: Unable to enter custom date range info and click apply button")
        except Exception:
            logger.error("LKQD: Unable to find range info fields and apply button")
            raise Exception("Error-LKQD: Unable to find range info fields and apply button")
        try:
            # Tries to find the run report button and will try at least 5 times
            AllButtonsOnReportPage = browser.find_elements_by_css_selector('.btn')
            runReportButton = AllButtonsOnReportPage[14]
            w = 1
            while (not runReportButton.text == "Run Report") and w < 6:
                logger.info("Could not find the run report button, trying again...")
                print("Could not find the run report button, trying again...")
                sleep(w)
                AllButtonsOnReportPage = browser.find_elements_by_css_selector('.btn')
                runReportButton = AllButtonsOnReportPage[14]
                w += 1

            try:
                runReportButton.click()
                print("Found it, Ran report")
                logger.info("Found button and ran report")
            except Exception:
                logger.error("LKQD:unable to click run report button")
                raise Exception("Error-LKQD:unable to click run report button")
        except:
            print("Unable to find run report button, trying again...")
            try:
                sleep(3)
                runReportButton = browser.find_element_by_class_name("run-report-button")
                runReportButton.click()
            except Exception:
                logger.error("LKQD: Unable to find run report button")
                raise Exception("Error-LKQD: Unable to find run report button")


    def getData(self,browser,logger):
        """
        Gets data from webpage
        :param browser:
        :return:
        """
        #reportTable = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[2]/table')

        # The loading wheel on the website (on a mac it looks like a lolipop(on the website it does not))
        lollipop = browser.find_elements_by_class_name("operation-in-progress-overlay")
        # Tries 3 different ways of getting the table data by class name then by tag name then by id

        try:
            # Waits for the page to completely load
            while(len(lollipop) is not 0):
                lollipop = browser.find_elements_by_class_name("operation-in-progress-overlay")
                sleep(1)
            reportTable = browser.find_elements_by_class_name("report-table")
            reportTable = reportTable[1]
            report_table_data = reportTable.text.splitlines()
            report_table_data = report_table_data[15:]
            del report_table_data[2::3]

        except:
            try:
                while (len(lollipop) is not 0):
                    lollipop = browser.find_elements_by_class_name("operation-in-progress-overlay")
                    sleep(1)
                reportTable = browser.find_element_by_tag_name("table")
                report_table_data = reportTable.text.splitlines()
                report_table_data = report_table_data[15:]
                taboolas = report_table_data[2::3]
            except:
                try:
                    while (len(lollipop) is not 0):
                        lollipop = browser.find_elements_by_class_name("operation-in-progress-overlay")
                        sleep(1)
                    reportTable = browser.find_elements_by_id('reports')
                    report_table_data = reportTable.text.splitlines()
                    report_table_data = report_table_data[42:len(report_table_data) - 3]
                    del report_table_data[2::3]
                except Exception:
                    logger.error("LKQD: Failed to find data from table")
                    raise Exception("Error-LKQD: Failed to find data from table")


        name_list = report_table_data[::2]
        the_length = len(name_list)
        data_list = report_table_data[1::2]

        final_name_list = []
        final_imp_list = []
        final_rev_list = []

        i = 0
        while(i < the_length):
            current_T = name_list[i].split(" ")
            # Remove unwanted info
            del current_T[0]

            current_T = " ".join(current_T)
            current_data = data_list[i].split(" ")
            current_imp = current_data[1]
            current_rev = current_data[5]
            # Add to each to own list
            final_name_list.append(current_T)
            final_imp_list.append(current_imp)
            final_rev_list.append(current_rev)
            i += 1

        # Scroll down to bottom of page
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Save screen shot
        screenShot = browser.save_screenshot(filename="/Users/noah.p/PycharmProjects/autoReports/DailyReportsLog/LKQDData.png")

        return final_name_list, final_imp_list, final_rev_list


def main():
    """
    Main method
    :return:
    """
    pp = PulsePoint(PulsePoint.end_date, PulsePoint.date_post, PulsePoint.location_of_file, PulsePoint.dict_T)
    lkqd = LKQD(LKQD.end_date,LKQD.date_post,LKQD.location_of_file,LKQD.dict_T)
    browser = lkqd.start_browser()
    logger = pp.logToFile(browser, LKQD.logFile, LKQD.logName)
    lkqd.lookup(browser,logger)
    lkqd.fillInDateAndRunReport(browser, lkqd.end_date,logger)
    final_name_list, final_imp_list, final_rev_list = lkqd.getData(browser,logger)
    if len(final_name_list) is 0 or len(final_imp_list) is 0 or len(final_rev_list) is 0:
        final_name_list, final_imp_list, final_rev_list = lkqd.getData(browser,logger)
    pp.makeCSV(lkqd.location_of_file, lkqd.dict_T, final_name_list, final_imp_list, final_rev_list, lkqd.end_date, lkqd.date_post)
    browser.quit()


if __name__ == "__main__":
    # Run Main method
    main()
