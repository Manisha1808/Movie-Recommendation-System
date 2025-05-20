import requests
from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
from flask_mysqldb import MySQL

# Flask app setup
app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'movie_db'

mysql = MySQL(app)

# OMDb API key
api_key = 'e602210f'

# Function to fetch poster URL from OMDb API
def fetch_omdb_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster')  # Returns poster URL or None

# Load data from MySQL database
def load_data_from_db():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT title, overview, genres, vote_average, release_date FROM movies")
    data = cursor.fetchall()
    cursor.close()
    
    # Convert to DataFrame
    columns = ['original_title', 'overview', 'genres', 'vote_average', 'release_date']
    return pd.DataFrame(data, columns=columns)

# Recommendation logic (updated with OMDb poster)
def get_movie_recommendations(title, top_n=10):
    df = load_data_from_db()  # Load data from DB
    title = title.lower()
    
    # Check for exact match first
    exact_match = df[df['original_title'].str.lower() == title]
    if not exact_match.empty:
        idx = exact_match.index[0]
    else:
        # Use fuzzy matching on original_title
        result = process.extractOne(title, df['original_title'].str.lower())
        if result:
            closest_match, score = result[:2]
            if score < 70:
                return None
            idx = df[df['original_title'].str.lower() == closest_match].index[0]
        else:
            return None

    # Compute similarity scores
    cosine_sim = cosine_similarity(TfidfVectorizer(stop_words='english').fit_transform(df['overview']), 
                                   TfidfVectorizer(stop_words='english').fit_transform(df['overview']))
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get top N similar movies
    movie_indices = [i[0] for i in sim_scores[1:top_n+1]]
    
    # Fetch poster URLs for each movie
    movie_data = df[['original_title', 'genres', 'vote_average', 'release_date']].iloc[movie_indices]
    movie_data['Poster_URL'] = movie_data['original_title'].apply(fetch_omdb_poster)
    
    return movie_data

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        movie_title = request.form['movie_title']  # Make sure this matches the form field
        results = get_movie_recommendations(movie_title)

        if results is None:
            message = f"No close match found for '{movie_title}'. Please check your spelling."
            return render_template('index.html', message=message, movie_title=movie_title)
        
        return render_template('index.html', movie_title=movie_title.title(), recommendations=results.to_dict(orient='records'))

    # For GET requests, render the form
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
