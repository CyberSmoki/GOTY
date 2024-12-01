# to launch this file enter
# python manage.py shell < import_games.py

import pandas as pd
from app.models import Game

file = "gamelist.csv"
df = pd.read_csv(file)

for index, row in df.iterrows():
    try:
        name = row['name']
        release_date = pd.to_datetime(row['release_date']).date()

        Game.objects.update_or_create(
            name=row['name'],
            defaults={
                'developer': row['developer'],
                'genre': row['genre'],
                'release_date': release_date,
                'image_url': row['image_url']
            }
        )
        print(f"Successfully imported: {name}")
    except Exception as e:
        print(f"Error importing {name}: {e}")
