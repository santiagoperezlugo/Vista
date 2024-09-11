from flask import Flask, request, jsonify, render_template
import pandas as pd
from app.models import fetch_data, preprocess_data, build_similarity_matrix, get_recommendations, find_show_index_by_name  # Adjust the import path based on your file name

app = Flask(__name__)

shows_df = fetch_data()
processed_df, feature_columns = preprocess_data(shows_df)
similarity_df = build_similarity_matrix(processed_df)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/recommendations', methods=['GET'])
def recommendations():
    show_name = request.args.get('showName', type=str)
    if not show_name:
        return jsonify({'error': 'Missing show name'}), 400

    show_index = find_show_index_by_name(show_name, shows_df)
    if show_index is not None:
        recs = get_recommendations(show_index, similarity_df, shows_df)
        # Include the image_url from your data, adjust the key name based on your actual data structure
        recs['image_url'] = 'path/to/default/image' 
        return jsonify(recs.to_dict('records'))
    else:
        return jsonify({'message': f"No shows found with the name '{show_name}'."}), 404

if __name__ == '__main__':
    app.run(debug=True)
