# -*- coding: utf-8 -*-
"""
Created on Thu May 24 15:13:46 2018

@author: mangz
"""
import spam_email_3 as mL
import email_program_2 as emailHelper
import time
import json
import random

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
        print("Subject: " + self._subject)
        print("Label: " + self._label)
        print("Body: \n" + self._body)
        print( "=======================================================" )
        
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
    account = jsonHelper.getAccount(user)
    
    #get list of example spam and ham data
    spam = mL.init_lists('enron1/spam/')
    ham = mL.init_lists('enron1/ham/')

    # 1 if it's spam, 0 if it's ham
    spam_emails = [(email, 'spam') for email in spam]
    ham_emails = [(email, 'ham') for email in ham]
    all_emails = spam_emails + ham_emails

    random.shuffle(all_emails)

    #bow_model
    all_features = [(mL.get_features(email, 'bow'), label) for (email, label) in all_emails]

    #default_model
    #all_features = [(get_features(email, ''), label) for (email, label) in all_emails]
    train_set, test_set, classifier = mL.train(all_features, 0.8)
    
    mL.evaluate(train_set, test_set, classifier)
    
    while 1:
    # Have to login/logout each time because that's the only way to get fresh results.
    
        #open up imap connection with specified user and password
        conn = emailHelper.connect(account, password)
        
        #return list of email ids of emails that have not been processed
        data = emailHelper.unchecked_emails(conn, account.latest_id)
        uids = [int(i) for i in data[0].split()]
        
        #uids length will be one if no new emails are being read b/c it includes itself.
            #create the list of ids from unchecked mail        
        for uid in uids:
            
            #check to make sure we're only getting ids > than recently_checked id   
            if uid > account.latest_id or uid == 1:
                emaiL = processEmail(conn,uid)
                print("This mail is " + mL.spam_or_ham(emaiL._body, classifier))
                account.latest_id = uid
                jsonHelper.updateAccount(account)
                    
        conn.close()
        conn.logout()
        print("Logged out")
        break
        time.sleep(10)

def processEmail(conn, uid):
    email_message = emailHelper.get_mail(conn, uid)
    
    #return email object, so stuff can be done to it
    new_email = emailHelper.basic_info(uid, email_message)
    new_email.printEmail()
    return new_email

#run main
if __name__ == '__main__':
    main()
