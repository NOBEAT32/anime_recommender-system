import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="Anime Recommender", layout="centered")

#  Data from mlmodel
anime_df = pickle.load(open('animes.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

#  CSS
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://wallpapercave.com/wp/wp12662319.jpg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }
        .title {
            font-size: 48px;
            color: #ff4b4b;
            text-align: center;
            margin-bottom: 10px;
            text-shadow: 2px 2px 5px #000;
        }
        .recommendation-card {
            text-align: center;
            padding: 10px;
        }
        .recommendation-card img {
            transition: transform 0.3s ease;
            border-radius: 10px;
            max-width: 100%;
            height: auto;
        }
        .recommendation-card img:hover {
            transform: translateY(-10px) scale(1.05);
            box-shadow: 0 8px 20px rgba(255, 255, 255, 0.2);
        }
        .stSelectbox > div {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

#  Title
st.markdown('<div class="title"> Anime Recommender 🎌</div>', unsafe_allow_html=True)

# 🔍 Recommend Function
def recommend(anime_name):
    anime_index = anime_df[anime_df['title_english'] == anime_name].index[0]
    distances = similarity[anime_index]
    anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_anime = []
    for i in anime_list:
        title = anime_df.iloc[i[0]]['title_english']
        image_url = anime_df.iloc[i[0]]['image_url']
        recommended_anime.append((title, image_url))
    return recommended_anime

selected_anime = st.selectbox(' Choose your favorite anime:', anime_df['title_english'].values)


if st.button(' Recommend'):
    recommendations = recommend(selected_anime)
    st.subheader(" Recommended for you:")

    cols = st.columns(len(recommendations))
    for idx, (title, image_url) in enumerate(recommendations):
        with cols[idx]:
            st.markdown(f"""
                <div class="recommendation-card">
                    <img src="{image_url}" alt="{title}">
                    <div style="margin-top: 8px; font-weight: bold; color: #fff;"> {title}</div>
                </div>
            """, unsafe_allow_html=True)
