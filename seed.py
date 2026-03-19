import os
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from games.models import Game

CSV_FILE = 'Video_Games_Sales_as_at_22_Dec_2016.csv'

# Clears all existing games then reads the CSV file and imports each valid row into the database
def run():
    print("Clearing existing games...")
    Game.objects.all().delete()

    print("Importing games from CSV...")
    imported = 0
    skipped = 0

    with open(CSV_FILE, encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            platform = row.get('Platform', '').strip()
            genre = row.get('Genre', '').strip()

            # Skips any row that is missing a name, platform or genre
            if not name or not platform or not genre:
                skipped += 1
                continue

            try:
                year = int(float(row.get('Year_of_Release', '') or 0))
                year = year if year > 1970 else None
            except:
                year = None

            developer = row.get('Developer', '').strip() or None

            try:
                critic_score = float(row.get('Critic_Score', '') or 0)
                critic_score = critic_score if critic_score > 0 else None
            except:
                critic_score = None

            age_rating = row.get('Rating', '').strip() or None

            Game.objects.create(
                title=name,
                platform=platform,
                genre=genre,
                release_year=year,
                developer=developer,
                critic_score=critic_score,
                age_rating=age_rating
            )
            imported += 1

    print(f"Done! Imported: {imported} games | Skipped: {skipped} rows")

if __name__ == '__main__':
    run()
