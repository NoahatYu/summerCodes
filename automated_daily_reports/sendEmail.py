import smtplib
import datetime
from datetime import timedelta
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

LKQD_dict = {"SelectMedia_MW_AUS_Android_$2_floor": "SelectMedia::Direct::Mobile::AUS-Android-2_DemandExtreme",
                "SelectMedia_MW_BR-IOS_$0.5_floor": "SelectMedia::Direct::Mobile::BR-IOS-0.5_DemandExtreme",
                "SelectMedia_MW_BR-IOS_$1_floor": "SelectMedia::Direct::Mobile::BR-IOS-1_DemandExtreme",
               "SelectMedia_MW_HK-Android_$1_floor": "SelectMedia::Direct::Mobile::HK-Android-1_DemandExtreme",
                "SelectMedia_MW_HK-IOS_$1_floor": "SelectMedia::Direct::Mobile::HK-IOS-1_DemandExtreme",
                "SelectMedia_MW_JP-IOS_$2_floor": "SelectMedia::Direct::Mobile::JP-IOS-2_DemandExtreme",
               "SelectMedia_MW_MX-Android_$1_floor" : "SelectMedia::Direct::Mobile::MX-Android-1_DemandExtreme",
                "SelectMedia_MW_MX-IOS_$1_floor": "SelectMedia::Direct::Mobile::MX-IOS-1_DemandExtreme",
                "SelectMedia_MW_SG-Android_$2_floor": "SelectMedia::Direct::Mobile::SG-Android-2_DemandExtreme",
                "SelectMedia_MW_SG-IOS_$2_floor": "SelectMedia::Direct::Mobile::SG-IOS-2_DemandExtreme"}

from_address = ""
to_address = "daniel.t@taboola.com"

#date_post = datetime.now() - timedelta(days=2)
#date_post = date_post.strftime(("%B %d, %Y"))

#nameOfFile = final_taboola + "_" + date_post

msg = MIMEMultipart()

msg['From'] = from_address
msg['To'] = to_address
msg['Subject'] = "" # SUBJECT OF THE EMAIL

body = "" # TEXT YOU WANT TO SEND

msg.attach(MIMEText(body, 'plain'))

filename = ""     #"NAME OF THE FILE WITH ITS EXTENSION"
attachment = open("", "rb") # PATH OF THE FILE

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(from_address, "password")
text = msg.as_string()
server.sendmail(from_address, to_address, text)
server.quit()
