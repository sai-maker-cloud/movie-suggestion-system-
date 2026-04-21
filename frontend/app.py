import streamlit as st
import requests

API_URL = "https://movie-suggestion-system-ok0f.onrender.com"

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommendation System")
st.write("Search a movie and get similar recommendations")


movie_name = st.text_input("Enter movie name")

if st.button("Recommend"):
    if movie_name:
        response = requests.get(API_URL + movie_name)

        if response.status_code == 200:
            data = response.json()["recommendations"]

            if not data:
                st.error("Movie not found!")
            else:
                st.subheader("Top Recommendations")

                cols = st.columns(5)

                for i, movie in enumerate(data):
                    with cols[i % 5]:
                        if movie["poster"]:
                            st.image(movie["poster"])
                        st.write(f"**{movie['title']}**")
                        st.caption(f"Similarity: {movie['score']}")
        else:
            st.error("API Error")
    else:
        st.warning("Please enter a movie name")