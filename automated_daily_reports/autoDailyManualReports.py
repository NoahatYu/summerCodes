import time
from sendEmail import main
import PulsePointReport
import SpringServeReport
import Optimatic_Platfrom
import LKQD_Platform
import ThriveDailyReport
import IronSourceReport

class AutoDailyManualReports:
    """
    MAIN class for  autoDailyManualReports
    """
    pp = 0
    ss = 0
    op = 0
    lk = 0
    th = 0
    ir = 0

    start_time_total = time.time()

    start_time_pp = time.time()
    print("Running PulsePoint")
    result = 0
    while result is 0 and pp < 3:
        try:
            # Try pulse point 3 times before giving up
            PulsePointReport.main()
            result = 1
        except:
            pp += 1
            if pp is 3:
                print("ERROR: PulsePoint did not run")
            else:
                pass
    print("DONE")
    print("PulsePoint program took --- %s seconds ---" % (time.time() - start_time_pp))
    print("----------------------")

    start_time_ss = time.time()
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
    print("DONE")
    print("SpringServe program took --- %s seconds ---" % (time.time() - start_time_ss))
    print("----------------------")

    start_time_op = time.time()
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
    print("DONE")
    print("Optimatic program took --- %s seconds ---" % (time.time() - start_time_op))
    print("----------------------")

    start_time_elka = time.time()
    print("Running LKQD")
    result = 0
    while result is 0 and lk < 3:
        try:
            # Try 3 times before giving up
            LKQD_Platform.main()
            result = 1
        except:
            lk += 1
            if lk is 3:
                print("ERROR: LKQD did not run")
            else:
                pass
    print("DONE")
    print("LKQD program took --- %s seconds ---" % (time.time() - start_time_elka))

    print("----------------------")
    start_time_tr = time.time()
    print("Running Thrive")
    result = 0
    while result is 0 and th < 3:
        try:
            # Try 3 times before giving up
            ThriveDailyReport.main()
            result = 1
        except:
            th += 1
            if th is 3:
                print("ERROR: Thrive did not run")
            else:
                pass

    print("Thrive program took --- %s seconds ---" % (time.time() - start_time_tr))
    print("----------------------")

    start_time_ir = time.time()
    print("Running Iron source")
    result = 0
    while result is 0 and ir < 3:
        try:
            # Try 3 times before giving up
            IronSourceReport.main()
            result = 1
        except:
            ir += 1
            if ir is 3:
                print("ERROR: IronSource did not run")
    print("IronSource program took --- %s seconds ---" % (time.time() - start_time_ir))

    print("Sending Emails...")
    #sendEmail's main method
    main()
    print("Done")
    print("やった！！！")

    print("The Daily Manual Reports program took --- %s seconds ---" % (time.time() - start_time_total))
