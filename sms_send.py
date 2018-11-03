from tracker import *
from twilio.rest import Client
from tw_auth import *

message()

client = Client(account_sid, auth_token)



message = client.messages.create(
                              body= [message()],
                              from_='+1234567890',
                              to=[+1234567890],
                          )

print(message.sid)

# numbers_to_message = ['+17608152442', '+19705316255']
#
# for number in numbers_to_message:
#     client.messages.create(
#         body=[birthday_wish(), birthday_advance()],
#         from_='+12527729034',
#         to = number
#     )
#
# print(message.sid)
