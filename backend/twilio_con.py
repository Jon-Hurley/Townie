from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

verify_sid = os.environ.get('TWILIO_VERIFY_SID')

def sendVerification(phone):
    t = Client(
        username=os.environ.get('TWILIO_SID'),
        password=os.environ.get('TWILIO_AUTH_TOKEN')
    )
    verification = t.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=phone, channel="sms")
    return verification.status

def testVerification(phone, otp):
    t = Client(
        username=os.environ.get('TWILIO_SID'),
        password=os.environ.get('TWILIO_AUTH_TOKEN')
    )
    verification_check = t.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=phone, code=otp)
    return verification_check.status == "approved"

# It's fine if it errors, so let it if it happens to.
def sendNotification(phone, message):
    return
    try:
        t = Client(
            username=os.environ.get('TWILIO_SID_2'),
            password=os.environ.get('TWILIO_AUTH_TOKEN_2')
        )
        return t.messages.create(
            from_='+18556853245',
            body=message,
            to=phone
        )
    except:
        return