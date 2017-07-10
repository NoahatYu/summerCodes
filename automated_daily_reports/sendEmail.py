import sys
import smtplib
import datetime
from email import encoders
from datetime import timedelta
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
class sendEmails:
    
    PulsePoint_dict = {
        "Pulse_Point_Direct_Desktop_BTU_Standard_5": "Pulse_Point_Direct_Desktop_BTU_Standard_5_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_6": "Pulse_Point_Direct_Desktop_BTU_Standard_6_DemandExtreme",
        "Pulse_Point_Direct_Desktop_BTU_Standard_7": "Pulse_Point_Direct_Desktop_BTU_Standard_7_DemandExtreme"
    }

    SpringServe_dict = {
        "Taboola_MX_$1_Floor": "SelectMedia_Direct_Desktop_MX-1_DemandExtreme",
        "Taboola_AUS_$2.5_Floor": "SelectMedia_Direct_Desktop_AUS-2.5_DemandExtreme",
        "Taboola_BR_$1_Floor": "SelectMedia_Direct_Desktop_BR-1_DemandExtreme",
        "Taboola-JS-AUS_$2.5_Floor": "SelectMedia_Direct_Desktop_AUS-2.5_JS",
        "Taboola_Anglo_+FR_+DE_SP_$4_Floor": "SelectMedia_Direct_Desktop_FR-DE-SmallPlayer-4_DemandExtreme",
        "Taboola-JS-_Anglo_+FR_+DE_SP_$4_Floor": "SelectMedia_Direct_Desktop_FR-DE-SmallPlayer-4_JS_DemandExtreme"
    }

    Optimatic_dict = {
        "Taboola APAC HK": "SelectMedia_Direct_Desktop_HK_DemandExtreme",
        "Taboola APAC JP": "SelectMedia_Direct_Desktop_JP_DemandExtreme",
        "Taboola APAC MY": "SelectMedia_Direct_Desktop_MY_DemandExtreme",
        "Taboola APAC MY $3 floor": "SelectMedia_Direct_Desktop_MY-3_DemandExtreme",
        "Taboola APAC PH": "SelectMedia_Direct_Desktop_PH_DemandExtreme",
        "Taboola APAC SG": "SelectMedia_Direct_Desktop_SG_DemandExtreme",
        "Taboola APAC SG $3.5 floor": "SelectMedia_Direct_Desktop_SG-3.5_DemandExtreme",
        "Taboola APAC TH": "SelectMedia_Direct_Desktop_TH_DemandExtreme"
        }

    LKQD_dict = {
        "SelectMedia_MW_AUS_Android_$2_floor": "SelectMedia_Direct_Mobile_AUS-Android-2_DemandExtreme",
        "SelectMedia_MW_BR-IOS_$0.5_floor": "SelectMedia_Direct_Mobile_BR-IOS-0.5_DemandExtreme",
        "SelectMedia_MW_BR-IOS_$1_floor": "SelectMedia_Direct_Mobile_BR-IOS-1_DemandExtreme",
        "SelectMedia_MW_HK-Android_$1_floor": "SelectMedia_Direct_Mobile_HK-Android-1_DemandExtreme",
        "SelectMedia_MW_HK-IOS_$1_floor": "SelectMedia_Direct_Mobile_HK-IOS-1_DemandExtreme",
        "SelectMedia_MW_JP-IOS_$2_floor": "SelectMedia_Direct_Mobile_JP-IOS-2_DemandExtreme",
        "SelectMedia_MW_MX-Android_$1_floor": "SelectMedia_Direct_Mobile_MX-Android-1_DemandExtreme",
        "SelectMedia_MW_MX-IOS_$1_floor": "SelectMedia_Direct_Mobile_MX-IOS-1_DemandExtreme",
        "SelectMedia_MW_SG-Android_$2_floor": "SelectMedia_Direct_Mobile_SG-Android-2_DemandExtreme",
        "SelectMedia_MW_SG-IOS_$2_floor": "SelectMedia_Direct_Mobile_SG-IOS-2_DemandExtreme"
        }

    Thrive_dict = {
        "Thrive_Mobile_2": "Thrive_Direct_Mobile_2_DemandExtreme",
        "Thrive_Direct_Desktop_5": "Thrive_Direct_Desktop_5_DemandExtreme"
    }

    IronSource_dict = {
        "IronSource_Direct_Desktop_US-5.5": "IronSource_Direct_Desktop_US-5.5_DemandExtreme",
        "IronSource_Direct_Desktop_US-6.5": "IronSource_Direct_Desktop_US-6.5_DemandExtreme",
        "IronSource_Direct_Desktop_US-7.5": "IronSource_Direct_Desktop_US-7.5_DemandExtreme",
    }

        
    
    COMMASPACE = ', '

    sender = 'YOUR GMAIL ADDRESS'
    gmail_password = 'YOUR GMAIL PASSWORD'
    recipients = ['EMAIL ADDRESSES HERE SEPARATED BY COMMAS']

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'EMAIL SUBJECT'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = ['FULL PATH TO ATTACHMENTS HERE']

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
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
