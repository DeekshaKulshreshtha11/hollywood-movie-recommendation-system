import streamlit as st
import pickle
import pandas as pd
import requests


TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


similarity = pickle.load(open('similarity.pkl', 'rb'))

def get_recommendations(movie_name): 

    index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:6]

    recommendations = []
    poster_path = []

    for movie_id in movies_list: 
        recommendations.append(movies.iloc[movie_id[0]].title)
        poster_path.append(fetch_poster(movies.iloc[movie_id[0]].movie_id))
    return recommendations, poster_path


def fetch_poster(movie_id): 

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()

    return("https://image.tmdb.org/t/p/w500/" + data['poster_path'])
       


st.title("Movie Recommendation System")

movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
movies_list = movies_list['title'].values()

selected_movie_name = st.selectbox("Please, select a movie name", movies_list)

if st.button("Recommend"): 

    movie_names, movie_posters = get_recommendations(selected_movie_name) # contains a dict of generic index and movie names

    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for iter in range(0,5): 
        with cols[iter]: 
            st.text(movie_names[iter])
            st.image(movie_posters[iter])