import smtplib
from email.message import EmailMessage
from configparser import ConfigParser

# Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

# Get the creds
creds = config_object['password']

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    
    #provide email and password
    user = "pri.test2103@gmail.com"
    password = creds
    msg['from'] = user
    
    #create server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    #server setting needed by gmail
    server.starttls()
    #login to server
    server.login(user,password['password'])
    #send msg
    server.send_message(msg)
    #close server conn
    server.quit()

if __name__ == '__main__':
    email_alert("Test", "Hello, sent using Python!", "pri.test2103@gmail.com")