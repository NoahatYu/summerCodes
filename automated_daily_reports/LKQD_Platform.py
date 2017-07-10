import time
import csv
import requests
#import sendEmail
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class LKQD:

    # Monday is 0 and Sunday is 6
    DayOfTheWeek = datetime.today().weekday()
    #browser = webdriver.PhantomJS()
    #browser.set_window_size(1120, 550)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    the_path = "/Users/noah.p/going_headless/chromedriver"
    browser = webdriver.Chrome(executable_path=the_path, chrome_options=chrome_options)

    browser.get('https://ui.lkqd.com/login')
    #assert 'Yahoo!' in browser.title

    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")


    username.send_keys("")
    password.send_keys("")

    signInButton = browser.find_element_by_tag_name("button")
    # Click the sign in button
    signInButton.click()

    # delays for 3 seconds
    time.sleep(3)

    # Here is a list of all the buttons on the page
    AllButtonsOnReportPage = browser.find_elements_by_css_selector('.btn')
    numOfButtons = AllButtonsOnReportPage.__len__()

    dailyReportButton = AllButtonsOnReportPage[5]

    # Click to set to daily report button
    dailyReportButton.click()
    dailyReportButton.send_keys(Keys.ARROW_DOWN)

    # Find dropdown menu for daily report and click it
    dailyReportDropDownList = browser.find_elements_by_class_name('dropdown-menu')
    dailyReportDropDownList[3].click()

    # Find the date tab and click on it
    customDateRangeTab = browser.find_element_by_tag_name('lkqd-date-range')
    customDateRangeTab.click()

    # Get the current Date
    currentDate = time.strftime("%m/%d/%Y")
    date_1 = datetime.strptime(currentDate, "%m/%d/%Y")

    # Move the current date back two days
    end_date = date_1 - timedelta(days=2)
    end_date = end_date.strftime('%m/%d/%Y')

    # Enter the date in the data field for start date and end data
    time.sleep(2)
    customDateRangeStart = browser.find_element_by_name('daterangepicker_start')
    customDateRangeStart.clear()
    customDateRangeStart.send_keys(end_date)

    customDateRangeEnd = browser.find_element_by_name('daterangepicker_end')
    customDateRangeEnd.clear()
    customDateRangeEnd.send_keys(end_date)


    # Hit the apply button
    applyButton = browser.find_element_by_class_name('applyBtn')
    applyButton.click()

    # Run the report
    runReportButton = AllButtonsOnReportPage[14]
    runReportButton.click()
    table = browser.find_element_by_xpath('//*[@id="reports"]/div/div[4]/div/div/div[1]/table')

    tableOfData = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[1]")
    pickle = browser.find_elements_by_xpath('//*[@id="reports"]/div/div[4]/div/div/div[1]/table/tbody/tr[2]/td[2]/div')
    time.sleep(5)

    table_text = tableOfData.text

    table_text_list = str(table_text).split(" ")

    html_source = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html_source, "html.parser")

    list_of_toboolas = soup.find_all("div","name-cell")

    # List of all the impressions on the page and how many there are
    impressions_list = soup.find_all("td","reporting-td-value-sized ")
    impressions_list = impressions_list[0::10]
    impressions_list.pop(0) # Remove the first element, which is the total
    numOfImpressions = impressions_list.__len__() - 1

    # Table with x columns and numOfImpressions number of rows

    # Gets all the rows in the table
    rows_List_strings = []
    rows = soup.findAll('table')[0].findAll('tr')

    # Makes a list of all the revenues, impressions and taboola and put them into a 2d list
    x = 0
    i = 2

    final_revenue_list = []
    final_revenue_list.append([])

    final_impressions_list = []
    final_impressions_list.append([])

    final_taboolas_list = []
    final_taboolas_list.append([])


    while(x < numOfImpressions):
        try:
            stringRow = str(rows[i].text)
        except Exception:
            break

        # Parse the row and get the revenue number
        split_string_by_rows = stringRow.split("$",5)

        revenue = split_string_by_rows[3]
        revenue_final = revenue[:4]


        # Checks to see if the first part of the string is a '0'
        first_digit_rev = revenue[:1]
        int_rev_final = "-1"

        # If it is convert just the first digit to a 0
        if(first_digit_rev is "0"):
            int_rev_final = first_digit_rev
            # Otherwise
        else:
            int_rev_final = revenue_final

        final_revenue_list[0].append(int_rev_final)
        final_impressions_list[0].append(impressions_list[x].text)
        final_taboolas_list[0].append(list_of_toboolas[x].text)
        i += 1
        x += 1

    # Create 2d table of values
    final_list = list(map(list, zip(final_impressions_list, final_revenue_list)))
    final_list = final_list[0]

    # Make a method of this, given a 2-D list make into spread sheet
    # Create and Write info to an CSV file
    location_of_file = "/Users/noah.p/Desktop/TestFolder/"
    num = 0
    while(num < len(list_of_toboolas)):
        current_taboola = list_of_toboolas[num].text.replace(" ","")
        if(current_taboola == "Taboola MW MX IOS $1 floor".replace(" ","")):
            final_taboola = "SelectMedia_MW_MX-IOS_$1_floor"

        elif(current_taboola == "Taboola MW JP IOS $2  floor".replace(" ","")):
            final_taboola = "SelectMedia_MW_JP-IOS_$2_floor"

        elif(current_taboola == "Taboola MW AUS Android $2 floor".replace(" ","")):
            final_taboola = "SelectMedia_MW_AUS_Android_$2_floor"

        elif(current_taboola == "Taboola MW SG Android $2  floor".replace(" ","")):
            final_taboola = "SelectMedia_MW_SG-Android_$2_floor"

        elif(current_taboola == "Taboola MW SG IOS $2  floor".replace(" ","")):
            final_taboola = "SelectMedia_MW_SG-IOS_$2_floor"

        elif(current_taboola == "Taboola MW MX Android $1 floor".replace(" ","")):
            final_taboola = "SelectMedia_MW_MX-Android_$1_floor"

        elif(current_taboola == "Taboola MW HK IOS  $1 floor".replace(" ","")):
            final_taboola = "SelectMedia_MW_HK-IOS_$1_floor"

        elif(current_taboola == "Taboola MW BR IOS $0.5 floor".replace(" ","")):
            final_taboola = "SelectMedia_MW_BR-IOS_$0.5_floor"

        elif (current_taboola == "Taboola MW BR IOS $1 floor".replace(" ", "")):
            final_taboola = "SelectMedia_MW_BR-IOS_$1_floor"
        else:
            final_taboola = "SelectMedia_MW_HK-Android_$1_floor"

        date_post = datetime.now() - timedelta(days=2)
        date_post = date_post.strftime(("%B %d, %Y"))
        # TODO: Make this a method
        with open(location_of_file + final_taboola + "_" + date_post + ".csv", "w") as csv_file:
            fileWriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            fileWriter.writerow(["Date", "Impressions", "Revenue"])
            fileWriter.writerow([end_date, final_list[0][0], final_list[1][0]])

        num += 1
    print("Finished!")
