import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import sys
sys.path.append('/Users/santi/Documents/Vista')
from app.utils.analysis.connect import connect_to_db
from dotenv import load_dotenv
import os

def fetch_tmdb_rating(title, api_key):
    """ Fetch rating from TMDB API using the title of the TV show """
    search_url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={title}"
    search_response = requests.get(search_url)
    search_response.raise_for_status()
    search_data = search_response.json()
    if search_data['results']:
        tv_id = search_data['results'][0]['id'] 
        details_url = f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={api_key}"
        details_response = requests.get(details_url)
        details_response.raise_for_status()
        details_data = details_response.json()
        return details_data.get('vote_average', 'N/A')
    return 'N/A'

def save_last_processed(name):
    with open('last_processed.txt', 'w') as f:
        f.write(name)

def get_last_processed():
    try:
        with open('last_processed.txt', 'r') as f:
            return f.readline().strip()
    except FileNotFoundError:
        return None

def update_ratings(collection, api_key):
    """ Update ratings in the MongoDB collection """
    last_processed = get_last_processed()
    cursor = collection.find({}, {"name": 1, "rating": 1})
    start_updating = False if last_processed else True

    for document in cursor:
        if start_updating or document['name'] == last_processed:
            start_updating = True 
            try:
                new_rating = fetch_tmdb_rating(document['name'], api_key)
                if new_rating != 'N/A':
                    collection.update_one({'_id': document['_id']}, {'$set': {'rating': new_rating}})
                    print(f"Updated rating for {document['name']} to {new_rating}")
                    save_last_processed(document['name']) 
            except requests.exceptions.RequestException as e:
                print(f"Failed to update {document['name']} due to API error: {e}")
                break 

def main():
    load_dotenv()
    api_key = os.getenv("TMDB") 
    print(f"API Key Used: '{api_key}'")
    db = connect_to_db()
    collection = db['shows']
    update_ratings(collection, api_key)
    print("All ratings updated based on TMDB data.")

if __name__ == '__main__':
    main()
