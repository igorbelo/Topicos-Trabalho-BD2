from django.contrib import admin

from .models import (
    Profile,
    Position,
    State,
    City,
    Team,
    Athlete,
    Arena,
    Match
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    pass

@admin.register(Arena)
class ArenaAdmin(admin.ModelAdmin):
    pass

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass
