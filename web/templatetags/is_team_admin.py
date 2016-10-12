from django.template import Library

register = Library()

def is_team_admin(profile, team):
    return team in profile.teams

register.filter('is_team_admin', is_team_admin)
