from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

t = Client(
    username=os.environ.get('TWILIO_SID'),
    password=os.environ.get('TWILIO_AUTH_TOKEN')
)

def verifyUser(verified_number):
    verify_sid = os.environ.get('TWILIO_VERIFY_SID')
    verification = t.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")
    print(verification.status)

    otp_code = input("Please enter the OTP:")

    verification_check = t.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=verified_number, code=otp_code)
    return verification_check.status


res = verifyUser("3176909263", "12345")
print(res)