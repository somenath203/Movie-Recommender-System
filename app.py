import streamlit as st 
import pandas as pd 
import pickle
import requests
from dotenv import load_dotenv
import os

load_dotenv()


movies_dataset_dictionary = pickle.load(open('cleaned_movies_dataset_dictionary.pkl', 'rb'))

similarity_matrix = pickle.load(open('./similarity_matrix.pkl', 'rb'))

movie_db_api_key=os.getenv('THE_MOVIE_DB_API_KEY')


movie_dataset = pd.DataFrame(movies_dataset_dictionary)


def fetch_poster_of_movie(id_of_the_movie):

    response = requests.get(f'https://api.themoviedb.org/3/movie/{id_of_the_movie}?api_key={movie_db_api_key}')
    
    data = response.json()
    
    poster_path = data.get('poster_path', None)
    
    if poster_path:

        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

        return full_path
    
    else:

        return None


def recommend_top_5_similar_movies_for_the_given_movie_input(movie_name):

    recommended_movies = []

    poster_of_recommended_movies = []
    
    index_of_the_movie = movie_dataset[movie_dataset['title'] == movie_name].index[0]
    
    all_distances = similarity_matrix[index_of_the_movie]
    
    top_five_movies = sorted(list(enumerate(all_distances)), reverse=True, key=lambda x:x[1])[1:6] 

    for i in top_five_movies:

        recommended_movies.append(movie_dataset.iloc[i[0]].title)

        poster_of_recommended_movies.append(fetch_poster_of_movie(movie_dataset.iloc[i[0]].movie_id))

    
    return recommended_movies, poster_of_recommended_movies


st.set_page_config(page_title='Movie Recommender System')


st.markdown("<h1 style='text-align: center;'>Movie Recommendation System</h1>", unsafe_allow_html=True)


selected_movie_name = st.selectbox(
    'Select or type a movie name to get recommendations for the top 5 similar movies',
    movie_dataset['title'].values
)

if st.button('Recommend top 5 Movies'):

    st.markdown('<br>', unsafe_allow_html=True)
    
    st.markdown(f'<h3>Selected Movie Name: {selected_movie_name}</h3>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    st.markdown(f'<h5>Top 5 recommended movies that are similar to "{selected_movie_name}" are:</h5>', unsafe_allow_html=True)

    name_of_top_five_recommendation, poster_of_top_five_recommended_movies = recommend_top_5_similar_movies_for_the_given_movie_input(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        
        if poster_of_top_five_recommended_movies[0]:
            st.image(poster_of_top_five_recommended_movies[0])
        else:
            st.write('Poster not available')

        st.markdown(f"<h5 style='text-align: center;'>{name_of_top_five_recommendation[0]}</h5>", unsafe_allow_html=True)

    with col2:

        if poster_of_top_five_recommended_movies[1]:
            st.image(poster_of_top_five_recommended_movies[1])
        else:
            st.write('Poster not available')
            
        st.markdown(f"<h5 style='text-align: center;'>{name_of_top_five_recommendation[1]}</h5>", unsafe_allow_html=True)

    with col3:

        if poster_of_top_five_recommended_movies[2]:
            st.image(poster_of_top_five_recommended_movies[2])
        else:
            st.write('Poster not available')
            
        st.markdown(f"<h5 style='text-align: center;'>{name_of_top_five_recommendation[2]}</h5>", unsafe_allow_html=True)

    with col4:

        if poster_of_top_five_recommended_movies[3]:
            st.image(poster_of_top_five_recommended_movies[3])
        else:
            st.write('Poster not available')
            
        st.markdown(f"<h5 style='text-align: center;'>{name_of_top_five_recommendation[3]}</h5>", unsafe_allow_html=True)

    with col5:

        if poster_of_top_five_recommended_movies[4]:
            st.image(poster_of_top_five_recommended_movies[4])
        else:
            st.write('Poster not available')
            
        st.markdown(f"<h5 style='text-align: center;'>{name_of_top_five_recommendation[4]}</h5>", unsafe_allow_html=True)