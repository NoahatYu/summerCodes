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
import PubmaticReports

"""
Author - Noah Potash 07/15/2017
"""

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
    pb = 0
    start_time_total = time()

    logFile = "/Users/noah.p/PycharmProjects/autoReports/DailyReportsLog/AutoDailyManualReportslogs.log/"
    logName = "Auto"
    logging.basicConfig(filename=logFile, level=logging.INFO)
    logger = logging.getLogger(logName)


    def __init__(self, pp, ss, op, lk, th, ir, sk, pb,start_time_total,logFile, logName, logger):
        """
        Constructor for class
        :param pp:
        :param ss:
        :param op:
        :param lk:
        :param th:
        :param ir:
        :param sk:
        :param pb:
        """
        self.pp = pp
        self.ss = ss
        self.op = op
        self.lk = lk
        self.th = th
        self.ir = ir
        self.sk = sk
        self.pb = pb
        self.start_time_total = start_time_total
        self.logFile = logFile
        self.logName = logName
        self.logger = logger



    def runPulsePointReport(self,pp,logger):
        """
        Run the pulse point report
        :param pp:
        :param logger:
        :return:
        """
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

    def runSpringServeReport(self,ss,logger):
        """
        Run the spring serve report
        :param ss:
        :param logger:
        :return:
        """
        start_time_ss = time()
        print("Running SpringServe")
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

    def runOptimaticReport(self, op, logger):
        """
        Run the optimatic report
        :param op:
        :param logger:
        :return:
        """
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

    def runLKQDReport(self, lk, logger):
        """
        Run the LKQD report
        :param lk:
        :param logger:
        :return:
        """
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

    def runThriveReport(self, th, logger):
        """
        Run the thrive report
        :param th:
        :param logger:
        :return:
        """
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

    def runIronSourceReport(self, ir, logger):
        """
        Run the iron source report
        :param ir:
        :param logger:
        :return:
        """
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
        print("----------------------")

    def runSekindoDailyReport(self, sk, logger):
        """
        Runs the sekindo reports
        :param sk:
        :param logger:
        :return:
        """
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
        logger.info("Sekindo program took --- %s seconds ---" % (time() - start_time_sk))
        print("Sekindo program took --- %s seconds ---" % (time() - start_time_sk))
        print("----------------------")

    def runPubmaticReports(self, pb, logger):
        """
        Runs the pubmatic reports
        :param pb:
        :param logger:
        :return:
        """
        start_time_pb = time()
        print("Running Pubmatic")
        result = 0
        while result is 0 and pb < 3:
            try:
                # Try 3 times before giving up
                PubmaticReports.main()
                result = 1
            except:
                pb += 1
                if pb is 3:
                    logger.error("Pubmatic did not run")
                    print("ERROR: Pubmatic did not run")
        logger.info("Pubmatic program took --- %s seconds ---" % (time() - start_time_pb))
        print("Pubmatic program took --- %s seconds ---" % (time() - start_time_pb))
        print("-----------------")

    def sendAllEmails(self):
        """
        Sends emails from a specific folder
        :return:
        """
        print("Sending Emails...")
        #sendEmail's main method
        main()
        print("Done")

def main():
    """
    Main Method
    :return:
    """
    autoR = AutoDailyManualReports(AutoDailyManualReports.pp,AutoDailyManualReports.ss,AutoDailyManualReports.op,
                                AutoDailyManualReports.lk,AutoDailyManualReports.th,AutoDailyManualReports.ir,
                                AutoDailyManualReports.sk, AutoDailyManualReports.pb,AutoDailyManualReports.start_time_total,
                                AutoDailyManualReports.logFile,AutoDailyManualReports.logName,AutoDailyManualReports.logger)

    autoR.runPulsePointReport(autoR.pp, autoR.logger)
    autoR.runSpringServeReport(autoR.ss, autoR.logger)
    autoR.runOptimaticReport(autoR.op, autoR.logger)
    autoR.runLKQDReport(autoR.lk, autoR.logger)
    autoR.runThriveReport(autoR.th, autoR.logger)
    autoR.runIronSourceReport(autoR.ir, autoR.logger)
    autoR.runSekindoDailyReport(autoR.sk, autoR.logger)
    autoR.runPubmaticReports(autoR.pb, autoR.logger)
    autoR.sendAllEmails()

    autoR.logger.info("The Daily Manual Reports program took --- %s seconds ---" % (time() - autoR.start_time_total))
    print("The Daily Manual Reports program took --- %s seconds ---" % (time() - autoR.start_time_total))

if __name__ == "__main__":
    main()
