import streamlit as st
import pickle
import requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import os


api_key = st.secrets["TMDB_API_KEY"]


# ------------------ FETCH POSTER ------------------ #

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching movie ID {movie_id}: {response.status_code}")
        return "https://via.placeholder.com/500x750?text=No+Poster"
    
    data = response.json()
    poster_path = data.get('poster_path')

    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# ------------------ RECOMMENDER ------------------ #

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# ------------------ LOAD DATA ------------------ #

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values
cv = pickle.load(open('vectorizer.pkl','rb'))
vectors = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vectors)

# ------------------ STREAMLIT UI ------------------ #
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px;'>Get 5 similar movies instantly</p>", unsafe_allow_html=True)
st.markdown("---")

selected_moviename = st.selectbox("🔍 Search a movie you like:", movies_list)

if st.button("✨ Recommend"):
    names, posters = recommend(selected_moviename)
    st.markdown("### 🎯 Top Recommendations:")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"<p style='font-size:14px; font-weight:bold; text-align:center;'>{names[0]}</p>", unsafe_allow_html=True)
        st.image(posters[0])


    with col2:
        st.markdown(f"<p style='font-size:14px; font-weight:bold; text-align:center;'>{names[1]}</p>", unsafe_allow_html=True)

        st.image(posters[1])

    with col3:
        st.markdown(f"<p style='font-size:14px; font-weight:bold; text-align:center;'>{names[2]}</p>", unsafe_allow_html=True)

        st.image(posters[2])

    with col4:
        st.markdown(f"<p style='font-size:14px; font-weight:bold; text-align:center;'>{names[3]}</p>", unsafe_allow_html=True)

        st.image(posters[3])

    with col5:
        st.markdown(f"<p style='font-size:14px; font-weight:bold; text-align:center;'>{names[4]}</p>", unsafe_allow_html=True)

        st.image(posters[4])