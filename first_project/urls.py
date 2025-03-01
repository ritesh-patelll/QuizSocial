from django.urls import re_path
from django.conf import settings
from django.views.static import serve

from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from home.sitemaps import StaticViewsSitemap, DynamicViewsSitemap
from django.contrib.sitemaps.views import sitemap

# from dumdumsocialbot import urls as dumdumsocialbot_urls

handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'
handler403 = 'home.views.error_403'
handler400 = 'home.views.error_400'

sitemaps = {
    'static_urls': StaticViewsSitemap,
    'dynamic_urls': DynamicViewsSitemap
}

urlpatterns = [
    path('secrete/adminpanal/qsap/access/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('dumdumsocialbot.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

