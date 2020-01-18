
# Python 2.x

# import smtplib
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText


# Python 3.x

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import mailcfg 

 
def sendMail(sub, body):
	fromaddr = f'{mailcfg["fromname"]}<{mailcfg["fromaddr"]}>'
						 
	toaddr = mailcfg['toaddr']
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr

	sub = sub.split()[0] if len(sub.split()[0]) > 4 else sub[:15] + '...'
	msg['Subject'] = f"Highlight of the day! | {sub}"
	 
	body = '<font face="Courier New, Courier, monospace">' + body + '</font>'
	msg.attach(MIMEText(body,'html'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(mailcfg['fromaddr'], mailcfg['psswd'])
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr.split(','), text)
	server.quit()
