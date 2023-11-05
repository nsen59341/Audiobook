import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyForAudios.settings")

import django
django.setup()

from faker import Faker, factory
from CrazyAudios.models import *
from model_bakery.recipe import Recipe, foreign_key

fake = Faker()

for k in range(10):
    audio = Recipe(Audio,
                   name=fake.name(),
                   upload_date=fake.future_datetime(end_date="+20d", tzinfo=None),)


    audio.make()