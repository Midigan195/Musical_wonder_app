# app.py

from flask import Flask, jsonify, render_template, g
from flask_cors import CORS
from Recomendations import get_recommendations
from Search import get_query
import MySQLdb

DB_USER = 'Midigan'
DB_HOST = 'Midigan.mysql.pythonanywhere-services.com'
DB_PASSWORD = 'Enirboreh'
DB_NAME = 'Midigan$Musical_wonder_db'
connection = MySQLdb.connect(user=DB_USER, host=DB_HOST, passwd=DB_PASSWORD, db=DB_NAME)

app = Flask(__name__)
CORS(app)
app.config['DATABASE'] = dict(
    user=DB_USER,
    host=DB_HOST,
    passwd=DB_PASSWORD,
    db=DB_NAME
)

def get_db():
    if 'db' not in g:
        g.db = MySQLdb.connect(**app.config['DATABASE'])
    return g.db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Anime/<int:anime_id>')
def get_anime_data(anime_id):
    anime_query = f"SELECT * FROM Anime WHERE Anime_ID = {anime_id};"
    music_query = f"SELECT * FROM Soundtracks WHERE Anime_ID = {anime_id};"

    cursor = g.db.cursor()

    # Execute queries
    cursor.execute(anime_query)
    anime_data = cursor.fetchone()

    if anime_data is None:
        return jsonify({'error': 'Anime not found', 'data': {}})

    cursor.execute(music_query)
    music_data = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Convert the data to a dictionary
    anime_dict = {
        'anime_data': {
            'Anime_ID': anime_data[0],
            'Name': anime_data[1],
            'Image_URL': anime_data[2],
            'Description': anime_data[3],
            'Writer': anime_data[4],
            'Genre': anime_data[5],
            'Year': anime_data[6]
        },
        'music_data': [{
            'Song_ID': record[0],
            'Anime_ID': record[1],
            'Name': record[2],
            'Artist': record[3],
            'Link': record[4]
        } for record in music_data]
    }

    return jsonify(anime_dict)

@app.route('/recommendations/<int:anime_id>')
def show_recommendations(anime_id):
    # Define the default number of items (e.g., 3)
    connection = g.db
    num_items = 8
    query = "SELECT * FROM Anime;"
    recommendations_data = get_recommendations(query, connection, anime_id, num_items)

    if recommendations_data is None:
        return jsonify({'recommendations': []})

    # Convert DataFrame to JSON format
    recommendations_json = recommendations_data.to_dict(orient='records')

    # Return JSON response
    return jsonify(recommendations_json)

@app.route('/search', strict_slashes=False)
@app.route('/search/<int:page>/')
@app.route('/search/<anime_name>')
@app.route('/search/<anime_name>/')
@app.route('/search/filter/<filter>')
@app.route('/search/<anime_name>/<filter>')
@app.route('/search/<anime_name>/<filter>/')
@app.route('/search/<anime_name>/<filter>/<int:page>')
def search_anime(anime_name=None, filter=None, page=None):
    limit = 8

    query = get_query(anime_name, filter, limit, page)

    cursor = g.db.cursor()
    cursor.execute(query)
    anime_results = cursor.fetchall()

    anime_list = [{'Anime_id': anime[0], 'Name': anime[1], 'Image': anime[2]} for anime in anime_results]
    cursor.close()

    return jsonify(anime_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
