import imaplib
import email
import os
import sys
from config import mailcfg
import re
from run import process 
from datetime import datetime
os.chdir(sys.path[0])
  
mail= imaplib.IMAP4_SSL('imap.gmail.com')

mail.login(mailcfg['fromaddr'],mailcfg['psswd'])
mail.select("Inbox")
typ, msgs = mail.search(None, 'Subject', '"{}"'.format('Your Kindle Notes From'))
msgs = msgs[0].split()

# iterate through emails from latest to oldest
msgs = msgs[-5:][::-1]


def clean_file_name(fname):
	allowed_chars = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))
	allowed_special_chars = [ord(x) for x in '`~!@#$%&*()-_=+[{]}|;:?.>,< ']
	allowed_chars += allowed_special_chars
	return ''.join(list(filter(lambda x:ord(x) in allowed_chars, fname)))




print(f'Downloading and parsing started at : {str(datetime.now()).split(".")[0]}\n')

unique_books = set()
for num in msgs:
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
		fileName = clean_file_name(part.get_filename())
		
		# Do not download and parse same book multiple times
		if fileName in unique_books:
			continue
		else:
			unique_books.add(fileName)

		if bool(fileName) and 'csv' in fileName:

			fileName = fileName.replace('.csv', '') + f'___{sender_info}' + '.csv'
			filePath = os.path.join('../data', fileName)
			if not os.path.isfile(filePath) :
				fp = open(filePath, 'wb')
				fp.write(part.get_payload(decode=True))
				fp.close()
			subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
			print('Downloaded : "{file}"'.format(file=fileName))


			print('Parsing book...')
			process(filePath)
print('\n'*3)