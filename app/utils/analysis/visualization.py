import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from connect import connect_to_db

db = connect_to_db()
shows_collection = db['shows']

# Fetch data from MongoDB
shows_cursor = shows_collection.find()
shows_df = pd.DataFrame(list(shows_cursor))

shows_df = shows_df.explode('genres')  # Ensure 'genres' is the correct field name in your collection

# Count the occurrences of each genre
genre_counts = shows_df['genres'].value_counts()

# Plotting genres by their counts
ax = genre_counts.plot(kind='bar', color='skyblue')
plt.title('TV Show Genres Distribution')
plt.xlabel('Genres')
plt.ylabel('Count')
plt.xticks(rotation=45)

# Annotating the bars with counts
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))

plt.show()



