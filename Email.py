# -*- coding: utf-8 -*-
"""
Created on Thu May 24 15:13:46 2018

@author: mangz
"""
import spam_email_3 as mL
import time
import json
import random
import gmail
import outlook
import sys


class Email:
    
    def __init__(self, _id, _date, _from, _to, _subject, _body, _label = ""):
        self._id = _id
        self._date = _date
        self._from = _from
        self._to = _to
        self._subject = _subject
        self._body = _body
        self._label = _label
        
    def printEmail(self):
        
        print( " " )
        print("Email Id: " + str(self._id))
        print("Date: " + self._date)
        print("From: " + self._from)
        print("To: " + self._to)
        print("Subject: " + str(self._subject))
        print("Label: " + self._label)
        print("Body: \n" + self._body)
        print( "-------------------------" )
        
class Account:
    
    def __init__(self, user, latest_id = 1):
        self.user = user
        self.latest_id = latest_id
        
    def jsonDefault(self):
        #convert to json object
        return self.__dict__

class jsonHelper:
        
    def appendAccount(account):
        with open('Accounts.json') as json_file:
            data = json.load(json_file)
            data['accounts'].append(account.jsonDefault())
            
        with open('Accounts.json', 'w') as json_file:
            json.dump(data, json_file)
            
    def updateAccount(account):
        with open('Accounts.json') as json_file:
            data = json.load(json_file)
            for acc in data['accounts']:
                if acc['user'] == account.user:
                    acc['latest_id'] = account.latest_id
                    break
        with open('Accounts.json', 'w') as json_file:
            json.dump(data, json_file)
    
    def getAccount(user):
        account = Account(user)
        with open('Accounts.json') as json_file:
            data = json.load(json_file)
            for acc in data['accounts']:
                if acc['user'] == user:
                    account = Account(user, acc['latest_id'])
        return account
            
def main():
    #user and password declared
    user = "email"
    password = "pwd"
    #account = jsonHelper.getAccount(user)
    
    #mail = gmail.Gmail()
    folder_name = "NonUnc"
    outlook_mail = outlook.Outlook()
    outlook_mail.login(user, password)
    outlook_mail.inbox()
    
    """
    unc = mL.init_lists('unc/')
    non_unc = mL.init_lists('non_unc/')
    
    unc_emails = [(email, 1) for email in unc]
    non_unc_emails = [(email, 0) for email in non_unc]
    all_emails = unc_emails + non_unc_emails
    random.shuffle(all_emails)
    
    all_features = [(mL.get_features(email, 'bow'), label) for (email, label) in all_emails]
    train_set, test_set, classifier = mL.train(all_features, 0.8)
    mL.evaluate(train_set, test_set, classifier)
    """
    
    ids = outlook_mail.allIds()
    count = 0
    
    i = outlook_mail.get_newest_mail()
    outlook_mail.move_to_folder(i, folder_name)
    
    for id_ in ids:
        break
        try:
            email_message = outlook_mail.getEmail(id_)
            email_body = outlook_mail.get_text_body(email_message)
            if (mL.spam_or_ham(email_body, classifier) == 1 ):
                outlook_mail.move_to_folder(id_, folder_name)
            count += 1
            progress(count)
        except Exception as e:
            print(id_)
            print(e)
            
    outlook_mail.close()
    outlook_mail.logout()
    
    """
    #get list of example spam and ham data
    spam = mL.init_lists('enron1/spam/')
    ham = mL.init_lists('enron1/ham/')

    # 1 if it's spam, 0 if it's ham
    spam_emails = [(email, 1) for email in spam]
    ham_emails = [(email, 0) for email in ham]
    all_emails = spam_emails + ham_emails

    random.shuffle(all_emails)
    
    for word in all_emails:
        print(word[1])
    
    #bow_model
    all_features = [(mL.get_features(email, 'bow'), label) for (email, label) in all_emails]
    

    #default_model
    #all_features = [(mL.get_features(email, ''), label) for (email, label) in all_emails]
    train_set, test_set, classifier = mL.train(all_features, 0.8)
    
    #mL.evaluate(train_set, test_set, classifier)
    """    
    """
    while 1:
    # Have to login/logout each time because that's the only way to get fresh results.
    
        #open up imap connection with specified user and password
        mail.connect(account, password)
        mail.inbox()
        
        #return list of email ids of emails that have not been processed
        data = mail.unchecked_emails(account.latest_id)
        uids = [int(i) for i in data[0].split()]
        #uids length will be one if no new emails are being read b/c it includes itself.
            #create the list of ids from unchecked mail    
            
        for uid in uids:
            
            #check to make sure we're only getting ids > than recently_checked id   
            if uid > account.latest_id or uid == 1:
                emaiL = processEmail(mail, uid)
                print("This mail is " + mL.spam_or_ham(emaiL._body, classifier))
                account.latest_id = uid
                jsonHelper.updateAccount(account)
                    
        mail.close()
        mail.logout()
        print("Logged out")
        time.sleep(10) 
        break
    """

def processEmail(mail, uid):
    email_message = mail.get_mail(uid)
    print("this is")
    print(email_message["Authentication-Results"])
    #return email object, so stuff can be done to it
    if email_message == "None":
        print("it is none")
        return email_message
    else:
        new_email = mail.basic_info(uid, email_message)
        new_email.printEmail()
        return new_email   

def write_to_folder(path, filename, count, content):   
    filename += str(count)
    filename += ".txt"
    path += filename
    create_text_file(path, content)
    
def create_text_file(path, content):
    file = open(path,"w+")
    file.write(content)
    file.close()
    
def progress(count):
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
#run main
if __name__ == '__main__':
    main()
