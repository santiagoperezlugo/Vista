import requests
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.utils.analysis.connect import connect_to_db

def fetch_tv_show_details(page=1):
    url = f"http://api.tvmaze.com/shows?page={page}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def clean_html_tags(text):
    """ Utility function to clean HTML tags from strings """
    if not text:
        return 'No summary available'
    return text.replace('<p>', '').replace('</p>', '').replace('<b>', '').replace('</b>', '')

def parse_and_store_show_data(shows, collection):
    for show in shows:
        # Prepare the document
        document = {
            "name": show['name'],
            "type": show['type'],
            "language": show['language'],
            "genres": show['genres'] if show['genres'] else 'N/A',
            "status": show['status'],
            "premiered": show['premiered'],
            "url": show['url'],
            "summary": clean_html_tags(show['summary']),
            "rating": show['rating']['average'] if show['rating']['average'] else 'No rating available',
            "image_url": show.get('image', {}).get('medium') if show.get('image') else 'No image available'
        }
        # Update or insert the document in MongoDB
        collection.update_one({'name': document['name']}, {'$set': document}, upsert=True)
        print(f"Processed: {document['name']}")



def main():
    db = connect_to_db()
    collection = db['shows']
    page = 1  # Initialize page variable here
    while page < 301:
        data = fetch_tv_show_details(page)
        if not data:
            print("No more data to fetch.")
            break
        parse_and_store_show_data(data, collection)
        page += 1
        print(f"Page {page} fetched and stored in MongoDB.")

if __name__ == '__main__':
    main()

