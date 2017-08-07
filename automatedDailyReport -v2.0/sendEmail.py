import sys
import os
import smtplib
from datetime import datetime
from datetime import timedelta
from email import encoders
from datetime import timedelta
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

"""
Author - Noah Potash 07/15/2017
"""

class sendEmails:

    date_post = datetime.now() - timedelta(days=2)
    date_post = date_post.strftime(("%B %d, %Y"))
    date_post = date_post.replace(" ","_")


    taboola_dict = {

        "Pulse_Point_Direct_Desktop_BTU_Standard_5": "Pulse Point::Direct::Desktop::BTU::Standard::5_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_6": "Pulse Point::Direct::Desktop::BTU::Standard::6_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_7": "Pulse Point::Direct::Desktop::BTU::Standard::7_DemandExtreme",
        "Taboola_MX_$1_Floor": "SelectMedia::Direct::Desktop::MX-1_DemandExtreme",
        "Taboola_AUS_$2.5_Floor": "SelectMedia::Direct::Desktop::AUS-2.5_DemandExtreme",
        "Taboola_BR_$1_Floor": "SelectMedia::Direct::Desktop::BR-1_DemandExtreme",
        "Taboola-JS-AUS_$2.5_Floor": "SelectMedia::Direct::Desktop::AUS-2.5::JS_DemandExtreme",
        "Taboola_Anglo_+FR_+DE_SP_$4_Floor": "SelectMedia::Direct::Desktop::FR-DE-SmallPlayer-4_DemandExtreme",
        "Taboola-JS-Anglo_+FR_+DE_SP_$4_Floor": "SelectMedia::Direct::Desktop::FR-DE-SmallPlayer-4::JS_DemandExtreme",
        "Taboola_APAC_HK": "SelectMedia::Direct::Desktop::HK_DemandExtreme",
        "Taboola_APAC_ID": "SelectMedia::Direct::Desktop::ID_DemandExtreme",
        "Taboola_APAC_JP": "SelectMedia::Direct::Desktop::JP_DemandExtreme",
        "Taboola_APAC_MY": "SelectMedia::Direct::Desktop::MY_DemandExtreme",
        "Taboola_APAC_MY_$3_floor": "SelectMedia::Direct::Desktop::MY-3_DemandExtreme",
        "Taboola_APAC_PH": "SelectMedia::Direct::Desktop::PH_DemandExtreme",
        "Taboola_APAC_SG": "SelectMedia::Direct::Desktop::SG_DemandExtreme",
        "Taboola_APAC_SG_$3.5_floor": "SelectMedia::Direct::Desktop::SG-3.5_DemandExtreme",
        "Taboola_APAC_TH": "SelectMedia::Direct::Desktop::TH_DemandExtreme",
        "SelectMedia_MW_AUS_Android_$2_floor": "SelectMedia::Direct::Mobile::AUS-Android-2_DemandExtreme",
        "SelectMedia_MW_BR-IOS_$0.5_floor": "SelectMedia::Direct::Mobile::BR-IOS-0.5_DemandExtreme",
        "SelectMedia_MW_BR-IOS_$1_floor": "SelectMedia::Direct::Mobile::BR-IOS-1_DemandExtreme",
        "SelectMedia_MW_HK-Android_$1_floor": "SelectMedia::Direct::Mobile::HK-Android-1_DemandExtreme",
        "SelectMedia_MW_HK-IOS_$1_floor": "SelectMedia::Direct::Mobile::HK-IOS-1_DemandExtreme",
        "SelectMedia_MW_JP-IOS_$2_floor": "SelectMedia::Direct::Mobile::JP-IOS-2_DemandExtreme",
        "SelectMedia_MW_MX-Android_$1_floor": "SelectMedia::Direct::Mobile::MX-Android-1_DemandExtreme",
        "SelectMedia_MW_MX-IOS_$1_floor": "SelectMedia::Direct::Mobile::MX-IOS-1_DemandExtreme",
        "SelectMedia_MW_SG-Android_$2_floor": "SelectMedia::Direct::Mobile::SG-Android-2_DemandExtreme",
        "SelectMedia_MW_SG-IOS_$2_floor": "SelectMedia::Direct::Mobile::SG-IOS-2_DemandExtreme",
        "Thrive_Mobile_2": "Thrive::Direct::Mobile::2_DemandExtreme",
        "Thrive_Direct_Desktop_5": "Thrive::Direct::Desktop::5_DemandExtreme",
        "Thrive_Direct_Mobile_2_LKQD": "Thrive::Direct::Mobile::2::LKQD_DemandExtreme",
        "Thrive_Direct_US_UK_MW_3.5_LKQD": "Thrive::Direct::US::UK::MW::3.5::LKQD_DemandExtreme",
        "IronSource_Direct_Desktop_US-5.5": "IronSource::Direct::Desktop::US-5.5_DemandExtreme",
        "IronSource_Direct_Desktop_US-6.5": "IronSource::Direct::Desktop::US-6.5_DemandExtreme",
        "IronSource_Direct_Desktop_US-7.5": "IronSource::Direct::Desktop::US-7.5_DemandExtreme",
        "Sekindo_Direct_Desktop_US_LP": "Sekindo::Direct::Desktop::US::LP_DemandExtreme",
        "Sekindo_Direct_Desktop_US_LP_Jscript": "Sekindo::Direct::Desktop::US::LP::Jscript_DemandExtreme",
        "Sekindo_Direct_DT_BRMX_LP_JS": "Sekindo::Direct::DT::BRMX::LP::JS_DemandExtreme",
        "Sekindo_Direct_Tier1_LP_JS": "Sekindo::Direct::Tier1::LP::JS _DemandExtreme",
        "Pubmatic_Direct_Desktop_LP_9": "Pubmatic::Direct::Desktop::LP::9_DemandExtreme",
        "Pubmatic_Direct_Desktop_MP_7": "Pubmatic::Direct::Desktop::MP::7_DemandExtreme",
        "Pubmatic_Direct_Desktop_Secured_6": "Pubmatic::Direct::Desktop::Secured::6_DemandExtreme",
        "Pubmatic_Direct_Desktop_SP_5": "Pubmatic::Direct::Desktop::SP::5_DemandExtreme",
        "Pubmatic_Direct_MW_LP_6": "Pubmatic::Direct::MW::LP::6_DemandExtreme",
        "Pubmatic_Direct_MW_LP_7": "Pubmatic::Direct::MW::LP::7_DemandExtreme",
        "Pubmatic_Direct_MW_LP_8": "Pubmatic::Direct::MW::LP::8_DemandExtreme",
        "Pubmatic_Direct_MW_MP_5": "Pubmatic::Direct::MW::MP::5_DemandExtreme",
        "Pubmatic_Direct_MW_SP_3": "Pubmatic::Direct::MW::SP::3_DemandExtreme",
        "Pubmatic_Direct_MW_Secured_5": "Pubmatic::Direct::MW::Secured::5_DemandExtreme",
        "Optimatic_ML_US_VPAID_DT_RS": "Optimatic::ML::US::VPAID::DT::RS_DemandExtreme",
        "Appthis_Direct_Desktop_4.5": "Appthis::Direct::Desktop::4.5_DemandExtreme"

    }


    def __init__(self,taboola_dict):
        """
        Constructor
        :param taboola_dict:
        """
        self.taboola_dict = taboola_dict

    def sendEmail(self,taboola_dict):
        """
        Send email with all the correct values
        :param taboola_dict:
        :return:
        """

        COMMASPACE = ', '
        sendDirectory = os.listdir("/Users/noah.p/Desktop/DailyReports")
        # Delete .ds store on mac
        del sendDirectory[0]
        lengthOfPP = len(sendDirectory)


        i = 1
        for fileToSend in sendDirectory:

            fileWithCSV = fileToSend
            # Remove the .csv from the file name in order to find it in the dictionary
            fileToSend = fileToSend.replace(".csv","")
            fileWithoutdate = fileToSend.split("|")
            fileWithoutdate = fileWithoutdate[0]

            sender = ''
            gmail_password = ''
            recipients = [""]  # EMAIL ADDRESSES HERE SEPARATED BY COMMAS - #
            # Create the enclosing (outer) message
            outer = MIMEMultipart()
            outer['To'] = COMMASPACE.join(recipients)
            outer['From'] = sender

            outer['Subject'] = taboola_dict[fileWithoutdate]# EMAIL SUBJECT

            outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

            # List of attachment
            attachment = "/Users/noah.p/Desktop/DailyReports/" + fileWithCSV # FULL PATH TO ATTACHMENTS HERE

            # Add the attachment to the message

            try:
                with open(attachment, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                    encoders.encode_base64(msg)
                    msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
                    outer.attach(msg)
            except:
                print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise

            composed = outer.as_string()

            # Send the email
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as s:
                    s.ehlo()
                    s.starttls()
                    s.ehlo()
                    s.login(sender, gmail_password)
                    s.sendmail(sender, recipients, composed)
                    s.close()
                    print("Email sent! " + str(i))
            except:
                print("Unable to send the email. Error: ", sys.exc_info()[0])
                raise
            i += 1
def main():
    """
    Main method
    :return:
    """
    autoE = sendEmails(sendEmails.taboola_dict)
    autoE.sendEmail(autoE.taboola_dict)
    print("DONE!")

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
