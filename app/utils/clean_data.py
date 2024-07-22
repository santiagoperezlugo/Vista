from pymongo import MongoClient
from connect import connect_to_db

db = connect_to_db()
shows_collection = db['shows']  # Adjusted to the 'shows' collection

# Fetch shows where 'N/A' is included in the genres array
shows_with_na = shows_collection.find({"genres": "N/A"})

updated_count = 0  # Counter for the number of updated documents
error_count = 0    # Counter for potential errors during updates

# Update the genre field for each show
for show in shows_with_na:
    try:
        show_type = show.get('type', 'Unknown')  # Get the show type, default to 'Unknown' if not available
        # Replace 'N/A' with show type in the genres list
        updated_genres = [genre if genre != "N/A" else show_type for genre in show['genres']]
        
        # Update the document in MongoDB
        update_result = shows_collection.update_one(
            {"_id": show['_id']},  # Use the unique ID to identify the document
            {"$set": {"genres": updated_genres}}  # Set the new genres array
        )

        if update_result.modified_count == 1:
            print(f"Successfully updated genres for show ID {show['_id']}.")
            updated_count += 1
        else:
            print(f"No changes made for show ID {show['_id']} (possibly already updated).")

    except Exception as e:
        print(f"Error updating show ID {show['_id']}: {e}")
        error_count += 1

print(f"Update completed. Total updated: {updated_count}. Errors encountered: {error_count}.")
