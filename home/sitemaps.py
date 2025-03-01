from django.contrib import sitemaps
from django.urls import reverse
from .models import quiz_social_movie_data, quiz_social_serie_data, movie_quiz_mcq_data_one, movie_quiz_mcq_data_two, serie_quiz_mcq_data_one, serie_quiz_mcq_data_two, serie_quiz_mcq_data_three, serie_quiz_mcq_data_four
from itertools import chain
from datetime import datetime

class StaticViewsSitemap(sitemaps.Sitemap):
    
    priority = 0.5
    changefreq = 'daily'

    def items(self):

        return [
            'home',
            ]

    def lastmod(self, item):
        return datetime.now()

    def location(self, item):
        return reverse(item)
        
class DynamicViewsSitemap(sitemaps.Sitemap):

    priority = 0.5
    changefreq = 'daily'

    def items(self):

        whole_url = []
        whole_url = list(chain(whole_url, movie_quiz_mcq_data_one.objects.all()))
        whole_url = list(chain(whole_url, movie_quiz_mcq_data_two.objects.all()))
        whole_url = list(chain(whole_url, serie_quiz_mcq_data_one.objects.all()))
        whole_url = list(chain(whole_url, serie_quiz_mcq_data_two.objects.all()))
        whole_url = list(chain(whole_url, serie_quiz_mcq_data_three.objects.all()))
        whole_url = list(chain(whole_url, serie_quiz_mcq_data_four.objects.all()))

        return whole_url

    def lastmod(self, item):
        return datetime.now()