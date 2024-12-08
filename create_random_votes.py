# to launch this file enter
# python manage.py shell < create_random_votes.py

import pandas as pd
import numpy as np
import random
from app.models import Game, Votes, get_finalists
from django.db import transaction


def dynamic_weights():
    negative_weight = random.uniform(0.45, 0.5)
    positive_weight = random.uniform(0.4, 0.5)
    zero_weight = 1.0 - (negative_weight + positive_weight)
    return [negative_weight, positive_weight, zero_weight]


df = pd.DataFrame({
    'user_id': [],
    'value': [],
    'game_id_id': [],
})

game_ids = list(Game.objects.values_list('id', flat=True))

num_users = 10
vote_values = [-1, 1, 0]

data = []
user_ids = np.random.randint(10**17, 10**18, size=num_users, dtype=np.int64)
for user_id in user_ids:
    for game_id in game_ids:
        vote_value = random.choices(vote_values, weights=dynamic_weights())[0]
        if vote_value != 0:
            data.append({
                'user_id': user_id,
                'value': vote_value,
                'game_id_id': game_id,
            })

df = pd.DataFrame(data)

print(df)

votes_to_create = [
    Votes(
        user_id=int(row['user_id']),
        game_id_id=row['game_id_id'],
        stage=1,
        value=row['value']
    )
    for _, row in df.iterrows()
]

with transaction.atomic():
    Votes.objects.all().delete()
    Votes.objects.bulk_create(votes_to_create, batch_size=1000)

print(f"Inserted {len(df)} votes for first stage.")

data = []
best_games, worst_games = get_finalists()
for user_id in user_ids:
    best_game_id = random.choice(best_games).id
    worst_game_id = random.choice(worst_games).id
    data.append({
        'user_id': user_id,
        'value': 1,
        'game_id_id': best_game_id,
    })
    data.append({
        'user_id': user_id,
        'value': -1,
        'game_id_id': worst_game_id,
    })

df = pd.DataFrame(data)

print(df)

votes_to_create = [
    Votes(
        user_id=int(row['user_id']),
        game_id_id=row['game_id_id'],
        stage=2,
        value=row['value']
    )
    for _, row in df.iterrows()
]

with transaction.atomic():
    Votes.objects.bulk_create(votes_to_create, batch_size=1000)

print(f"Inserted {len(df)} votes for second stage.")
