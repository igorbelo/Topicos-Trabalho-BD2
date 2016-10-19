from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from core.models import (Profile, Match, Team,\
                         State, City, Position, Athlete,\
                         StatType, MatchStat, Arena)
from random import randint
import math
import uuid
from tqdm import tqdm
from datetime import datetime, timedelta
from random import randint

NUMBER_OF_STATES = 26
NUMBER_OF_CITIES = 70
NUMBER_OF_TEAMS = 10000
NUMBER_OF_ATHLETES_IN_TEAM = 11
NUMBER_OF_ATHLETES = NUMBER_OF_TEAMS * NUMBER_OF_ATHLETES_IN_TEAM
NUMBER_OF_ARENAS = 20
NUMBER_OF_MATCHES = 2000000
POSITIONS_LIST = (
    'Goleiro','Lateral','Zagueiro','Volante','Meio-campo','Atacante'
)
fake = Faker()

def random_date(start, end):
    return start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))

class Command(BaseCommand):
    def handle(self, *args, **options):
        # stat types
        STAT_TYPES_LIST = (
            'goal','own-goal','yellow-card','red-card'
        )
        stat_types = []
        for stat_name in STAT_TYPES_LIST:
            stat_types.append(
                StatType.objects.create(
                    name = stat_name
                )
            )
        # positions
        self.positions = []
        for position_name in POSITIONS_LIST:
            self.positions.append(
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
        print "criando times..."
        self.teams = []
        for _ in tqdm(range(0,NUMBER_OF_TEAMS)):
            team_city = cities[
                randint(0,NUMBER_OF_CITIES-1)
            ]
            team_name = fake.company()
            self.teams.append(
                Team(
                    city = team_city,
                    name = team_name
                )
            )
        Team.objects.bulk_create(self.teams)
        # athletes
        print "criando atletas..."
        users = []
        profiles = []
        athletes = []

        for i in tqdm(range(NUMBER_OF_ATHLETES)):
            first_name = "FakeFirstName"
            last_name = "FakeLastName"
            email = str(uuid.uuid1())+"@varzeapro.com"
            user = User(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = email
            )
            users.append(user)
            d1 = datetime.strptime('1/1/1970', '%m/%d/%Y')
            d2 = datetime.strptime('10/1/1998', '%m/%d/%Y')
            when = random_date(d1, d2)
            profile = Profile(
                user_id = i+1,
                birthday = when
            )
            profiles.append(profile)
            team_index = int(
                math.floor(i/NUMBER_OF_ATHLETES_IN_TEAM)
            )
            team = self.teams[team_index]
            position = self.positions[
                randint(0,len(POSITIONS_LIST)-1)
            ]
            athlete = Athlete(
                profile_id = i+1,
                team = team,
                position = position
            )
            athletes.append(athlete)

        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)
        Athlete.objects.bulk_create(athletes)
        # arenas
        arenas = []
        for i in range(0,NUMBER_OF_ARENAS):
            arenas.append(
                Arena.objects.create(
                    name = fake.street_name()
                )
            )
        # matches
        print "criando partidas..."
        matches = []
        for i in tqdm(range(0,NUMBER_OF_MATCHES)):
            team_index = int(
                math.floor(i/200)
            )
            random_team_index = randint(0,NUMBER_OF_TEAMS-1)
            if random_team_index == team_index:
                if random_team_index == 0:
                    random_team_index += 1
                else:
                    random_team_index -= 1

            if i % 2 == 0:
                home_team = self.teams[team_index]
                visitor_team = self.teams[random_team_index]
            else:
                home_team = self.teams[random_team_index]
                visitor_team = self.teams[team_index]

            arena = arenas[randint(0,NUMBER_OF_ARENAS-1)]
            d1 = datetime.strptime('1/1/2010 7:00 AM', '%m/%d/%Y %I:%M %p')
            d2 = datetime.strptime('10/1/2016 4:00 PM', '%m/%d/%Y %I:%M %p')
            when = random_date(d1, d2)
            matches.append(
                Match(
                    arena = arena,
                    home_team = home_team,
                    visitor_team = visitor_team,
                    when = when
                )
            )
        Match.objects.bulk_create(matches)
