import requests
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['tv_shows_db']  # Create a database named 'tv_shows_db'
collection = db['shows']  # Create a collection named 'shows