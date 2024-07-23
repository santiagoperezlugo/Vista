from pymongo import MongoClient
import sys
sys.path.append('/Users/santi/Documents/Vista')  # Append the root of your project
from app.utils.analysis.connect import connect_to_db

def extract_decade(date):
    """ Extracts the decade from a date string. """
    if date:
        year = int(date[0:4])
        return f"{(year // 10) * 10}s"  # Formats as '1990s'
    return None  # Handle cases where date might be None or malformed

def update_premiere_to_decade(collection):
    """ Updates 'premiered' field to store only the decade. """
    cursor = collection.find({"premiered": {"$exists": True}})
    for show in cursor:
        decade = extract_decade(show['premiered'])
        if decade:
            collection.update_one({"_id": show['_id']}, {"$set": {"premiered": decade}})
    print("Premiere dates updated to decades.")

def remove_low_count_languages(collection, threshold=80):
    """ Removes documents with languages having fewer shows than the threshold. """
    pipeline = [
        {"$group": {"_id": "$language", "count": {"$sum": 1}}},
        {"$match": {"count": {"$lte": threshold}}}
    ]
    results = collection.aggregate(pipeline)
    low_count_languages = [result['_id'] for result in results]

    if low_count_languages:
        delete_result = collection.delete_many({"language": {"$in": low_count_languages}})
        print(f"Deleted {delete_result.deleted_count} documents in languages with <= {threshold} shows.")
    else:
        print("No languages found with low show counts to remove.")

def remove_noRuntime_movies(collection):
    """ Removes documents without a specified average runtime. """
    result = collection.delete_many({"average_runtime": {"$exists": False}})
    print(f"Deleted {result.deleted_count} documents with 'N/A' average runtimes.")

def remove_noRating_movies(collection):
    """ Removes documents without a specified rating. """
    result = collection.delete_many({"rating": {"$exists": False}})
    print(f"Deleted {result.deleted_count} documents with 'No rating available' ratings.")

def remove_specific_runtimes(collection):
    """ Removes documents with specific average runtimes. """
    # List of specific runtimes to remove
    runtimes_to_remove = [
        150, 8, 7, 49, 6, 2, 26, 4, 13, 210, 130, 85, 51, 110, 42,
        140, 95, 249, 1, 9, 105, 53, 27, 21, 28, 58, 14, 125, 135,
        41, 115, 67, 29, 16, 300, 31, 18, 56, 63, 36, 19, 160, 37,
        360, 200, 57, 73, 62, 66, 72, 96, 255, 34, 33, 170, 68, 165,
        78, 32, 195, 83, 107, 88, 74, 185, 145, 69, 144, 71, 124, 270,
        113, 118, 64, 181, 183, 405, 138, 275, 98, 103, 155, 79, 106, 141,
        93, 77, 215, 92, 235, 191, 175, 313, 84, 82, 91, 61, 136, 420, 121, 89      
    ]
    # Deleting documents with the specified runtimes
    delete_result = collection.delete_many({"average_runtime": {"$in": runtimes_to_remove}})
    print(f"Deleted {delete_result.deleted_count} documents with specified average runtimes.")

def find_missing_premiered(collection):
    # Find documents where 'premiered' field does not exist
    missing_shows = collection.find({"premiered": {"$exists": False}})
    
    # Print the results
    print("Shows with missing 'premiered' field:")
    for show in missing_shows:
        print(show)

# def delete_unknown_values(collection):
#     """ Deletes documents with unknown values in 'decade', 'rating', and 'language' fields. """
#     # Using $or to match any of the conditions
#     delete_result = collection.delete_many({
#         "$or": [
#             {"premiered": {"$eq": None}},  # Assuming 'premiered' should be checked for None
#             {"rating": "N/A"},             # Documents where 'rating' is 'N/A'
#             {"language": {"$eq": None}}    # Documents where 'language' is None
#         ]
#     })
#     # Update print statement to reflect actual fields and operation
#     print(f"Deleted {delete_result.deleted_count} documents with unknown values in 'premiered', 'rating', and 'language' fields.")



def main_cleanup():
    db = connect_to_db()
    shows_collection = db['shows']
    print("Starting cleanup process...")
    delete_unknown_values(shows_collection)  # Remove documents with unknown values
    # find_missing_premiered(shows_collection)
    # update_premiere_to_decade(shows_collection)  # Convert premiere dates to decades
    # remove_low_count_languages(shows_collection)  # Clean up rare languages
    # remove_noRuntime_movies(shows_collection)     # Remove entries without runtime information
    # remove_noRating_movies(shows_collection)      # Remove entries without ratings
    # remove_specific_runtimes(shows_collection)    # Remove entries with specific runtimes
    # print("Cleanup process completed.")

main_cleanup()
