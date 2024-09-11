 
import smtplib

server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.starttls()

#below password should be from Google Account > Security > App Passwords  NOT the password for your google account
server.login( 'Mishajules24@gmail.com', 'olai gjmv uvzw awya' )
from_mail = 'Mishajules24@gmail.com'

# https://help.inteliquent.com/sending-emails-to-sms-or-mms

#mish
#to = '2817958017@tmomail.net'
#to = 'misha.rem7@gmail.com'
#jules
#to = '464289530@tmomail.net'
#jules friend
#to = '7138197478@vtext.com'


#body = 'The second coming of the prophetic geese has begun!'

#server.sendmail(from_mail, to, message)

# for x in range(6):
#     server.sendmail(from_mail, to, message)
#     print("ran")
 
def sendMessage(body1):
    body = str(body1)
    to = 'misha.rem7@gmail.com'
    message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % '' + "\r\n" + body)
    server.sendmail(from_mail, to, message)
    to = 'julesbeech@icloud.com'
    server.sendmail(from_mail, to, message)

#class Message:
def plantsWateringMessage():
    body = 'Plant is being watered!'
    sendMessage(body)

def plantsNeedWaterMessage():
    body = 'I NEED WATER!!!!'
    sendMessage(body)
        











    #The above is Python code for a Gmail account to send a text message. The Gmail account does need to go to Manage Google Account>Security> App Passwords and create a
    #password. That is the password for the script, NOT the account password 
