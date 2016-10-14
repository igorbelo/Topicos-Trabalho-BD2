from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.text import slugify

from django.conf import settings as conf
import re
import hmac
import base64
import hashlib
from time import time
from uuid import uuid4

def gen_uuid():
    return seed_uuid(uuid4().hex)

def seed_uuid(sessionid, length=32):
    hex = hashlib.md5(conf.SECRET_KEY + str(sessionid)).hexdigest()
    uid = hex.encode('base64')
    uid = re.sub("[^A-Z0-9]", "", uid.upper())
    if length < 4:
        length = 4
    if length > 128:
        length = 128
    while (len(uid) < length):
        uid = uid + seed_uuid(sessionid, 22)
    return uid[0:length]

def gen_secret_key():
    salt = seed_uuid(64)
    p = {'time': str(time()), 'salt': salt, 'secret': conf.SECRET_KEY}
    digest = hmac.new(urlencode(p), salt, digestmod=hashlib.sha256).hexdigest()
    return quote_plus(base64.b64encode(digest).strip('=='))

class ModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self._select_related = kwargs.pop('select_related', None)
        self._prefetch_related = kwargs.pop('prefetch_related', None)
        super(ModelManager, self).__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(ModelManager, self).get_queryset(*args, **kwargs).\
             exclude(deleted__isnull=False)
        if self._select_related:
            qs = qs.select_related(*self._select_related)
        if self._prefetch_related:
            qs = qs.prefetch_related(*self._prefetch_related)
        return qs

    def deleted(self, *args, **kwargs):
        qs = super(ModelManager, self).get_queryset(*args, **kwargs).\
            exclude(deleted__isnull=True)
        if self._select_related:
            qs = qs.select_related(*self._select_related)
        if self._prefetch_related:
            qs = qs.prefetch_related(*self._prefetch_related)
        return qs

    def delete(self):
        self.get_queryset().update(deleted=timezone.now())

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True, editable=False)

    objects = ModelManager()

    class Meta:
        abstract = True

class PasswordReset(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    token = models.CharField(
        max_length=128, unique=True, default=gen_secret_key, editable=False)
    is_active = models.BooleanField(default=True)

def profile_photo_upload(instance, filename):
    prefix = 'profiles/user-%s-%s'
    return prefix % (
        slugify(instance.user.first_name),
        filename)

class Profile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile')
    photo = models.ImageField(
        blank=True, null=True, upload_to=profile_photo_upload)
    birthday = models.DateField(null=True)
    phone = models.CharField(null=True, max_length=11)
    teams = models.ManyToManyField(
        'Team',
        through='TeamAdmin'
    )

    def is_admin(self, team):
        return team in teams

    def __unicode__(self):
        return u'User: {} Profile: {}'.format(
            self.user.first_name,
            self.pk
        )

class Position(BaseModel):
    name = models.CharField(max_length=45)

    def __unicode__(self):
        return u'{}'.format(self.name)

class State(BaseModel):
    name = models.CharField(max_length=45)

    def __unicode__(self):
        return u'State: {}'.format(
            self.name
        )

class City(BaseModel):
    state = models.ForeignKey(State, related_name='cities')
    name = models.CharField(max_length=45)

    class Meta:
        verbose_name_plural = "Cities"

    def __unicode__(self):
        return u'{}'.format(self.name)

def logo_upload(instance, filename):
    prefix = 'teams/logo-%s-%s'
    return prefix % (
        slugify(instance.name),
        filename)

class Team(BaseModel):
    city = models.ForeignKey(City, related_name='teams')
    logo = models.ImageField(blank=True, null=True, upload_to=logo_upload)
    name = models.CharField(max_length=50)
    foundation = models.DateField(null=True)
    president = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return u'Team: {}'.format(
            self.name
        )

class Athlete(BaseModel):
    profile = models.ForeignKey(Profile)
    team = models.ForeignKey(Team, related_name='athletes')
    position = models.ForeignKey(Position, related_name='athletes')

    @property
    def name(self):
        return u'{} {}'.format(
            self.profile.user.first_name,
            self.profile.user.last_name
        )

    @property
    def email(self):
        return self.profile.user.email

    @property
    def phone(self):
        return self.profile.phone

    @property
    def photo(self):
        return self.profile.photo

    def __unicode__(self):
        return u'Athlete: {}'.format(
            self.profile.user.first_name
        )

class Arena(BaseModel):
    name = models.CharField(max_length=50)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __unicode__(self):
        return u'{}'.format(self.name)

class Match(BaseModel):
    arena = models.ForeignKey(Arena, related_name='matches')
    home_team = models.ForeignKey(Team, related_name='home_matches')
    visitor_team = models.ForeignKey(Team, related_name='visitor_matches')
    when = models.DateTimeField(null=False)

    class Meta:
        verbose_name_plural = 'Matches'

    def __unicode__(self):
        return u'Match: {}x{} in {}'.format(
            self.home_team.name,
            self.visitor_team.name,
            self.arena.name
        )

class StatType(BaseModel):
    name = models.CharField(max_length=50)

class MatchStat(BaseModel):
    match = models.ForeignKey(Match, related_name='stats')
    team = models.ForeignKey(Team, null=True)
    athlete = models.ForeignKey(Athlete, null=True)
    type = models.ForeignKey(StatType)

class Participation(BaseModel):
    athlete = models.ForeignKey(Athlete)
    match = models.ForeignKey(Match)
    going = models.BooleanField()
    reason_not_going = models.CharField(max_length=140)

class TeamAdmin(BaseModel):
    profile = models.ForeignKey(Profile)
    team = models.ForeignKey(Team)
