import time
import PulsePointReport
import SpringServeReport
import Optimatic_Platfrom
import LKQD_Platform
import ThriveDailyReport
import IronSourceReport

class Main:
    pp = 0
    ss = 0
    op = 0
    lk = 0
    th = 0
    ir = 0

    start_time_total = time.time()

    print("Running Pulse point")
    result = 0
    while result is 0 and pp < 3:
        try:
            # Try pulse point 3 times before giving up
            PulsePointReport.main()
            result = 1
        except:
            pp += 1
            if pp is 3:
                print("ERROR: Pulse point did not run")
            else:
                pass
    print("----------------------")

    print("Running Spring Serve")
    result = 0
    while result is 0 and ss < 3:
        try:
            # Try pulse point 3 times before giving up
            SpringServeReport.main()
            result = 1
        except:
            ss += 1
            if ss is 3:
                print("ERROR: Spring Serve did not run")
            else:
                pass
    print("----------------------")

    print("Running Optimatic")
    result = 0
    while result is 0 and op < 3:
        try:
            # Try 3 times before giving up
            Optimatic_Platfrom.main()
            result = 1
        except:
            op += 1
            if op is 3:
                print("ERROR: Optimatic did not run")
            else:
                pass
    print("----------------------")

    print("Running LKQD")
    result = 0
    while result is 0 and lk < 3:
        try:
            # Try 3 times before giving up
            LKQD_Platform.main()
            result = 1
        except:
            lk += 1
            pass
            if lk is 3:
                print("ERROR: LKQD did not run")

    print("----------------------")

    print("Running Thrive")
    result = 0
    while result is 0 and th < 3:
        try:
            # Try 3 times before giving up
            ThriveDailyReport.main()
            result = 1
        except:
            th += 1
            pass
            if th is 3:
                print("ERROR: Thrive did not run")
    print("----------------------")

    print("Running Iron source")
    result = 0
    while result is 0 and ir < 3:
        try:
            # Try 3 times before giving up
            IronSourceReport.main()
            result = 1
        except:
            ir += 1
            pass
            if ir is 3:
                print("ERROR: Thrive did not run")

    print("やった！！！")

    print("This program took --- %s seconds ---" % (time.time() - start_time_total))
