# Video Games Library API

A RESTful web service providing access to a database of over 16,000 video games. Supports full CRUD operations, advanced filtering, personalised game recommendations, and database statistics. Built using Django REST Framework with SQLite.
**Live API:** https://ZayedAlhashmi.pythonanywhere.com

## Tech Stack

- Python 3
- Django 6
- Django REST Framework
- SQLite
- drf-yasg (Swagger/ReDoc documentation)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Zayed-Alhashmi/videogames-api.git
cd videogames-api
```

### 2. Install dependencies
```bash
pip install django djangorestframework drf-yasg
```

### 3. Run database migrations
```bash
python manage.py migrate
```

### 4. Import the game data
```bash
python seed.py
```

### 5. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

The API will be available at: http://127.0.0.1:8000

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/

## Endpoints

### Games

| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/games/ | List all games (paginated, 20 per page) |
| POST | /api/games/ | Add a new game |
| GET | /api/games/\<id\>/ | Get a single game by ID |
| PUT | /api/games/\<id\>/ | Update a game by ID |
| DELETE | /api/games/\<id\>/ | Delete a game by ID |

### Reviews

| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/games/\<id\>/reviews/ | Get all reviews for a game |
| POST | /api/games/\<id\>/reviews/ | Add a review to a game |

### Special Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/recommend/ | Get personalised game recommendations |
| GET | /api/metadata/ | Get all available genres, platforms and age ratings |
| GET | /api/stats/ | Get database statistics |

## Filtering & Search

The `/api/games/` endpoint supports the following query parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| genre | Filter by genre | ?genre=Action |
| platform | Filter by platform | ?platform=PS4 |
| age_rating | Filter by age rating | ?age_rating=M |
| developer | Filter by developer | ?developer=Nintendo |
| year | Filter by release year | ?year=2006 |
| min_score | Minimum critic score | ?min_score=90 |
| max_score | Maximum critic score | ?max_score=98 |
| search | Search by title keyword | ?search=mario |
| ordering | Sort results | ?ordering=-critic_score |
| page | Page number | ?page=2 |

### Ordering options

| Value | Description |
|-------|-------------|
| critic_score | Critic score ascending |
| -critic_score | Critic score descending |
| release_year | Release year ascending |
| -release_year | Release year descending |
| title | Title A-Z |
| -title | Title Z-A |

### Example combined requests

```
GET /api/games/?genre=Action&platform=PS4
GET /api/games/?min_score=90&ordering=-critic_score
GET /api/games/?search=mario&ordering=release_year
GET /api/recommend/?genre=Role-Playing&platform=PS3
GET /api/recommend/?genre=Sports&min_score=80
```

## Recommendation Endpoint

Returns the top 10 highest rated games matching your preferences.

| Parameter | Description | Example |
|-----------|-------------|---------|
| genre | Preferred genre | ?genre=Action |
| platform | Preferred platform | ?platform=PS4 |
| age_rating | Age rating preference | ?age_rating=M |
| min_score | Minimum critic score | ?min_score=80 |

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK — request successful |
| 201 | Created — new resource created successfully |
| 400 | Bad Request — invalid data provided |
| 404 | Not Found — resource does not exist |

## Admin Panel

Access the Django admin panel at http://127.0.0.1:8000/admin/

## Dataset

This project uses the [Video Game Sales with Ratings](https://www.kaggle.com/) dataset from Kaggle, containing over 16,000 video games with critic scores, platforms, genres and age ratings.

## Author

Zayed Alhashmi — University of Leeds — COMP3011 Web Services 2025/2026
