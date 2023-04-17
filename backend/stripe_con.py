import stripe
import os
import dotenv
dotenv.load_dotenv()

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

def createCheckoutSession():
    return stripe.checkout.Session.create(
        success_url='http://localhost:5173/app/account?success=true',
        cancel_url='http://localhost:5173/app/account?success=false',
        mode='subscription',
        line_items=[
            {
                'price': os.environ.get('STRIPE_PRICE_ID'),
                'quantity': 1
            }
        ]
    )

def getSubscriptionEvent(request):
    try:
        signature = request.headers['stripe-signature']
        event = stripe.Webhook.construct_event(
            payload=request.body,
            sig_header=signature,
            secret=os.environ.get('STRIPE_WEBHOOK_SECRET')
        )
        return event['data']['object'], event['type']
    except Exception as e:
        print(e)
        return None, None

def cancelSubscription(subscriptionId):
    stripe.Subscription.modify(
        subscriptionId,
        cancel_at_period_end=True
    )

def expireSession(sessionId):
    try:
        stripe.checkout.Session.expire(sessionId)
        return True
    except:
        return False
