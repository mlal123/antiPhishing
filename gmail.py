import imaplib, email, os, datetime
import Email
import base64

"""
#variable initialization
pwd = "mfpr nwax tyir wjdd"
imap_url = 'imap.gmail.com'
attachment_dir = 'C:/Users/mangz/Documents/Python Projects/'
"""
class Gmail():
    def __init__(self):
        mydate = datetime.datetime.now()-datetime.timedelta(1)
        self.today = mydate.strftime("%d-%b-%Y")
        self.url = "imap.gmail.com"
        
    def connect(self, account, password):
        #make connection with user and password --> return connection
        print("Making connection")
        try:
            self.imap = imaplib.IMAP4_SSL(self.url)
            print("Logging in...")
            self.imap.login(account.user, password)
            print("Log in success!")
        except Exception as err:
            print('ERROR:', err)
            
    def inbox(self):
        return self.imap.select("INBOX")

    def get_text_body(self, email_message):
        body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

        # skip any text/plain (txt) attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload().split('\r\n\r\n2015')[0]  # decode
                    break
# not multipart - i.e. plain text, no attachments, keeping fingers crossed
        else:
            body = email_message.get_payload().split('\r\n\r\n2015')[0]
        return body

    def fetch_mail(self, mail_id):
        result, email_data = self.imap.uid('fetch', str(mail_id), '(RFC822)')
        return email_data
    
    def get_mail(self, mail_id):
        #takes in mail id
        email_data = self.fetch_mail(mail_id)
    
        if (email_data[0] == None):
            return "None"
        raw_email = email_data[0][1].decode('utf-8')
        email_message = email.message_from_string(raw_email)
        return email_message

    def basic_info(self, _id, email_message):
        #returns Email object
        _email = Email.Email(_id, email_message['Date'], email_message['From'],
                         email_message['To'], email_message['Subject'], str(self.get_text_body(email_message)) )
        return _email

    def get_newest_mail(self):
        #returns Email object of the newest email
        result, data = self.imap.search(None, "ALL")
        mails = data[0].split()
        newest_id = mails[-1]
        newest = self.fetch_mail(newest_id)
        newest_mail = self.basic_info(newest_id, newest)
        return newest_mail

    def unchecked_emails(self, _id):
        #return list of unchecked email_ids, email ids that are greater than or equal to recently checked id (_id),
        #which gets  updated with each email it checks.
        result, data = self.imap.uid('search', None, 'UID ' + str(_id) + ':*')
        return data

    def move_to_spam(self, uid):
        result = self.imap.uid('COPY', str(uid), 'Spam')
        
        if result[0] == 'OK':
            mov, data = self.imap.uid('STORE', str(uid) , '+FLAGS', '(\Deleted)')
            self.imap.expunge()
    def close(self):
        return self.imap.close()
    
    def logout(self):
        return self.imap.logout()
 
    """
def get_attachments(msg):
    for part in msg.walk():
        if part.get_content_maintype()=="multipart":
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            
            filePath = os.path.join(attachment_dir, fileName)
            with open(filePath, 'wb') as f:
                f.write(part.get_payload(decode=True))
"""
