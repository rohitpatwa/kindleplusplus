# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 22:59:50 2020

@author: 2ativ
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import mailcfg 

 
def sendmail(book_name, authors,note):
    fromaddr = f'{mailcfg["fromname"]}<{mailcfg["fromaddr"]}>'		 
    toaddr = mailcfg['toaddr']
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    sb = book_name.split()[0] if len(book_name.split()[0]) > 4 else book_name[:15] + '...'
    msg['Subject'] = f"Trying with HTML | {sb}"
    new_body=""
    with open('/trial.txt',"r") as f:
        data=f.readlines()
    data[35]=sb
    data[38]=authors
    data[43]=note
    new_body=""
    for i in data:
        new_body=new_body+i
    msg.attach(MIMEText(new_body,'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mailcfg['fromaddr'], mailcfg['psswd'])
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr.split(','), text)
    server.quit()

