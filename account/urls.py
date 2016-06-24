from django.conf.urls import url
from .views import login, home, logout,reset_password, activate_user, google_login

urlpatterns = [
    url(r'^login/$', login, name ="login" ),
    url(r'^logout/$', logout, name ="logout" ),
    url(r'^(?P<id>\d+)/home/$', home, name = "home"),
    url(r'^reset/(?P<id>\d+)/(?P<otp>\d{4})/$', reset_password, name='reset-password'),
    url(r'^activate/(?P<id>\d+)/(?P<otp>\d{4})/$', activate_user, name='activate'),
    url(r'^google_auth/$',google_login, name = "google-login"),
]