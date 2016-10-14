from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from core.models import Profile, Match, Team, State, City, Position, Athlete
from random import randint
import math

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        NUMBER_OF_STATES = 26
        NUMBER_OF_CITIES = 70
        NUMBER_OF_TEAMS = 100

        # positions
        positions = []
        POSITIONS_LIST = (
            'Goleiro','Lateral','Zagueiro','Volante','Meio-campo','Atacante'
        )
        for position_name in POSITIONS_LIST:
            positions.append(
                Position.objects.create(
                    name = position_name
                )
            )
        # states
        states = []
        for _ in range(0,NUMBER_OF_STATES):
            state_name = fake.state()
            states.append(
                State.objects.create(
                    name = state_name
                )
            )
        # cities
        cities = []
        for _ in range(0,NUMBER_OF_CITIES):
            city_name = fake.city()
            cities.append(
                City.objects.create(
                    name = city_name,
                    state = states[
                        randint(0,NUMBER_OF_STATES-1)
                    ]
                )
            )
        # teams
        teams = []
        for _ in range(0,NUMBER_OF_TEAMS):
            team_city = cities[
                randint(0,NUMBER_OF_CITIES-1)
            ]
            team_name = fake.company()
            teams.append(
                Team.objects.create(
                    city = team_city,
                    name = team_name
                )
            )
        #athletes
        for i in range(0,1100):
            first_name =  fake.first_name()
            last_name =  fake.last_name()
            email = fake.ipv4()+fake.safe_email()
            user = User.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = email
            )
            profile = Profile.objects.create(
                user = user,
                birthday = fake.profile()['birthdate']
            )
            team_index = int(
                math.floor(i/11)
            )
            team = teams[team_index]
            position = positions[
                randint(0,len(POSITIONS_LIST)-1)
            ]
            Athlete.objects.create(
                profile = profile,
                team = team,
                position = position
            )
