import imaplib, email

org_email = "@gmail.com"
from_email = "mangzalal" + org_email
from_pwd = "mfpr nwax tyir wjdd"
smtp_server = "imap.gmail.com"
smtp_port = 993

def readmail():
	# mail reading logic
	try:
		#connecting to SMTP server over ssl
		mail = imaplib.IMAP4_SSL(smtp_server)
		mail.login(from_email, from_pwd)

		#grabbing inbox from mail
		mail.select('inbox')

		#searching for mails in the inbox, returns list of ids per email
		type, data = mail.search(None, 'ALL')
		mail_ids = data[0]
		id_list = mail_ids.split

		#grab first and last email id
		first_email_id = int(id_list[0])
		latest_email_id = int(id_list[-1])

		for i in range(latest_email_id, first_email_id, -1):
			typ, data = mail.fetch(i, '(RFC822)' )

			for response_part in data:
				if isinstance(response_part, tuple):
					msg = email.message_from_string(response_part[1])
					email_subject = msg['subject']
					email_from = msg['from']
					print('From : ' + email_from + '\n')
					print('Subject : ' + email_subject + '\n')
					print('Message: ' + msg + '\n')
					print('<----------------------------------------->')

	except:
		print('Could not connect')	

readmail()