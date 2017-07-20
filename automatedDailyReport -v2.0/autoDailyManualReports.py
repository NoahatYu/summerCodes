import logging
import time
from time import time
from sendEmail import main
import PulsePointReport
import SpringServeReport
import Optimatic_Platfrom
import LKQD_Platform
import ThriveDailyReport
import IronSourceReport
import SekindoDailyReport

class AutoDailyManualReports:
    """
    MAIN class for the Auto Daily Manual Reports
    Each script is called and will try 3 times to run. if it still doesnt run after that it will move on
    to the next one.
    """
    pp = 0
    ss = 0
    op = 0
    lk = 0
    th = 0
    ir = 0
    sk = 0

    start_time_total = time()
    logFile = "/Users/noah.p/PycharmProjects/autoReports/DailyReportsLog/AutoDailyManualReportslogs.log/"
    logName = "Auto"
    logging.basicConfig(filename=logFile, level=logging.INFO)
    logger = logging.getLogger(logName)

    start_time_pp = time()
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
                logger.error("PulsePont did not run")
            else:
                pass
    print("DONE")
    logger.info("PulsePoint program took --- %s seconds ---" % (time() - start_time_pp))
    print("PulsePoint program took --- %s seconds ---" % (time() - start_time_pp))
    print("----------------------")

    start_time_ss = time()
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
                logger.error("SpringServe did not run")
                print("ERROR: Spring Serve did not run")
            else:
                pass
    print("DONE")
    logger.info("SpringServe program took --- %s seconds ---" % (time() - start_time_ss))
    print("SpringServe program took --- %s seconds ---" % (time() - start_time_ss))
    print("----------------------")

    start_time_op = time()
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
                logger.error("Optimatic did not run")
                print("ERROR: Optimatic did not run")
            else:
                pass
    print("DONE")
    logger.info("Optimatic program took --- %s seconds ---" % (time() - start_time_op))
    print("Optimatic program took --- %s seconds ---" % (time() - start_time_op))
    print("----------------------")

    start_time_elka = time()
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
                logger.error("LKQD did not run")
                print("ERROR: LKQD did not run")
            else:
                pass
    print("DONE")
    logger.info("LKQD program took --- %s seconds ---" % (time() - start_time_elka))
    print("LKQD program took --- %s seconds ---" % (time() - start_time_elka))

    print("----------------------")
    start_time_tr = time()
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
                logger.error("Thive did not run")
                print("ERROR: Thrive did not run")
            else:
                pass
    logger.info("Thrive program took --- %s seconds ---" % (time() - start_time_tr))
    print("Thrive program took --- %s seconds ---" % (time() - start_time_tr))
    print("----------------------")

    start_time_ir = time()
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
                logger.error("IronSource did not run")
                print("ERROR: IronSource did not run")
    logger.info("IronSource program took --- %s seconds ---" % (time() - start_time_ir))
    print("IronSource program took --- %s seconds ---" % (time() - start_time_ir))


    start_time_sk = time()
    print("Running Sekindo")
    result = 0
    while result is 0 and sk < 3:
        try:
            # Try 3 times before giving up
            SekindoDailyReport.main()
            result = 1
        except:
            sk += 1
            if sk is 3:
                logger.error("Sekindo did not run")
                print("ERROR: Sekindo did not run")
    logger.info("Sekindo program took --- %s seconds ---" % (time() - start_time_ir))
    print("Sekindo program took --- %s seconds ---" % (time() - start_time_ir))

    print("Sending Emails...")
    #sendEmail's main method
    main()
    print("Done")
    logger.info("The Daily Manual Reports program took --- %s seconds ---" % (time() - start_time_total))
    print("The Daily Manual Reports program took --- %s seconds ---" % (time() - start_time_total))
