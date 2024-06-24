import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=64260b9462a7b1ab55ed019e24d26699'.format(movie_id))
    data=response.json()
    return  "https://image.tmdb.org/t/p/w500" + data['poster_path']

# Load the movie list and similarity matrix
movie_list_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Ensure movie_list is defined correctly
movie_titles = movie_list_df['title'].values

def recommend(movie):
    movie_index = movie_list_df[movie_list_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster=[]
    for i in movie_list:
        movie_id=movie_list_df.iloc[i[0]].id
        recommended_movies.append(movie_list_df.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster
# Streamlit UI
st.title('Movie Recommendation System')

option = st.selectbox(
    "Choose Movie:",
    movie_titles)

if st.button('Recommend'):
    names,posters = recommend(option)
    st.write("Recommended Movies:")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])