# Restaurant Review

A web application for submitting restaurant reviews, analyzing sentiment, and displaying a real-time leaderboard of top restaurants.

## Features

- Submit reviews with sentiment analysis ([helpers/nlp.py](helpers/nlp.py), [`helpers.determine_sentiment`](helpers/nlp.py))
- View all restaurants and their average sentiment ([app.py](app.py))
- Real-time leaderboard via WebSocket ([ws.py](ws.py))
- CORS enabled for frontend integration

## **Quickstart**

1. Create a `.env` with the following variables:

   * `DB_HOST_URL`

   * `DB_PORT`

   * `DB_USERNAME`

   * `DB_PASSWORD`

   * `DB_NAME`

   * `REDIS_HOST_URL`

   * `REDIS_PORT`

   * `REDIS_USERNAME`

   * `REDIS_PASSWORD`

2. Install dependencies:

   * `pip install -r requirements.txt`

3. Ensure VADER lexicon is available:

   * `python -m nltk.downloader vader_lexicon`

## **Run**

* API: `python app.py` ([http://127.0.0.1:5000](http://127.0.0.1:5000))

* WebSocket server: `python ws.py` (ws://localhost:8080)

## **Endpoints**

* `GET /restaurants` — list restaurants with `id`, `name`, `avg_sentiment`, `total_reviews`

`POST /post-review` — JSON body:

 `{ "name": "string", "email": "string", "review": "string", "restaurant_id": int }`

