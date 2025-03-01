from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [
    path("", views.index, name='home'),
    path("home", views.home, name='Home'),
    path("signin", views.signin, name='Signin'),
    path("signout", views.signout, name='Signout'),
    path("profile", views.profile, name='Profile'),
    path("referral_program", views.referral_program, name='ReferralProgram'),
    path("events", views.events_page, name='Events'),
    path("errorresult", views.errorresult, name='errorresult'),
    path("privacypolicy", views.privacypolicy, name='PrivacyPolicy'),
    path("termsofuse", views.termsofuse, name='Termsofuse'),
    path("admin/dashboard", views.dashboard),
    path("getting_leaderboard_data/", views.getting_leaderboard_data),
    path("eventliked/", views.eventliked),
    path("fav/<str:task>/", views.fav_task),
    path("membership/", views.checkout, name='Checkout'),
    path("cancel_subscription/", views.cancel_subscription, name='CancelSubscription'),
    path("webhook/", views.stripewebhook, name='Webhook'),
    path("success/", views.subsuccess, name='Subsuccess'),
    path("create-checkout-session/", views.create_checkout_session, name='create_checkout_session'),
    path("authorize/", views.StripeAccount, name='StripeAccount'),
    path("withdrawmoney/", views.WithdrawMoneyFromStripeAccount, name='WithdrawMoneyFromStripeAccount'),
    path("_link/", views.Redirect_Links, name='RedirectLinks'),
    path('accept_event/<int:event_id>/', views.accept_event, name='accept_event'),
    path('reject_event/<int:event_id>/', views.reject_event, name='reject_event'),

    path('get_token/', views.getToken),
    path('checkroomfull/', views.checkroomfull),
    path('delete_member_from_mr/', views.deleteMemberFromMR),
    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),

    path("loadpage/<str:type_>/<int:type_id>", views.loadpage, name='LoadPage'),
    path("result/<str:type_>/<int:type_id>", views.result, name='Result'),
    path("requestquiz/<int:type_id>/<str:type>", views.requestquiz, name='RequestQuiz'),
    path("download/<str:filename>", views.download_file, name='DownloadFile'),
    path("change/<str:value>/", views.change_profile_data),
    path("ref/<unique_code>", views.refer_by_user, name='ReferByUser'),

    path('room/<room_code>',views.room, name='Room'),
    path('loadpage/<str:type_>/<str:wiki_id>/<str:room_info>', views.loadpage_, name='LoadPage_'),
    # path('<str:link_type>/<str:type_>/<str:wiki_id>/<str:room_info>/<str:username>',views.waitingroom_, name='WaitingRoom_'),

    path("<str:type>/<int:type_id>/mcq/<int:noq>", views.movie_mcq, name='Movie_MCQ'),
    # path("<str:type_name>/<str:type_wiki_id>", views.moviepage, name='MoviePage'),
    path("<str:link_type>/<str:type_>/<int:id>/<str:room_info>", views.waitingroom, name='WaitingRoom'),
    
]