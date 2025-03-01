from home.models import Profile
from django.utils import timezone
from datetime import timedelta

def ReferalProgram():
    getting_profile_list = Profile.objects.filter(sub_week_referrals='False', recommended_by__isnull=False)
    for one_by_one_profile in getting_profile_list:
        if one_by_one_profile.recommended_by_expiry_date < timezone.now():
            print(one_by_one_profile)
            one_by_one_profile.recommended_by = None
            one_by_one_profile.save()