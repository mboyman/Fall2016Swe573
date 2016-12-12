import requests
import sendgrid
import os

def send_sms(message, number):
    payload = {'Username': 'rebus',
               'Password': '317500',
               'Msisdns': number,
               'Messages': message,
               'TransmissionID': 'REBUS LABS'
               }
    if number[:2] != '90':
        payload['TransmissionID'] = '905498030816'
        payload['Channel'] = 'YD'
    r = requests.post(
        "http://www.biotekno.biz:8080/SMS-Web/HttpSmsSend?", data=payload)
    print(r.text)


def send_email(_from ,_to, _subject, _message):
    sg_username = "azure_382d070917a3c61ea4bc4bbde2f1fffe@azure.com"
    sg_password = "J6JcfxBhSO6B00e"
    sg = sendgrid.SendGridClient(sg_username, sg_password)
    message = sendgrid.Mail()
    message.set_from(_from)
    message.set_subject(_subject)
    message.set_text(_message)
    message.set_html("")
    message.add_to(_to)
    status, msg = sg.send(message)
    print (msg)

send_sms("Hi Philippe this is a test SMS from RebusLabs 06/12/2016 07:37:00 GMT+0 .","33674528120")