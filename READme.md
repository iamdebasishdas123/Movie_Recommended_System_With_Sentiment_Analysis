To run your Streamlit app:

1. **Install Python** if not already installed.

2. **Install necessary packages**:
   ```bash
   pip install streamlit pandas requests beautifulsoup4 joblib scikit-learn
   ```

3. **Navigate to your project directory**:
   ```bash
   cd /path/to/your/project
   ```

4. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

Replace `/path/to/your/project` with the path where your script is located and `app.py` with the name of your Streamlit script.

**Problem Statement**

In the contemporary digital entertainment landscape, movie recommendations are essential to help users discover content that aligns with their preferences. Additionally, understanding the sentiment of movie reviews can provide deeper insights into the audience's reception of a film. 

**Objective**

The objective of this project is to develop a web-based application using Streamlit that:

1. **Recommends Movies:** Provides personalized movie recommendations based on user input, using a movie dataset and similarity measures. This allows users to find films similar to a given movie they like.

2. **Performs Sentiment Analysis:** Analyzes sentiment from IMDb reviews of the selected movie. This involves:
   - Fetching reviews from IMDb.
   - Performing sentiment analysis to determine the proportion of positive and negative reviews.
   - Displaying these sentiment results to users, providing insights into the overall reception of the movie.

**Key Features**

1. **Movie Information Retrieval:**
   - Fetch and display movie posters and ratings using the TMDB API.
   - Handle cases where movie information is incomplete or unavailable.

2. **Sentiment Analysis:**
   - Retrieve and process movie reviews from IMDb.
   - Utilize a trained sentiment analysis model to classify reviews as positive or negative.
   - Display the percentage of positive and negative reviews.

3. **Recommendation System:**
   - Provide recommendations for movies similar to the user's selected film.
   - Display recommended movies along with their posters for better visualization.

**Challenges Addressed**

1. **Data Integration:** Combining data from multiple sources (TMDB API and IMDb) to provide comprehensive information about movies.
2. **Sentiment Analysis:** Developing and applying a machine learning model to analyze and classify the sentiment of movie reviews.
3. **User Experience:** Designing an intuitive and interactive web interface to enhance user engagement and provide real-time feedback.

---

This problem statement outlines the goals, features, and challenges of your project, providing a clear framework for the development and evaluation of your movie recommender and sentiment analysis system.