from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/?$', views.Login.as_view(), name='login'),
    url(r'^logout/?$', views.Logout.as_view(), name='logout'),
    url(r'^index/?$', views.Index.as_view(), name='index'),
    url(r'^teams/add/?$', views.CreateTeam.as_view(), name='create_team'),
    url(r'^teams/(?P<pk>[0-9]+)/?$', views.ShowTeam.as_view(), name='team'),
    url(r'^teams/(?P<pk>[0-9]+)/change/?$', views.UpdateTeam.as_view(), name='update_team'),
    url(r'^teams/(?P<team_id>[0-9]+)/athletes/?$', views.AthleteList.as_view(), name='athlete_list'),
    url(r'^teams/(?P<team_id>[0-9]+)/athletes/add/?$', views.CreateAthlete.as_view(), name='create_athlete'),
    url(r'^teams/(?P<team_id>[0-9]+)/athletes/(?P<pk>[0-9]+)/change/?$', views.UpdateAthlete.as_view(), name='update_athlete'),
    url(r'^upload-file/?$', views.UploadFile.as_view(), name='upload_file'),
]
