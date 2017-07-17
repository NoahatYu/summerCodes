import re
import csv
import time
#import sendEmail
from PulsePointReport import PulsePoint
from time import sleep
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from bs4 import BeautifulSoup

class Optimatic:
    # The calender is weird so got to go back a month
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
    yesterday = the_time.day - 1

    dict_T = {

        "Taboola APAC HK": "Taboola APAC HK".replace(" ", "_"),
        "Taboola APAC ID": "Taboola APAC ID".replace(" ", "_"),
        "Taboola APAC JP": "Taboola APAC JP".replace(" ", "_"),
        "Taboola APAC MY": "Taboola APAC MY".replace(" ", "_"),
        "Taboola APAC MY $3 floor": "Taboola APAC MY $3 floor".replace(" ", "_"),
        "Taboola APAC PH": "Taboola APAC PH".replace(" ", "_"),
        "Taboola APAC SG": "Taboola APAC SG".replace(" ", "_"),
        "Taboola APAC SG $3.5 floor": "Taboola APAC SG $3.5 floor".replace(" ", "_"),
        "Taboola APAC TH": "Taboola APAC TH".replace(" ", "_"),

    }

    def __init__(self, end_date, date_post, the_time, dict_T):
        """
        Constructor
        :param end_date:
        :param date_post:
        :param location_of_file:
        :param dict_T:
        """
        self.end_date = end_date
        self.date_post = date_post
        self.the_time = the_time
        self.dict_T = dict_T

    def start_browser(self):
        """
        Initilizes the browser
        :return the browser:
        """
        # NOTE: THIS MUST RUN PHANTOMJS
        #browser = webdriver.Firefox()
        browser = webdriver.PhantomJS()
        #browser.maximize_window()
        browser.set_window_size(1124, 1000)

        browser.wait = WebDriverWait(browser, 5)
        return browser

    def lookup(self, browser):
        """
        Navigates to the reports page
        :param browser:
        :return:
        """

        try:
            loginPage = browser.get('https://publishers.optimatic.com/Portal2/default.aspx')
        except Exception:
            raise Exception("Error-Optimatic:Failed to load the page")
        try:
            username = browser.wait.until(EC.visibility_of_element_located((By.ID, "txtUserName")))
            password = browser.wait.until(EC.visibility_of_element_located((By.ID, "txtPassword")))
            #username = browser.find_element_by_id("txtUserName")
            #password = browser.find_element_by_id("txtPassword")
            username.send_keys("taboola@selectmedia")
            password.send_keys("Banana")
            # Find sign in button, browser.find_element_by_tag_name("button")
            signInButton = browser.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
            try:
                # Click the sign in button
                signInButton.click()
            except Exception:
                raise Exception("Error: Unable to click login button")

        except Exception:
            raise Exception("Unable to locate or inputs values into login boxes")

        reportsPage = "https://publishers.optimatic.com/Portal2/reports/"
        # Get the reports page
        browser.get(reportsPage)
        if browser.current_url == reportsPage:
            print("Logged in successfully")

        try:
            # Here is a list of all the buttons on the page
            AllButtonsOnHeader = browser.find_elements_by_class_name('menuLabel')
        except:
            numOfButtons = len(AllButtonsOnHeader)
            if numOfButtons < 1:
                raise Exception("Error-Optimatic: Unable to find any buttons on page")
        # Look for the report button out of all buttons on the page
        i = 0
        for button in AllButtonsOnHeader:
            if(button.text == "REPORTING"):
                break
            else:
                i += 1
        reportingButton = AllButtonsOnHeader[i]
        if not reportingButton.text == "REPORTING":
            print("Error-Optimatic: Unable to find reporting button")
        try:
            # Click the reporting button
            reportingButton.click()
        except Exception:
            raise Exception("Error- Optimatic: Element Is Not Selectable")

        waitForIt = browser.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'headerTitle')))
        print("Page is ready!")

    def fillInDateAndRunReport(self, browser, the_time):
        """
        Fills in the date in the calenders on the site and runs the report
        :param browser:
        :param the_time:
        :return: all_list_containers
        """
        #select_report_type_btn = browser.find_element_by_class_name('headerTitle')
        try:
            select_report_type_btn = browser.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "headerTitle")))
            try:
                select_report_type_btn.click()
            except Exception:
                raise Exception("Error-Optimatic: select report button not clickable")
        except Exception:
            raise Exception("Error-Optimatic:Unable to find select report type button")

        all_list_containers = browser.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "label")))

        #all_list_containers = browser.find_elements_by_class_name('label')
        try:
            domain_btn = all_list_containers[2].click()
        except:
            print("ERROR: Domain button not clickable, Trying again...")
            # try again after waiting 5 seconds
            sleep(5)
            try:
                all_list_containers = browser.find_elements_by_class_name('label')
                domain_btn = all_list_containers[2].click()
                print("Success!")
            except Exception:
                raise Exception("Error-Optimatic:Failure to find domain button")

        # calendar_chart = browser.find_element_by_class_name('calendarLabel')
        try:
            calendar_chart = browser.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "calendarLabel")))
            try:
                calendar_chart.click()
            except Exception:
                raise Exception("Error-Optimatic: could not click calendar chart button")
        except Exception:
            raise Exception("Error-Optimatic:Could not find calender chart button")

        try:
            calender_date = browser.find_elements_by_class_name('ui-state-default')
        except Exception:
            raise Exception("Error-Optimatic: unable to locate calender")

        numberOfDaysInMonth = len(calender_date) / 2
        numberOfDaysInMonth = int(numberOfDaysInMonth)

        # 2 calenders and 30 days c1: 0:1 - 29:30 and c2: 30:1 - 60:30
        # if 31 days c1: 0:1 - 30:31 and c2: 31:1 - 62:31

        two_days_past = the_time.day - 2
        two_days_past_str = str(two_days_past)
        counter = 1

        try:
            # Prevoius month method
            if (self.yesterday == 1):
                self.prevoiusMonth()

            calender_dates = browser.find_elements_by_xpath('//a[@href="'+'#'+'"]')
            first_half_cal = calender_date[:len(calender_date) // 2]
            second_half_cal = calender_date[len(calender_date) // 2:]

            first_cal_date = first_half_cal[two_days_past - 1]
            second_cal_date = second_half_cal[two_days_past - 1]

            first_cal_date.click()
            second_cal_date.click()


        except:
            print("ERROR: unable to find calender dates, trying again...")
            try:
                if (self.yesterday == 1):
                    self.prevoiusMonth()

                calender_dates = browser.find_elements_by_link_text(two_days_past_str)
                # Click both buttons
                for date_btn in calender_dates:
                    date_btn.click()
                print("Success!")
            except Exception:
                raise Exception("Error-Optimatic:Failed to find calender")
        try:
            # Get the 'ok' button and click it
            ok_btn = browser.find_elements_by_class_name('button')
            try:
                ok_btn[(len(ok_btn) - 1)].click()
            except Exception:
                raise Exception("Error-Optimatic: unable to click 'OK' button")
        except Exception:
            raise Exception("Error-Optimatic: unable to locate 'Ok' Button")

        return all_list_containers

    def getDataAndMakeCSV(self, browser,end_date, date_post):
        """
        Scrapes the data from the website and exports it as an CSV file
        :param browser:
        :param all_list_containers:
        :return:
        """
        # Split the list to get the taboolas I would like
        all_list_containers = browser.find_elements_by_class_name('label')
        select_report_type_DropDownList = all_list_containers[5:14]
        numberOfTaboolas = len(select_report_type_DropDownList)
        # sleep(3)
        q = 0
        while(q < numberOfTaboolas):
            # After the first taboola is done the buttons need to be reloaded
            if(q > 0):
                sleep(2)
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

            # note: Ads delivered is paid impressions
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
            location_of_file = "/Users/noah.p/Desktop/DailyReports/"
            indexer = 0

            # Makes sure to not create a csv file for one with no data
            if not(len(paid_impressions_list) is 0 and len(domain_list) is 0 and len(revenue_list) is 0):
                # Write to csv file
                with open(location_of_file + self.dict_T[current_Taboola] + "|" + date_post.replace(" ", "_") + ".csv", "w") as csv_file:
                    fileWriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    fileWriter.writerow(["Date", "Site", "Impressions", "Revenue"])
                    # Write to file
                    while(indexer < (numberOfElements - 1)):
                        fileWriter.writerow([end_date, domain_list[indexer], paid_impressions_list[indexer], revenue_list[indexer]])
                        indexer += 1
                q += 1
            else:
                q += 1

    def prevoiusMonth(self, browser, the_time):
        """
        Check if current date is the 1st then got to go back a month on calender and click it, one day
        :param browser:
        :param the_time:
        :return:
        """
        try:
            one_month_past = browser.find_elements_by_class_name('ui-datepicker-prev')
            try:
                # Right calender
                one_month_past[0].click()
                # Left calender
                one_month_past[1].click()
            except:
                raise Exception("Error-Optimatic: unable to click one month back button on calender")
        except:
            raise Exception("Error-Optimatic: could not find one month back button on calender")

def main():
    """
    Main method
    :return:
    """
    op = Optimatic(Optimatic.end_date, Optimatic.date_post, Optimatic.the_time, Optimatic.dict_T)
    browser = op.start_browser()
    op.lookup(browser)
    all_list_containers = op.fillInDateAndRunReport(browser, op.the_time)
    # If the return list is empty then there must be an error, so try again
    if len(all_list_containers) is 0:
        all_list_containers = op.fillInDateAndRunReport(browser, op.the_time)
    op.getDataAndMakeCSV(browser,op.end_date,op.date_post)
    browser.quit()


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
