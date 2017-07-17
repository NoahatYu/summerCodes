import sys
import os
import smtplib
from datetime import datetime
from datetime import timedelta
#import PulsePointReport
from email import encoders
from datetime import timedelta
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class sendEmails:

    date_post = datetime.now() - timedelta(days=2)
    date_post = date_post.strftime(("%B %d, %Y"))
    date_post = date_post.replace(" ","_")


    taboola_dict = {

        "IronSource_Direct_Desktop_US-5.5": "IronSource_Direct_Desktop_US-5.5_DemandExtreme",
        "IronSource_Direct_Desktop_US-6.5": "IronSource_Direct_Desktop_US-6.5_DemandExtreme",
        "IronSource_Direct_Desktop_US-7.5": "IronSource_Direct_Desktop_US-7.5_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_5": "Pulse_Point_Direct_Desktop_BTU_Standard_5_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_6": "Pulse_Point_Direct_Desktop_BTU_Standard_6_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_7": "Pulse_Point_Direct_Desktop_BTU_Standard_7_DemandExtreme",
        "Taboola_MX_$1_Floor": "SelectMedia_Direct_Desktop_MX-1_DemandExtreme",
        "Taboola_AUS_$2.5_Floor": "SelectMedia_Direct_Desktop_AUS-2.5_DemandExtreme",
        "Taboola_BR_$1_Floor": "SelectMedia_Direct_Desktop_BR-1_DemandExtreme",
        "Taboola-JS-AUS_$2.5_Floor": "SelectMedia_Direct_Desktop_AUS-2.5_JS_DemandExtreme",
        "Taboola_Anglo_+FR_+DE_SP_$4_Floor": "SelectMedia_Direct_Desktop_FR-DE-SmallPlayer-4_DemandExtreme",
        "Taboola-JS-Anglo_+FR_+DE_SP_$4_Floor": "SelectMedia_Direct_Desktop_FR-DE-SmallPlayer-4_JS_DemandExtreme",
        "Taboola_APAC_HK": "SelectMedia_Direct_Desktop_HK_DemandExtreme",
        "Taboola_APAC_JP": "SelectMedia_Direct_Desktop_JP_DemandExtreme",
        "Taboola_APAC_MY": "SelectMedia_Direct_Desktop_MY_DemandExtreme",
        "Taboola_APAC_MY_$3_floor": "SelectMedia_Direct_Desktop_MY-3_DemandExtreme",
        "Taboola_APAC_PH": "SelectMedia_Direct_Desktop_PH_DemandExtreme",
        "Taboola_APAC_SG": "SelectMedia_Direct_Desktop_SG_DemandExtreme",
        "Taboola_APAC_SG_$3.5_floor": "SelectMedia_Direct_Desktop_SG-3.5_DemandExtreme",
        "Taboola_APAC_TH": "SelectMedia_Direct_Desktop_TH_DemandExtreme",
        "SelectMedia_MW_AUS_Android_$2_floor": "SelectMedia_Direct_Mobile_AUS-Android-2_DemandExtreme",
        "SelectMedia_MW_BR-IOS_$0.5_floor": "SelectMedia_Direct_Mobile_BR-IOS-0.5_DemandExtreme",
        "SelectMedia_MW_BR-IOS_$1_floor": "SelectMedia_Direct_Mobile_BR-IOS-1_DemandExtreme",
        "SelectMedia_MW_HK-Android_$1_floor": "SelectMedia_Direct_Mobile_HK-Android-1_DemandExtreme",
        "SelectMedia_MW_HK-IOS_$1_floor": "SelectMedia_Direct_Mobile_HK-IOS-1_DemandExtreme",
        "SelectMedia_MW_JP-IOS_$2_floor": "SelectMedia_Direct_Mobile_JP-IOS-2_DemandExtreme",
        "SelectMedia_MW_MX-Android_$1_floor": "SelectMedia_Direct_Mobile_MX-Android-1_DemandExtreme",
        "SelectMedia_MW_MX-IOS_$1_floor": "SelectMedia_Direct_Mobile_MX-IOS-1_DemandExtreme",
        "SelectMedia_MW_SG-Android_$2_floor": "SelectMedia_Direct_Mobile_SG-Android-2_DemandExtreme",
        "SelectMedia_MW_SG-IOS_$2_floor": "SelectMedia_Direct_Mobile_SG-IOS-2_DemandExtreme",
        "Thrive_Mobile_2": "Thrive_Direct_Mobile_2_DemandExtreme",
        "Thrive_Direct_Desktop_5": "Thrive_Direct_Desktop_5_DemandExtreme"

    }


    def __init__(self,taboola_dict):
        """
        Constructor
        :param taboola_dict:
        """
        self.taboola_dict = taboola_dict

    def sendEmail(self,taboola_dict):

        COMMASPACE = ', '
        sendDirectory = os.listdir("/Users/noah.p/Desktop/EmailTestFolder")
        # Delete .ds store on mac
        del sendDirectory[0]
        lengthOfPP = len(sendDirectory)


        i = 0
        for fileToSend in sendDirectory:

            fileWithCSV = fileToSend
            # Remove the .csv from the file name in order to find it in the dictionary
            fileToSend = fileToSend.replace(".csv","")
            fileWithoutdate = fileToSend.split("|")
            fileWithoutdate = fileWithoutdate[0]

            sender = 'noah.p@taboola.com'  # from_address = "noah.p@taboola.com"
            gmail_password = 'whviduonpebrdxnl'  # whviduonpebrdxnl
            recipients = ["cm-autoreportdex@taboola.com"]  # cm-autoreportdex@taboola.com EMAIL ADDRESSES HERE SEPARATED BY COMMAS - # to_address = "daniel.t@taboola.com"
            # Create the enclosing (outer) message
            outer = MIMEMultipart()
            outer['To'] = COMMASPACE.join(recipients)
            outer['From'] = sender

            outer['Subject'] = taboola_dict[fileWithoutdate]# EMAIL SUBJECT

            outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

            # List of attachment
            attachment = "/Users/noah.p/Desktop/EmailTestFolder/" + fileWithCSV # FULL PATH TO ATTACHMENTS HERE

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
