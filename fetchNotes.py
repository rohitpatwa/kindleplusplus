import imaplib
import email
import os
from config import mailcfg
import re
  
mail= imaplib.IMAP4_SSL('imap.gmail.com')

mail.login(mailcfg['fromaddr'],mailcfg['psswd'])
mail.select("Inbox")
typ, msgs = mail.search(None, 'Subject', '"{}"'.format('Your Kindle Notes From'))
msgs = msgs[0].split()

for num in msgs[-3:]:
	raw_email = mail.fetch(num,'(RFC822)')
	raw_email_str = raw_email[1][0][1].decode('UTF-8')
	email_message = email.message_from_string(raw_email_str)

	sender_info = email_message.get('from')


	for part in email_message.walk():
		# this part comes from the snipped I don't understand yet... 
		if part.get_content_maintype() == 'multipart':
			continue
		if part.get('Content-Disposition') is None:
			continue
		fileName = part.get_filename()
		if bool(fileName) and 'csv' in fileName:
			fileName = fileName.replace('.csv', '') + f'___{sender_info}' + '.csv'
			filePath = os.path.join(fileName)
			if not os.path.isfile(filePath) :
				fp = open(filePath, 'wb')
				fp.write(part.get_payload(decode=True))
				fp.close()
			subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
			print('Downloaded "{file}" from email titled "{subject}"'.format(file=fileName, subject=subject))

