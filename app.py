import streamlit as st
from src.recommender import TMDBRecommender

st.set_page_config(page_title="CineMatch", page_icon="🎬")

st.title("🎬 CineMatch: Movie Recommender")
st.markdown("Type a movie title and get similar movie suggestions from TMDB.")

# Initialize recommender
recommender = TMDBRecommender()

# User input
movie = st.text_input("Enter a movie title:", placeholder="e.g. Inception")

if movie:
    with st.spinner("Fetching recommendations..."):
        results = recommender.recommend(movie)
    
    st.subheader("🎥 Recommended Movies:")

    for rec in results:
        cols = st.columns([1, 3])
        with cols[0]:
            if rec["poster_path"]:
                poster_url = f"https://image.tmdb.org/t/p/w200{rec['poster_path']}"
                st.image(poster_url, width=120)
            else:
                st.write("No image")

        with cols[1]:
            st.markdown(f"### {rec['title']}")
            st.markdown(f"**Rating:** ⭐ {rec['rating']}/10")
            st.markdown(f"**Genres:** {', '.join(rec['genres'])}")
            st.markdown("---")

