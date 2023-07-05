import streamlit as st
import time
import pandas as pd
import torch
import numpy as np
from Recommender import *
import streamlit.components.v1 as com
import requests


st.set_page_config(page_title="movie recommeder", page_icon='📽')


## css designing code
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image : url(https://wallpapercave.com/wp/wp1945939.jpg);
background-size : cover;
}

[data-testid = "stHeader"] {
background-color: rgba(0, 0, 0, 0);
}

[data-testid = "stVerticalBlock"]
{
    background-color: white;
    border-color: red;
    border-width: 100px;
}


button > div[data-testid = "stMarkdownContainer"]
{
    width : 650px;
    color: black;
}

</style>
"""

# loading datasets
df = pd.read_csv("cleaned.csv")
ratings = pd.read_csv("ratings_small.csv") # path to ratings_small dataset
links = pd.read_csv("links.csv")

#limitting ratings
movieIds = links['movieId'].unique()
ratings = ratings[ratings['movieId'].isin(movieIds)]
movies = ratings["movieId"].unique()

titles = df['title'].tolist()
final = []

def add_selectbox():
    st.selectbox("New Selectbox", titles)


st.markdown(page_bg_img, unsafe_allow_html=True)
with open("style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)
st.markdown("<h1 style ='text-align: center;'>Movie Recommender</h1>", unsafe_allow_html=True)

# main form------------------------------------------------------------
with st.form('my_form'):
    st.markdown("""
    <style>
    .st-dd {
        top: 35px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    com.iframe("https://embed.lottiefiles.com/animation/1961")
    multi = st.multiselect('Select 3 or more movies', titles)

#when user presses recommend button---------------------
    def recommende():
        lenof = multi.__len__()
        if lenof < 3:
            st.warning("Please select 3 or more movies")
        else:
            st.markdown("select a rating from 0 to 10 for each")

            for title in multi:
                temp = []
                
                # getting movie id from input title
                tmdb_id = df.loc[df['title'] == title, 'id'].iloc[0]
                movie_id = links.loc[links['tmdbId'] == tmdb_id, 'movieId'].iloc[0]
                
                temp.append(movie_id)
                temp.append(10)

                final.append(temp)


            # getting top 10 recommendations
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model = torch.load('RecSys.pth', map_location=device) # path to the pretrained model 
            st.markdown(final)
            top_10_id = get_top_rated_movies(final, model, movies, device, 10)

            st.markdown(top_10_id)

            # showing top 10 information for user
            for movie_id in top_10_id:
                tmdb_id = links.loc[links['movieId'] == movie_id, 'tmdbId'].iloc[0]

                url = "https://api.themoviedb.org/3/movie/{}?api_key=73e889cc3c939a8d7a8ae0e57794a4bc".format(tmdb_id)
                response = requests.get(url)
                response = response.json()
                poster = response['poster_path']
                image_data = "https://image.tmdb.org/t/p/w500" + poster

                centered_header = f'<h1 style="text-align: center;">{df.loc[df["id"] == tmdb_id, "title"].iloc[0]}</h1>'
                st.markdown(centered_header, unsafe_allow_html=True)
                st.markdown(
                    f'<div style="display: flex; justify-content: center;">'
                    f'<img src="{image_data}" style="width: 300px;">'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.markdown("")
                with st.expander("Click to see the overview"):
                    st.markdown(df[df["id"] == tmdb_id]["overview"].iloc[0])
        

    if st.form_submit_button('Recommend'):
        recommende()

    pass

st.markdown('</div>', unsafe_allow_html=True)