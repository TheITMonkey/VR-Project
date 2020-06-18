#!/usr/bin/python

import smtplib

sender = 'teste@gcom.di.uminho.pt'
receiver = 'a78322@alunos.uminho.pt'
smtp_address = 'mailServer:25'

def sendEmail(sender,receiver,subject,content):

    message = """From: From Person <%s>
        To: To Person <%s>
        Subject: %s
        %s
        """% (sender+'@gcom.di.uminho.pt', receiver, subject, content)
    print(message)
    try:
        smtpObj = smtplib.SMTP(smtp_address)
        smtpObj.sendmail(sender, receiver, message)         
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")
