# Sending SMS
# we import the Twilio client from the dependency we just installed
from twilio.rest import Client

def sendSms(phone_number,message):
    
    # the following line needs your Twilio Account SID and Auth Token
    client = Client("AC2d781c1c6af484986922b5220aa6979f", "971c27c8396400d53dc528f3b4da7938")
    
    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    # account to send SMS to any phone number
    client.messages.create(to = "+91"+phone_number, 
                           from_ = "+12059904359", 
                           body = message)
    
    # print("Message Sent")

