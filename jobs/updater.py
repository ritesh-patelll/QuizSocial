from apscheduler.schedulers.background import BackgroundScheduler
# from .job1 import EventCreator
from .job2 import TopListCreator
from .job3 import SupervisingRooms
from .job4 import AssigningRank
from .job5 import AutoRenewSub
from .job6 import ReferalProgram
from .job7 import StripeAccount
from .job8 import EventCreator

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(EventCreator, "interval", days=1, id='Event_Creator', replace_existing=True)
	scheduler.add_job(StripeAccount, "interval", hours=6, id='Stripe_Account', replace_existing=True)
	scheduler.add_job(ReferalProgram, "interval", days=1, id='Referal_Program', replace_existing=True)
	scheduler.add_job(AutoRenewSub, "interval", hours=6, id='Auto_Renew_Sub', replace_existing=True)
	scheduler.add_job(AssigningRank, "interval", days=1, id='Assigning_Rank', replace_existing=True)
	scheduler.add_job(SupervisingRooms, "interval", minutes=15, id='Supervising_Rooms', replace_existing=True)
	scheduler.add_job(TopListCreator, "interval", days=7, id='Top_List_Creator', replace_existing=True)
	# scheduler.add_job(EventCreator, "interval", days=7, id='Top_List_Creator', replace_existing=True)
	scheduler.start()
	# TopListCreator()
	# SupervisingRooms()
	# AssigningRank()
	# AutoRenewSub()
	# ReferalProgram()
	# StripeAccount()
	# EventCreator()