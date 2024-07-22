from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

games = [
    {"title": "Game A", "description": "A puzzle game that challenges your brain."},
    {"title": "Game B", "description": "An action-packed adventure game."}
]

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform([game['description'] for game in games])

def get_recommendation(user_input, tfidf, games):
    user_tfidf = tfidf.transform([user_input])
    cosine_similarities = linear_kernel(user_tfidf, tfidf_matrix).flatten()
    top_match_index = cosine_similarities.argmax()
    return games[top_match_index]
