import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
# Load environment variables
load_dotenv()
uri = os.getenv("MONGO_URI")

def fetch_data():
    client = MongoClient(uri)
    db = client['tv_shows_db']
    collection = db['shows']
    tv_shows = list(collection.find())
    return pd.DataFrame(tv_shows)


def preprocess_data(shows_df):
    shows_df['genres'] = shows_df['genres'].apply(lambda x: x if isinstance(x, list) else [])
    mlb = MultiLabelBinarizer()
    genres_encoded = mlb.fit_transform(shows_df['genres'])
    genre_columns = mlb.classes_

    # Define transformers for numerical and categorical data
    numerical_features = ['average_runtime', 'rating']
    categorical_features = ['language', 'premiered']

    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', MinMaxScaler())
    ])
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    features = shows_df[numerical_features + categorical_features]
    features_transformed = preprocessor.fit_transform(features)

    # Extract feature names for the dataframe
    cat_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
    all_feature_names = numerical_features + list(cat_feature_names)

    features_df = pd.DataFrame(features_transformed.toarray(), columns=all_feature_names)

    # Combine genre data with other features
    full_features = pd.concat([pd.DataFrame(genres_encoded, columns=genre_columns), features_df], axis=1)
    
    return full_features, list(genre_columns) + list(all_feature_names)

# Build cosine similarity matrix
def build_similarity_matrix(processed_df):
    similarity_matrix = cosine_similarity(processed_df)
    return pd.DataFrame(similarity_matrix, index=processed_df.index, columns=processed_df.index)

# Function to get recommendations based on cosine similarity and include recommendation scores, adjust top_n to get more recommendations
def get_recommendations(show_id, similarity_df, shows_df, top_n=15):
    sim_scores = similarity_df.loc[show_id]
    top_indices = sim_scores.sort_values(ascending=False).index[1:top_n+1]
    recommended_shows = shows_df.loc[shows_df.index.isin(top_indices)]
    # Include the similarity scores in the output
    recommended_shows['recommendation_score'] = sim_scores[top_indices].values
    return recommended_shows[['name', 'url', 'rating', 'recommendation_score']]


# Find a show by name and return its _id
def find_show_index_by_name(show_name, shows_df):
    matches = shows_df[shows_df['name'].str.lower() == show_name.lower()]
    if not matches.empty:
        return matches.index[0]
    else:
        return None

# testing
def main():
    show_name = "One Piece" 
    shows_df = fetch_data()
    processed_df, feature_columns = preprocess_data(shows_df)
    similarity_df = build_similarity_matrix(processed_df)

    show_index = find_show_index_by_name(show_name, shows_df)
    if show_index is not None:
        recommendations = get_recommendations(show_index, similarity_df, shows_df)
        print("Recommendations based on multiple features:")
        print(recommendations)
    else:
        print(f"No shows found with the name '{show_name}'.")

if __name__ == "__main__":
    main()
