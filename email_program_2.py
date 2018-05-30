import imaplib, email, os, datetime
import Email
import base64
"""
#variable initialization
pwd = "mfpr nwax tyir wjdd"
imap_url = 'imap.gmail.com'
attachment_dir = 'C:/Users/mangz/Documents/Python Projects/'
"""
recently_checked_id = 1

def connect(account, password):
    #make connection with user and password --> return connection
    url = 'imap.gmail.com'
    print("Making connection")
    conn = imaplib.IMAP4_SSL(url)
    try:
        print("Logging in...")
        conn.login(account.user, password)
        print("Log in success!")
        conn.select('INBOX')
    except Exception as err:
        print('ERROR:', err)
    return conn
    
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

def get_emails(conn, result_bytes):
    #returns list of emails
    msg = []
    for num in result_bytes[0].split():
        typ, data = conn.fetch(num, '(RFC822)')
        msg.append(data)
    return msg

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

def get_text_body(email_message):
    body = ""

    if email_message.is_multipart():
        for part in email_message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

        # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
# not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body = email_message.get_payload(decode=True)
    return body

def get_emails_from_date(conn, date):
    date_search = '(SINCE "' + date + '")'
    typ, emails = conn.search(None, date_search)
    for mail_id in emails[0].split():
        email_message = get_mail(conn, mail_id)
        basic_info(email_message)

def get_mail(conn, mail_id):
    #takes in mail id
    email_data = fetch_mail(conn, mail_id)
    
    if (email_data[0] == None):
        return "No email data for that id"
    raw_email = email_data[0][1].decode('utf-8')
    email_message = email.message_from_string(raw_email)
    return email_message

def fetch_mail(conn, mail_id):
    result, email_data = conn.uid('fetch', str(mail_id), '(RFC822)')
    return email_data

def basic_info(_id, email_message):
    #returns Email object
    _email = Email.Email(_id, email_message['Date'], email_message['From'],
                         email_message['To'], email_message['Subject'], str(get_text_body(email_message)) )
    return _email

def get_all_emails(conn):
    #returns list of email ids
    result, data = conn.search(None, "ALL")
    return data

def get_newest_mail(conn):
    #returns Email object of the newest email
    result, data = conn.search(None, "ALL")
    mails = data[0].split()
    newest_id = mails[-1]
    newest = fetch_mail(conn, newest_id)
    newest_mail = basic_info(newest_id, newest)
    return newest_mail

def unchecked_emails(conn, _id):
    #return list of unchecked email_ids, email ids that are greater than or equal to recently checked id (_id),
    #which gets  updated with each email it checks.
    result, data = conn.uid('search', None, 'UID ' + str(_id) + ':*')
    return data

def move_to_spam(conn, uid):
    result = conn.uid('COPY', str(uid), 'Spam')

    if result[0] == 'OK':
        mov, data = conn.uid('STORE', str(uid) , '+FLAGS', '(\Deleted)')
        conn.expunge()
 

