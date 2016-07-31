from django.conf.urls import url
from .views import LandingView

urls = [
    url(r'^$', LandingView.as_view(), name='violet')
]
