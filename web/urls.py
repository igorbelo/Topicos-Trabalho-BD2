from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/?$', views.Login.as_view(), name='login'),
    url(r'^index/?$', views.Index.as_view(), name='index'),
]
