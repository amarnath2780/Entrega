import os
from django.conf import settings
from twilio.rest import Client
from entrega.settings import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,TWILIO_SERVICE_SID

def verify(phone_number):
      account_sid = TWILIO_ACCOUNT_SID
      # Your Auth Token from twilio.com/console
      auth_token  = TWILIO_AUTH_TOKEN
      client = Client(account_sid, auth_token)
      verification = client.verify \
                     .services(TWILIO_SERVICE_SID) \
                     .verifications \
                     .create(to='+91'+ phone_number, channel='sms')
      print(verification.sid)

def verify_check(mobile,otp):
    number = '+91'+str(mobile)
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    service_id = TWILIO_SERVICE_SID
    client = Client(account_sid, auth_token)

    verification_check = client.verify \
                            .services(service_id) \
                            .verification_checks \
                            .create(to=number, code=otp)

    print(verification_check.status)
    
    if verification_check.status == 'approved':
        print('Verification Conform')
        return True
    else:
        return False
