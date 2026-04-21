from fastapi import FastAPI
from model import get_recommendations
import requests

app = FastAPI()


OMDB_API_KEY = "2ff87d5a" 


def get_poster(movie_name):
    if not OMDB_API_KEY:
        return None  
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_name}"
        data = requests.get(url, timeout=5).json()

        if data.get("Response") == "True":
            poster = data.get("Poster", "")
            if poster and poster != "N/A":
                return poster
    except:
        pass

    
  
    return "https://placehold.co/300x450/1a1a2e/ffffff?text=No+Poster"


@app.get("/")
def home():
    return {"message": "Movie Recommendation API (OMDb)"}


@app.get("/recommend/{movie_name}")
def recommend(movie_name: str):
    results = get_recommendations(movie_name)

    for movie in results:
        if isinstance(movie, dict):  
          movie["poster"] = get_poster(movie["title"])

    return {"recommendations": results}