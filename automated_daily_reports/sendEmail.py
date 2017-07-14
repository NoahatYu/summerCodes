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


    taboola_Dict = {
        "IronSource_Direct_Desktop_US-5.5|" + date_post: "IronSource_Direct_Desktop_US-5.5_DemandExtreme",
        "IronSource_Direct_Desktop_US-6.5|" + date_post: "IronSource_Direct_Desktop_US-6.5_DemandExtreme",
        "IronSource_Direct_Desktop_US-7.5|" + date_post: "IronSource_Direct_Desktop_US-7.5_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_5|" + date_post: "Pulse_Point_Direct_Desktop_BTU_Standard_5_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_6|" + date_post: "Pulse_Point_Direct_Desktop_BTU_Standard_6_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_7|" + date_post: "Pulse_Point_Direct_Desktop_BTU_Standard_7_DemandExtreme",
        "Taboola_MX_$1_Floor|" + date_post: "SelectMedia_Direct_Desktop_MX-1_DemandExtreme",
        "Taboola_AUS_$2.5_Floor|" + date_post: "SelectMedia_Direct_Desktop_AUS-2.5_DemandExtreme",
        "Taboola_BR_$1_Floor|" + date_post: "SelectMedia_Direct_Desktop_BR-1_DemandExtreme",
        "Taboola-JS-AUS_$2.5_Floor|" + date_post: "SelectMedia_Direct_Desktop_AUS-2.5_JS",
        "Taboola_Anglo_+FR_+DE_SP_$4_Floor|" + date_post: "SelectMedia_Direct_Desktop_FR-DE-SmallPlayer-4_DemandExtreme",
        "Taboola-JS-_Anglo_+FR_+DE_SP_$4_Floor|" + date_post: "SelectMedia_Direct_Desktop_FR-DE-SmallPlayer-4_JS_DemandExtreme",
        "Taboola APAC HK|" + date_post: "SelectMedia_Direct_Desktop_HK_DemandExtreme",
        "Taboola APAC JP|" + date_post: "SelectMedia_Direct_Desktop_JP_DemandExtreme",
        "Taboola APAC MY|" + date_post: "SelectMedia_Direct_Desktop_MY_DemandExtreme",
        "Taboola APAC MY $3 floor|" + date_post: "SelectMedia_Direct_Desktop_MY-3_DemandExtreme",
        "Taboola APAC PH|" + date_post: "SelectMedia_Direct_Desktop_PH_DemandExtreme",
        "Taboola APAC SG|" + date_post: "SelectMedia_Direct_Desktop_SG_DemandExtreme",
        "Taboola APAC SG $3.5 floor|" + date_post: "SelectMedia_Direct_Desktop_SG-3.5_DemandExtreme",
        "Taboola APAC TH|" + date_post: "SelectMedia_Direct_Desktop_TH_DemandExtreme",
        "SelectMedia_MW_AUS_Android_$2_floor|" + date_post: "SelectMedia_Direct_Mobile_AUS-Android-2_DemandExtreme",
        "SelectMedia_MW_BR-IOS_$0.5_floor|" + date_post: "SelectMedia_Direct_Mobile_BR-IOS-0.5_DemandExtreme",
        "SelectMedia_MW_BR-IOS_$1_floor|" + date_post: "SelectMedia_Direct_Mobile_BR-IOS-1_DemandExtreme",
        "SelectMedia_MW_HK-Android_$1_floor|" + date_post: "SelectMedia_Direct_Mobile_HK-Android-1_DemandExtreme",
        "SelectMedia_MW_HK-IOS_$1_floor|" + date_post: "SelectMedia_Direct_Mobile_HK-IOS-1_DemandExtreme",
        "SelectMedia_MW_JP-IOS_$2_floor|" + date_post: "SelectMedia_Direct_Mobile_JP-IOS-2_DemandExtreme",
        "SelectMedia_MW_MX-Android_$1_floor|" + date_post: "SelectMedia_Direct_Mobile_MX-Android-1_DemandExtreme",
        "SelectMedia_MW_MX-IOS_$1_floor|" + date_post: "SelectMedia_Direct_Mobile_MX-IOS-1_DemandExtreme",
        "SelectMedia_MW_SG-Android_$2_floor|" + date_post: "SelectMedia_Direct_Mobile_SG-Android-2_DemandExtreme",
        "SelectMedia_MW_SG-IOS_$2_floor|" + date_post: "SelectMedia_Direct_Mobile_SG-IOS-2_DemandExtreme",
        "Thrive_Mobile_2|" + date_post: "Thrive_Direct_Mobile_2_DemandExtreme",
        "Thrive_Direct_Desktop_5|" + date_post: "Thrive_Direct_Desktop_5_DemandExtreme"

    }

    def sendEmail(self,taboola_Dict):

        COMMASPACE = ', '
        sendDirectory = os.listdir("/Users/noah.p/Desktop/TestFolder/TestFolder2")
        # Delete .ds store on mac
        del sendDirectory[0]
        lengthOfPP = len(sendDirectory)

        sender = 'noah.p@taboola.com'  # from_address = "noah.p@taboola.com"
        gmail_password = 'whviduonpebrdxnl'  # whviduonpebrdxnl
        recipients = ["noahpotash@gmail.com"]  # cm-autoreportdex@taboola.com EMAIL ADDRESSES HERE SEPARATED BY COMMAS - # to_address = "daniel.t@taboola.com"
        # Create the enclosing (outer) message
        outer = MIMEMultipart()
        outer['To'] = COMMASPACE.join(recipients)
        outer['From'] = sender

        i = 0
        for fileToSend in sendDirectory:
            fileWithCSV = fileToSend
            # Remove the .csv from the file name in order to find it in the dictionary
            fileToSend = fileToSend.replace(".csv","")

            outer['Subject'] = taboola_Dict[fileToSend] # EMAIL SUBJECT

            outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

            # List of attachment
            attachment = "/Users/noah.p/Desktop/TestFolder/TestFolder2/" + fileWithCSV # FULL PATH TO ATTACHMENTS HERE

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
                    print("Email sent!")
            except:
                print("Unable to send the email. Error: ", sys.exc_info()[0])
                raise
def main():
  sendEmails.sendEmail(sendEmails.taboola_Dict)

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()


"""


    PulsePoint_subject_dict = {
        "Pulse_Point_Direct_Desktop_BTU_Standard_5|" + date_post: "Pulse_Point_Direct_Desktop_BTU_Standard_5_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_6|" + date_post: "Pulse_Point_Direct_Desktop_BTU_Standard_6_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_7|" + date_post: "Pulse_Point_Direct_Desktop_BTU_Standard_7_DemandExtreme"
    }



    SpringServe_subject_dict = {
        "Taboola_MX_$1_Floor|" + date_post: "SelectMedia_Direct_Desktop_MX-1_DemandExtreme",
        "Taboola_AUS_$2.5_Floor|" + date_post: "SelectMedia_Direct_Desktop_AUS-2.5_DemandExtreme",
        "Taboola_BR_$1_Floor|" + date_post: "SelectMedia_Direct_Desktop_BR-1_DemandExtreme",
        "Taboola-JS-AUS_$2.5_Floor|" + date_post: "SelectMedia_Direct_Desktop_AUS-2.5_JS",
        "Taboola_Anglo_+FR_+DE_SP_$4_Floor|" + date_post: "SelectMedia_Direct_Desktop_FR-DE-SmallPlayer-4_DemandExtreme",
        "Taboola-JS-_Anglo_+FR_+DE_SP_$4_Floor|" + date_post: "SelectMedia_Direct_Desktop_FR-DE-SmallPlayer-4_JS_DemandExtreme"
    }

    Optimatic_subject_dict = {
        "Taboola APAC HK|" + date_post: "SelectMedia_Direct_Desktop_HK_DemandExtreme",
        "Taboola APAC JP|" + date_post: "SelectMedia_Direct_Desktop_JP_DemandExtreme",
        "Taboola APAC MY|" + date_post: "SelectMedia_Direct_Desktop_MY_DemandExtreme",
        "Taboola APAC MY $3 floor|" + date_post: "SelectMedia_Direct_Desktop_MY-3_DemandExtreme",
        "Taboola APAC PH|" + date_post: "SelectMedia_Direct_Desktop_PH_DemandExtreme",
        "Taboola APAC SG|" + date_post: "SelectMedia_Direct_Desktop_SG_DemandExtreme",
        "Taboola APAC SG $3.5 floor|" + date_post: "SelectMedia_Direct_Desktop_SG-3.5_DemandExtreme",
        "Taboola APAC TH|" + date_post: "SelectMedia_Direct_Desktop_TH_DemandExtreme"
        }

    LKQD_subject_dict = {
        "SelectMedia_MW_AUS_Android_$2_floor_" + date_post: "SelectMedia_Direct_Mobile_AUS-Android-2_DemandExtreme",
        "SelectMedia_MW_BR-IOS_$0.5_floor_" + date_post: "SelectMedia_Direct_Mobile_BR-IOS-0.5_DemandExtreme",
        "SelectMedia_MW_BR-IOS_$1_floor_" + date_post: "SelectMedia_Direct_Mobile_BR-IOS-1_DemandExtreme",
        "SelectMedia_MW_HK-Android_$1_floor_" + date_post: "SelectMedia_Direct_Mobile_HK-Android-1_DemandExtreme",
        "SelectMedia_MW_HK-IOS_$1_floor_" + date_post: "SelectMedia_Direct_Mobile_HK-IOS-1_DemandExtreme",
        "SelectMedia_MW_JP-IOS_$2_floor_" + date_post: "SelectMedia_Direct_Mobile_JP-IOS-2_DemandExtreme",
        "SelectMedia_MW_MX-Android_$1_floor_" + date_post: "SelectMedia_Direct_Mobile_MX-Android-1_DemandExtreme",
        "SelectMedia_MW_MX-IOS_$1_floor_" + date_post: "SelectMedia_Direct_Mobile_MX-IOS-1_DemandExtreme",
        "SelectMedia_MW_SG-Android_$2_floor_" + date_post: "SelectMedia_Direct_Mobile_SG-Android-2_DemandExtreme",
        "SelectMedia_MW_SG-IOS_$2_floor_" + date_post: "SelectMedia_Direct_Mobile_SG-IOS-2_DemandExtreme"
        }

    Thrive_subject_dict = {
        "Thrive_Mobile_2|" + date_post: "Thrive_Direct_Mobile_2_DemandExtreme",
        "Thrive_Direct_Desktop_5|" + date_post: "Thrive_Direct_Desktop_5_DemandExtreme"
    }

    IronSource_subject_dict = {
        "IronSource_Direct_Desktop_US-5.5|" + date_post: "IronSource_Direct_Desktop_US-5.5_DemandExtreme",
        "IronSource_Direct_Desktop_US-6.5|" + date_post: "IronSource_Direct_Desktop_US-6.5_DemandExtreme",
        "IronSource_Direct_Desktop_US-7.5|" + date_post: "IronSource_Direct_Desktop_US-7.5_DemandExtreme",
    }







"""
