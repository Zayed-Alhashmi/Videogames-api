# Video Games Library API

A RESTful web service built with Django REST Framework, giving programmatic access to a database of over 16,700 video games. Supports full CRUD, filtering, search, personalised recommendations and statistics.

**Live:** https://ZayedAlhashmi.pythonanywhere.com

---

## Tech Stack

- Python 3 · Django 6 · Django REST Framework
- SQLite
- drf-yasg (Swagger UI + ReDoc)

---

## Setup

```bash
git clone https://github.com/Zayed-Alhashmi/videogames-api.git
cd videogames-api
pip install django djangorestframework drf-yasg
python manage.py migrate
```

Place `Video_Games_Sales_as_at_22_Dec_2016.csv` in the project root, then:

```bash
python seed.py          # imports 16,717 games
python seed_reviews.py  # adds 25 sample reviews (optional)
python manage.py createsuperuser  # optional
python manage.py runserver
```

- Frontend dashboard: http://127.0.0.1:8000
- API root: http://127.0.0.1:8000/api/

---

## Frontend

The root URL `/` serves a visual dashboard where you can browse and filter games, get recommendations, view statistics, add new games, and read reviews — all talking to the API in real time.

---

## API Documentation

| | Local | Live |
|--|--|--|
| Swagger UI | http://127.0.0.1:8000/swagger/ | https://ZayedAlhashmi.pythonanywhere.com/swagger/ |
| ReDoc | http://127.0.0.1:8000/redoc/ | https://ZayedAlhashmi.pythonanywhere.com/redoc/ |

---

## Endpoints

### Games

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/games/` | List all games — paginated, 20 per page |
| POST | `/api/games/` | Create a new game |
| GET | `/api/games/<id>/` | Get a single game with its reviews |
| PUT | `/api/games/<id>/` | Update a game |
| DELETE | `/api/games/<id>/` | Delete a game and its reviews |

### Reviews

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/games/<id>/reviews/` | List reviews for a game |
| POST | `/api/games/<id>/reviews/` | Add a review |

### Other

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/recommend/` | Top 10 games matching your preferences |
| GET | `/api/metadata/` | All valid genres, platforms and age ratings |
| GET | `/api/stats/` | Database statistics |

---

## Filtering

`/api/games/` accepts the following query parameters:

| Parameter | Example |
|-----------|---------|
| `genre` | `?genre=Action` |
| `platform` | `?platform=PS4` |
| `age_rating` | `?age_rating=M` |
| `developer` | `?developer=Nintendo` |
| `year` | `?year=2006` |
| `min_score` | `?min_score=90` |
| `max_score` | `?max_score=98` |
| `search` | `?search=mario` |
| `ordering` | `?ordering=-critic_score` |
| `page` | `?page=2` |

Ordering values: `critic_score`, `-critic_score`, `release_year`, `-release_year`, `title`, `-title`

```
GET /api/games/?genre=Action&platform=PS4
GET /api/games/?min_score=90&ordering=-critic_score
GET /api/recommend/?genre=Role-Playing&min_score=85
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |

---

## Admin

- Local: http://127.0.0.1:8000/admin/
- Live: https://ZayedAlhashmi.pythonanywhere.com/admin/

---

## Dataset

[Video Game Sales with Ratings](https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings) — Kaggle. 16,700+ games with critic scores, platforms, genres and age ratings.

---

## Author

Zayed Alhashmi