import streamlit as st
import requests
import os
import pandas as pd

os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

def send_request_top10():
    response = requests.get("http://localhost:8000/movie/top10")
    return response.json()

def send_request_top10genre(genre):
    response = requests.get(f"http://localhost:8000/movie/top10genre?genre={genre}")
    return response.json()

def send_request_top10rec(title):
    response = requests.get(f"http://localhost:8000/movie/top10rec?title={title}")
    return response.json()

def send_request_allGenres():
    response = requests.get(f"http://localhost:8000/genre")
    return response.json()

def send_request_userContent(idUser):
    response = requests.get(f"http://localhost:8000/movie/userContent?idUser={idUser}")
    return response.json()


# Add the About window
with st.expander("О программе"):
    st.write("""
    Эта программа отображает три вида рекомендательных систем

    - Топ 10 популярных фильмов: выводит информацию о 10 наиболее высокооценненых фильмах.
    - Топ 10 фильмов по жанру: введите жанр и программа выдаст информацию о 10 наиболее высокооценненых фильмах в данном жанре.
    - Топ 10 фильмов по контенту: введите название фильма и программа выдаст информацию о 10 похожих произведений.
    - Топ 10 фильмов по контенту пользователя: введите идентификатор пользователя и программа выдаст информацию о 10 произведениях со схожими интересами у других пользователей.
    """)

st.title("Рекомендательная система")

with st.expander("Топ 10 популярных фильмов"):
    top10_data = send_request_top10()
    top10_df = pd.DataFrame(top10_data)
    st.bar_chart(top10_df.set_index('title')['w_score'])

with st.expander("Топ 10 фильмов по жанру"):
    options = send_request_allGenres()
    genre = st.selectbox('Выберите жанр', options)
    if genre:
        top10genre_data = send_request_top10genre(genre)
        top10genre_df = pd.DataFrame(top10genre_data)
        st.bar_chart(top10genre_df.set_index('title')['w_score'])

with st.expander("Топ 10 фильмов по контенту"):
    title = st.text_input("Введите название")
    if title:
        top10rec_data = send_request_top10rec(title)
        top10rec_df = pd.DataFrame(top10rec_data)
        st.write(top10rec_df)

with st.expander("Топ 10 фильмов по контенту пользователей"):
    title = st.text_input("Введите идентификатор")
    if title:
        top10user_data = send_request_userContent(title)
        top10user_df = pd.DataFrame(top10user_data)
        st.write(top10user_df)
