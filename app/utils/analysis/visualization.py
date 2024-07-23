import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from connect import connect_to_db

def fetch_shows_data():
    db = connect_to_db()
    shows_collection = db['shows']
    shows_cursor = shows_collection.find()
    shows_df = pd.DataFrame(list(shows_cursor))
    shows_df = shows_df.explode('genres')
    return shows_df

def plot_genre_distribution(shows_df):
    # Handle N/A or invalid entries by filling them with a placeholder
    shows_df['genres'].replace('', 'Unknown', inplace=True)
    shows_df['genres'].replace('N/A', 'Unknown', inplace=True) 
    shows_df['genres'].fillna('Unknown', inplace=True)

    # Count the occurrences of each genre including 'Unknown'
    genre_counts = shows_df['genres'].value_counts().sort_index()

    # Plotting
    plt.figure(figsize=(14, 7))
    ax_genre = genre_counts.plot(kind='bar', color='skyblue', title='TV Show Genres Distribution')
    ax_genre.set_xlabel('Genres')
    ax_genre.set_ylabel('Count')
    plt.xticks(rotation=45)
    
    # Annotating the bars with counts
    for p in ax_genre.patches:
        ax_genre.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    
    plt.show()


def plot_language_distribution(shows_df):
    shows_df['language'].replace('', 'Unknown', inplace=True)
    shows_df['language'].replace('N/A', 'Unknown', inplace=True) 
    shows_df['language'].fillna('Unknown', inplace=True)
    language_counts = shows_df['language'].value_counts()
    ax_lang = language_counts.plot(kind='bar', color='green', title='TV Show Languages Distribution')
    ax_lang.set_xlabel('Language')
    ax_lang.set_ylabel('Count')
    plt.xticks(rotation=45)
    for p in ax_lang.patches:
        ax_lang.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()

def plot_decade_distribution(shows_df):
    shows_df['premiered'].replace('', 'Unknown', inplace=True)
    shows_df['premiered'].replace('N/A', 'Unknown', inplace=True) 
    shows_df['premiered'].fillna('Unknown', inplace=True) # invalid entries

    # Count the occurrences of each decade including 'Unknown'
    decade_counts = shows_df['premiered'].value_counts().sort_index()

    # Plotting
    plt.figure(figsize=(14, 7))
    ax_decade = decade_counts.plot(kind='bar', color='red', title='Distribution of TV Shows by Decade')
    ax_decade.set_xlabel('Decade')
    ax_decade.set_ylabel('Number of Shows')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Annotating the bars with counts
    for p in ax_decade.patches:
        ax_decade.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

    plt.tight_layout()
    plt.show()



def plot_runtime_distribution(shows_df):
    shows_df['average_runtime'].replace('', 'Unknown', inplace=True)
    shows_df['average_runtime'].replace('N/A', 'Unknown', inplace=True) 
    shows_df['average_runtime'].fillna('Unknown', inplace=True)
    runtime_counts = shows_df['average_runtime'].value_counts()
    ax_runtime = runtime_counts.plot(kind='bar', color='purple', title='TV Show Runtime Distribution')
    ax_runtime.set_xlabel('Runtime (minutes)')
    ax_runtime.set_ylabel('Count')
    plt.xticks(rotation=45)
    for p in ax_runtime.patches:
        ax_runtime.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()

def plot_rating_distribution(shows_df):
    shows_df['rating'].replace('', 'Unknown', inplace=True)
    shows_df['rating'].replace('N/A', 'Unknown', inplace=True) 
    shows_df['rating'].fillna('Unknown', inplace=True)
    rating_counts = shows_df['rating'].value_counts()
    ax_rating = rating_counts.plot(kind='line', color='orange', title='TV Show Ratings Distribution')
    ax_rating.set_xlabel('Rating')
    ax_rating.set_ylabel('Count')
    plt.xticks(rotation=45)
    for p in ax_rating.get_lines():
        plt.text(p.get_xydata()[0][0], p.get_xydata()[0][1], str(int(p.get_xydata()[0][1])))
    plt.show()

def count_runtimes(shows_collection):
    pipeline = [
        {"$match": {"average_runtime": {"$exists": True}}},
        {"$group": {"_id": "$average_runtime", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    results = shows_collection.aggregate(pipeline)
    print("Runtime (minutes) - Count")
    for result in results:
        print(f"{result['_id']} - {result['count']}")

def count_ratings(collection):
    pipeline = [
        {"$match": {"rating": {"$exists": True}}},
        {"$group": {"_id": "$rating", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    results = collection.aggregate(pipeline)
    print("Rating - Count")
    for result in results:
        print(f"{result['_id']} - {result['count']}")


def main():
    shows_df = fetch_shows_data()
    plot_genre_distribution(shows_df)
    plot_language_distribution(shows_df)
    plot_decade_distribution(shows_df)
    plot_runtime_distribution(shows_df)
    plot_rating_distribution(shows_df)
    count_runtimes()

if __name__ == "__main__":
    main()
