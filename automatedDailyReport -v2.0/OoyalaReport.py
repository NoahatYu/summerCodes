import json
import time
import csv
from datetime import datetime
from datetime import timedelta
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from PulsePointReport import PulsePoint
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

"""
Author - Noah Potash 08/08/2017
"""

class Ooyala:
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

    logFile = "/Users/noah.p/PycharmProjects/autoReports/DailyReportsDataLog/ooyala.log/"
    logName = "ooyala"


    ooyalaUserName = ""
    ooyalaPassWord = ""

    Username2 = ""
    Password2 = ""

    dayMonthYear = str(end_date).split("/")
    a_month = dayMonthYear[0].zfill(2)
    a_day = dayMonthYear[1].zfill(2)
    a_year = dayMonthYear[2]

    next_day = str(int(a_day) + 1).zfill(2)


    dict_T = {

        "Desktop_direct_instream_Tier3Geos": "Desktop_direct_instream_Tier3_Geos"
    }

    def __init__(self, end_date, date_post, location_of_file, dict_T,ooyalaUserName, ooyalaPassword,Username2,Password2):
        """
        Constructor
        :param end_date:
        :param date_post:
        :param location_of_file:
        :param dict_T:
        :param ooyalaUserName:
        :param ooyalaPassword:
        :param Username2:
        :param Password2:
        """
        self.end_date = end_date
        self.date_post = date_post
        self.location_of_file = location_of_file
        self.dict_T = dict_T
        self.ooyalaUserName = ooyalaUserName
        self.ooyalaPassWord = ooyalaPassword
        self.Username2 = Username2
        self.Password2 = Password2

    def start_browser(self):
        """
        Initilizes the browser
        :return the browser:
        """
        browser = webdriver.PhantomJS()
        browser.set_window_size(1124, 1000)
        browser.wait = WebDriverWait(browser, 5)
        return browser


    def loginTo(self,browser, the_username, the_password,logger):
        """
        Login to website
        :param browser:
        :param the_username:
        :param the_password:
        :param logger:
        :return:
        """
        try:
            loginPage = "http://pulse-ssp.ooyala.com/"
            browser.get(loginPage)

        except Exception:
            logger.error("ooyala:Failed to load page")
            raise Exception("Error-ooyala:Failed to load page")
        try:

            username = browser.wait.until(EC.visibility_of_element_located((By.ID, "email")))
            password = browser.wait.until(EC.visibility_of_element_located((By.ID, "password")))
            signInButton = browser.wait.until(EC.element_to_be_clickable((By.ID, "ok")))

            username.send_keys(the_username)
            password.send_keys(the_password)

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
            print("Login Box or Button not found on ooyala website")
            print("Login Failed")

            # delays for 3 seconds
            #sleep(3)

    def getData(self,browser):
        """
        Gets the data from the site
        :param browser:
        :return the data in JSON:
        """
        sleep(2)
        browser.get("http://pulse-ssp-reporting.ooyala.com")
        sleep(1)
        dataPage = "http://pulse-ssp-reporting.ooyala.com/slices/view/?dimension=site&startdate=" + Ooyala.a_year + "-" + Ooyala.a_month + "-" + Ooyala.a_day + " 04:00&enddate=" + Ooyala.a_year + "-" + Ooyala.a_month + "-" + Ooyala.next_day + " 03:00&datesIncludesTime=true&filters=filterkey:site---filtervalues:127649---&pageNumber=1&pageItemsCount=100&includeSliceOnly=false&columns=imps,publisher_net&currency=USD"
        tableDataRequest = browser.get(dataPage)
        soup = BeautifulSoup(browser.page_source,"html.parser")
        j = json.loads(soup.find("body").text)
        jsonListData = j["data"]["slice"]["slice"]
        browser.quit()

        return jsonListData

    def parseJson(self,json_data):
        """
        Parses the json of the data
        :param json_data:
        :return dp_list,imp_list,rev_list:
        """
        # print(j["data"]["slice"][0]["imps"])
        json_list_length = len(json_data)

        rev_list = []
        imp_list = []
        # Demand partner list
        dp_list = []

        for jdata in json_data:
            # Ignore empty ones since they will be less than 4
            if len(jdata) > 4:
                # Get the domains and add to the list

                current_dp = jdata["site_mapping"]
                current_dp = current_dp.replace("-","_").replace(" ", "")

                dp_list.append(current_dp)
                # Get the impressions and add to list
                current_imp = str(jdata["imps"])
                imp_list.append(current_imp)
                # Get the revenues and add to list - total_sprice:
                current_rev = str(jdata["publisher_net"])
                rev_list.append(current_rev)

        return dp_list,imp_list,rev_list




def main():
    """
    Main method
    :return:
    """
    pp = PulsePoint(PulsePoint.end_date, PulsePoint.date_post, PulsePoint.location_of_file, PulsePoint.dict_T)
    ooyala = Ooyala(Ooyala.end_date, Ooyala.date_post,Ooyala.location_of_file,Ooyala.dict_T,Ooyala.ooyalaUserName,Ooyala.ooyalaPassWord,Ooyala.Username2,Ooyala.Password2)

    #ooyala.runParallel()
    browser = ooyala.start_browser()
    # Start logger
    logger = pp.logToFile(browser, ooyala.logFile, ooyala.logName)
    ooyala.loginTo(browser,ooyala.ooyalaUserName,ooyala.ooyalaPassWord,logger)
    json_data = ooyala.getData(browser)
    dp_list, imp_list, rev_list = ooyala.parseJson(json_data)
    pp.makeCSV(ooyala.location_of_file,ooyala.dict_T,dp_list, imp_list, rev_list,ooyala.end_date,ooyala.date_post)
    print("Done")


if __name__ == "__main__":
    # Run Main method
    main()

