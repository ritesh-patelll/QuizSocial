from home.models import Profile
import stripe
from first_project import settings

def StripeAccount():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    getting_profile_list = Profile.objects.filter(stripe_user_id__isnull=False, verify_identity='False')
    for one_by_one_profile in getting_profile_list:
        account = stripe.Account.retrieve(one_by_one_profile.stripe_user_id)
        if len(account["requirements"]["eventually_due"]) == 0:
            one_by_one_profile.verify_identity = True
            one_by_one_profile.save()