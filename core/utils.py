from core.models import Profile
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from urllib2 import urlopen

def create_or_update_profile(strategy, user, response, details, is_new=False, *args, **kwargs):
    email = details['email']
    user = User.objects.get(email=email)

    profile, _ = Profile.objects.get_or_create(
        user=user
    )

    if is_new and strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture?width=320&height=320'.format(response['id'])
        photo = urlopen(url)
        profile.photo.save(
            '{0}_social.jpg'.format(user.username),
            ContentFile(photo.read())
        )
        profile.save()
