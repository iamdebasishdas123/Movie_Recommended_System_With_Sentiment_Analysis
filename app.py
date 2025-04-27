import streamlit as st
import pickle
import pandas as pd
import requests
from bs4 import BeautifulSoup
import joblib
import time

# Function to fetch movie details using TMDB API
def fetch_movie(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    try:
        response = requests.get(url, timeout=35)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        imdb_id = data.get('imdb_id')
        rating = data.get("vote_average")
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return [full_path, imdb_id, rating]
        else:
            return ["https://via.placeholder.com/500x750.png?text=Poster+Not+Available", None, None]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return ["https://via.placeholder.com/500x750.png?text=Poster+Not+Available", None, None]

# Function to fetch reviews from IMDb
def fetch_reviews(imdb_id, max_reviews=100):
    print(imdb_id)
    start_url = f'https://www.imdb.com/title/{imdb_id}/reviews?ref_=tt_ururv_sm'
    link = f'https://www.imdb.com/title/{imdb_id}/reviews/_ajax'
    params = {'ref_': 'undefined', 'paginationKey': ''}
    reviews = []

    with requests.Session() as s:
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        res = s.get(start_url)

        while len(reviews) < max_reviews:
            soup = BeautifulSoup(res.text, "lxml")
            for item in soup.select(".review-container"):
                review_text = item.select_one(".text.show-more__control").get_text(strip=True)
                reviews.append(review_text)
                if len(reviews) >= max_reviews:
                    break

            try:
                pagination_key = soup.select_one(".load-more-data[data-key]").get("data-key")
                if not pagination_key:
                    break
            except AttributeError:
                break

            params['paginationKey'] = pagination_key
            res = s.get(link, params=params)

    return reviews

# Function to perform sentiment analysis on reviews
def perform_sentiment_analysis(reviews):
    print(reviews)
    if len(reviews) == 0:
        return 0, 0, [], []  # Or handle as you prefer

    vectorizer = joblib.load(open('IMDB_vectorizer.pkl', 'rb'))
    model = joblib.load(open('IMDB_svm.pkl', 'rb'))
    X = vectorizer.transform(reviews)
    X = X.toarray()
    sentiments = model.predict(X)

    positive_reviews = (sentiments == 1).sum()
    negative_reviews = (sentiments == 0).sum()
    total_reviews = len(sentiments)

    positive_percentage = (positive_reviews / total_reviews) * 100
    negative_percentage = (negative_reviews / total_reviews) * 100

    return positive_percentage, negative_percentage, reviews, sentiments


# Function to recommend movies
def recommend(movie_title):
    movie_index = movie[movie["title"] == movie_title].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movie_list:
        movie_id = movie.iloc[i[0]].movie_id
        recommended_movies.append(movie.iloc[i[0]]["title"])
        result = fetch_movie(movie_id)
        poster = result[0]
        recommended_movie_posters.append(poster)

    return recommended_movies, recommended_movie_posters

# Load data
try:
    movie = pickle.load(open('movie.pkl', 'rb'))
    similarity = pickle.load(open('Movie_similarity.pkl', 'rb'))
except (FileNotFoundError, pickle.UnpicklingError) as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Streamlit app layout
st.title("Movie Recommender System")
m = st.selectbox("Select a movie", movie["title"].values)

# Sentiment analysis button
if st.button('Analyze Sentiment'):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    movie_id = movie[movie["title"] == m].movie_id.values[0]
    result = fetch_movie(movie_id)
    imdb_id = result[1]
    progress_bar.progress(30)
    status_text.text(f"Progress: 35%")
    st.success(f"IMDB Rating: {result[2]}")

    if imdb_id:
        reviews = fetch_reviews(imdb_id, max_reviews=100)
        # print(f"Fetched {len(reviews)} reviews.")
        df_reviews = pd.DataFrame(reviews, columns=["Review"])
        progress_bar.progress(50)
        status_text.text(f"Progress: 50%")

        positive_percentage, negative_percentage, reviews, sentiments = perform_sentiment_analysis(df_reviews["Review"])
        progress_bar.progress(90)
        status_text.text(f"Progress: 90%")
        st.success(f"Positive reviews: {positive_percentage:.2f}%")
        st.error(f"Negative reviews: {negative_percentage:.2f}%")
        progress_bar.progress(100)
        status_text.text(f"Progress: 100%")
    else:
        st.error("Failed to fetch IMDb ID.")

# Show recommendation button
if st.button('Show Recommendation'):
    recommended_movies, recommended_movie_posters = recommend(m)
    cols = st.columns(5)
    for col, movie, poster in zip(cols, recommended_movies, recommended_movie_posters):
        col.text(movie)
        col.image(poster)
        
footer_html = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    padding: 20px;
}
</style>
<div class="footer">
    <p>Made ❤️ by Debasish Das</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
