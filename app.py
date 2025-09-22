import mysql.connector
from flask import Flask, request
from helpers import determine_sentiment
import redis
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

r = redis.Redis(
    host=os.getenv("REDIS_HOST_URL"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True,
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
)

app = Flask(__name__)
CORS(app)

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST_URL"),  
    port=os.getenv("DB_PORT"),          
    user=os.getenv("DB_USERNAME"),        
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME") 
)

cursor = conn.cursor()

@app.route("/", methods=["GET"])
def home():
    cursor.execute("SELECT * FROM restaurants") 
    restaurants = cursor.fetchall()
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_list.append({
            "id": restaurant[0],
            "name": restaurant[1],
            "avg_sentiment": float(restaurant[2]) if restaurant[2] is not None else None,
            "total_reviews": restaurant[3]
        })
    return {"restaurants": restaurant_list}, 200

@app.route("/post-review", methods=["POST"])
def handle_review():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    review = data.get("review")
    restaurant_id = data.get("restaurant_id")

    if not (name and email and review and restaurant_id):
        return {"error": "All fields are required"}, 400
    
    sentiment_score = determine_sentiment(review)

    try: 
        cursor.execute("INSERT INTO users (name, email, review) VALUES (%s, %s, %s)", (name, email, review))
        user_id = cursor.lastrowid
        cursor.execute("INSERT INTO reviews (restaurant_id, user_id, review_text, sentiment_score) VALUES (%s, %s, %s, %s)", (restaurant_id, user_id, review, sentiment_score, ))
        cursor.execute("SELECT AVG(sentiment_score) FROM reviews WHERE restaurant_id = %s", (restaurant_id, ))
        avg_sentiment = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM reviews WHERE restaurant_id = %s",
            (restaurant_id,)
        )
        total_reviews = cursor.fetchone()[0]
        cursor.execute("UPDATE restaurants SET avg_sentiment = %s WHERE id = %s", (avg_sentiment, restaurant_id, ))
        cursor.execute("UPDATE restaurants SET total_reviews = %s WHERE id = %s", (total_reviews, restaurant_id, ))
        conn.commit()

        r.zadd("restaurants", {str(restaurant_id): float(avg_sentiment) if avg_sentiment is not None else 0})
        
        return {"msg": "Entry added", "id": user_id}, 201
    except:
        return {"msg": "Something went wrong"}, 500
    
@app.route("/restaurants", methods=["GET"])    
def fetch_restaurant():
    cursor.execute("SELECT * FROM restaurants")
    restaurant = cursor.fetchall()
    if not restaurant:
        return {"error": "No restaurants found"}, 404
    restaurant_list = []
    for res in restaurant:
        restaurant_list.append({
            "id": res[0],
            "name": res[1],
            "avg_sentiment": float(res[2]) if res[2] is not None else None,
            "total_reviews": res[3]
        })
    return {"restaurants": restaurant_list}, 200

if __name__ == "__main__":
    app.run(debug=True)