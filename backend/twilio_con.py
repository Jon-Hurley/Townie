from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

t = Client(
    username=os.environ.get('TWILIO_SID'),
    password=os.environ.get('TWILIO_AUTH_TOKEN')
)
verify_sid = os.environ.get('TWILIO_VERIFY_SID')

def sendVerification(phone):
    verification = t.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=phone, channel="sms")
    return verification.status

def testVerification(phone, otp):
    verification_check = t.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=phone, code=otp)
    return verification_check.status

# res = verifyUser("+13176909263")
# print(res)