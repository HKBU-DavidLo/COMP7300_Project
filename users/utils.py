import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure

#account_sid = os.environ['ACffc23d8e042b3db355bf668f22b36bf7']
#auth_token = os.environ['7207aa1585be061ae5e65b5936b9d0d6']


account_sid = 'ACffc23d8e042b3db355bf668f22b36bf7'
auth_token = '7207aa1585be061ae5e65b5936b9d0d6'

client = Client(account_sid, auth_token)


def send_sms(user_code, mobile):
    message = client.messages \
                    .create(
                        body=f'Hi! Your user and verification code is {user_code}',
                        from_='+17077084880',
                        to=f'{mobile}'
                    )

    print(message.sid)
