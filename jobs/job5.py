from home.models import Profile
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
from django.contrib.auth.models import User

def AutoRenewSub():
    referral_program_money_distri = {'S': 1, 'SS': 2, 'SDS': 3, 'FS': 4}
    getting_an_subscription_list = Profile.objects.filter(auto_renew='True', sub_expiry_date__lt=timezone.now()).exclude(sub_type='F')
    for one_by_one_sub in getting_an_subscription_list:
        if one_by_one_sub.sub_expiry_date < timezone.now() + timedelta(hours=6):
            one_by_one_sub.sub_expiry_date = timezone.now() + timedelta(days=30, hours=6)
            if one_by_one_sub.sub_type == 'S':
                one_by_one_sub.social_month = F('social_month') + 1
            elif one_by_one_sub.sub_type == 'SS':
                one_by_one_sub.social_month = F('super_social_month') + 1
            elif one_by_one_sub.sub_type == 'SDS':
                one_by_one_sub.social_month = F('super_duper_social_month') + 1
            elif one_by_one_sub.sub_type == 'FS':
                one_by_one_sub.social_month = F('fan_social_month') + 1
            one_by_one_sub.save()

            if one_by_one_sub.recommended_by != '' and one_by_one_sub.sub_week_referrals == True:
                Profile.objects.filter(user = User.objects.filter(username=one_by_one_sub.recommended_by).first()).update(withdrawal_amount=F('withdrawal_amount') + referral_program_money_distri[one_by_one_sub.sub_type], total_revenue=F('total_revenue') + referral_program_money_distri[one_by_one_sub.sub_type])
            