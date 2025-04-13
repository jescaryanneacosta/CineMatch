import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TMDBRecommender:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        if not self.api_key:
            raise ValueError("TMDB API key not found. Make sure it's in your .env file.")
        self.base_url = "https://api.themoviedb.org/3"

    def search_movie(self, query):
        url = f"{self.base_url}/search/movie"
        params = {"api_key": self.api_key, "query": query}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None
        results = response.json().get("results", [])
        return results[0] if results else None

    def get_recommendations(self, movie_id):
        url = f"{self.base_url}/movie/{movie_id}/recommendations"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return []

        data = response.json().get("results", [])
        recommendations = []

        for movie in data:
            recommendations.append({
                "title": movie["title"],
                "poster_path": movie["poster_path"],
                "rating": movie["vote_average"],
                "genre_ids": movie["genre_ids"]
            })

        return recommendations

    def get_genre_mapping(self):
        url = f"{self.base_url}/genre/movie/list"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return {}
        genres = response.json().get("genres", [])
        return {genre["id"]: genre["name"] for genre in genres}

    def recommend(self, movie_title, genre_filter=None):
        movie = self.search_movie(movie_title)
        if not movie:
            return ["❌ Movie not found."]
        raw_recs = self.get_recommendations(movie["id"])
        genres = self.get_genre_mapping()

        filtered_recs = []
        for rec in raw_recs:
            rec["genres"] = [genres.get(genre_id, "") for genre_id in rec["genre_ids"]]
            if genre_filter is None or genre_filter in rec["genres"]:
                filtered_recs.append(rec)

        return filtered_recs
