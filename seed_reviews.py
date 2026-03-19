import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from games.models import Game, Review

# Removes any existing reviews before inserting the sample data
Review.objects.all().delete()
print("Cleared existing reviews...")

# Each entry is a tuple of (game_id, reviewer_name, rating, comment)
reviews = [
    (1, "JohnGamer92", 8, "Amazing party game, perfect for family gatherings!"),
    (2, "RetroKing", 9, "A true classic. Every gamer should play this at least once."),
    (3, "SpeedRunner_X", 10, "Pure perfection. One of the best racing games ever made."),
    (4, "NintendoFan", 7, "Solid game but gets repetitive after a while."),
    (5, "GamingPro2000", 9, "Incredible level design and tight controls throughout."),
    (6, "CasualPlayer", 6, "Fun for a few hours but lacks depth for serious players."),
    (7, "Zayed_Reviews", 10, "Absolutely brilliant. Changed how I think about gaming."),
    (8, "PixelHunter", 8, "Great graphics for its time and genuinely fun gameplay."),
    (9, "GameCritic_UK", 7, "Good but slightly overrated. Still worth playing though."),
    (10, "NightOwlGamer", 9, "Stayed up all night playing this. Completely addictive."),
    (11, "SarahPlays", 10, "The story is breathtaking. Emotionally unforgettable."),
    (12, "TurboGamer", 8, "Fast paced and exciting from start to finish."),
    (13, "OldSchoolAce", 9, "Reminds me why I fell in love with gaming in the first place."),
    (14, "IndieSpirit", 7, "Creative and unique but the controls take getting used to."),
    (15, "ProController", 10, "Flawless execution. A masterpiece in game design."),
    (16, "LevelUpLara", 8, "Challenging but rewarding. Every victory feels earned."),
    (17, "DigitalDave", 6, "Decent game but nothing particularly special about it."),
    (18, "GameVaultMike", 9, "One of the greatest games of its generation without doubt."),
    (19, "ScreenshotQueen", 8, "Visually stunning and the soundtrack is incredible."),
    (20, "PlatformKing", 10, "Perfect platforming mechanics. Smooth and satisfying to play."),
    (21, "RPGAdventurer", 9, "Deep lore and engaging characters kept me hooked for weeks."),
    (22, "FPSFanatic", 7, "Great shooter mechanics but the story is a bit thin."),
    (23, "CoopPlayer", 8, "Even better with friends. A fantastic multiplayer experience."),
    (24, "AchievementHunter", 9, "Loaded with content. Easily 100 hours of entertainment."),
    (25, "FinalBossGamer", 10, "This game set the standard for everything that followed it."),
]

added = 0
# Loops through each review entry, finds the matching game and saves the review to the database
for game_id, reviewer, rating, comment in reviews:
    try:
        game = Game.objects.get(pk=game_id)
        Review.objects.create(
            game=game,
            reviewer_name=reviewer,
            rating=rating,
            comment=comment
        )
        added += 1
        print(f"Added review for: {game.title}")
    except Game.DoesNotExist:
        print(f"Game ID {game_id} not found, skipping...")

print(f"\nDone! Added {added} reviews.")
