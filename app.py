from flask import Flask, request, jsonify
from ytmusicapi import YTMusic

app = Flask(__name__)
ytmusic = YTMusic("oauth.json")

# Home
@app.route('/home', methods=['GET'])
def get_home():
    try:
        home_data = ytmusic.get_home(10)  # Mengambil data home dengan batasan 10 item
        return jsonify(home_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Search
@app.route('/search', methods=['GET'])
def search_ytmusic():
    # Ambil query dari parameter yang dikirimkan
    query = request.args.get('query')

    if not query:
        return jsonify({'error': 'Parameter "query" tidak ditemukan'}), 400

    try:
        search_results = ytmusic.search(query=query)
        return jsonify(search_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Playlist Show
@app.route('/playlist/show', methods=['GET'])
def show_playlist():
    playlist_id = request.args.get('playlistId')

    if not playlist_id:
        return jsonify({'error': 'Parameter "playlistId" tidak ditemukan'}), 400

    try:
        playlist_info = ytmusic.get_playlist(playlistId=playlist_id)
        return jsonify(playlist_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Playlist Create
@app.route('/playlist/create', methods=['POST'])
def create_playlist():
    # Ambil judul dari permintaan POST (wajib)
    title = request.json.get('title')

    if not title:
        return jsonify({'error': 'Parameter "title" wajib diisi'}), 400

    # Ambil deskripsi dari permintaan POST, atau gunakan string kosong jika tidak ada
    description = request.json.get('description', '')

    try:
        # Membuat playlist dengan judul dan deskripsi yang diberikan
        create_playlist_response = ytmusic.create_playlist(title=title, description=description, privacy_status="PUBLIC")
        return jsonify(create_playlist_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Playlist Add Items
@app.route('/playlist/addItems', methods=['POST'])
def add_items_to_playlist():
    # Ambil playlistId dari permintaan POST
    playlist_id = request.json.get('playlistId')

    if not playlist_id:
        return jsonify({'error': 'Parameter "playlistId" wajib diisi'}), 400

    # Ambil videoIds (songIds) dari permintaan POST dalam bentuk list
    video_ids = request.json.get('videoIds')

    if not video_ids:
        return jsonify({'error': 'Parameter "videoIds" wajib diisi'}), 400

    try:
        # Menambahkan item (lagu) ke dalam playlist
        add_items_response = ytmusic.add_playlist_items(playlistId=playlist_id, videoIds=video_ids)
        return jsonify(add_items_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Playlist Remove Items
@app.route('/playlist/deleteItems', methods=['POST'])
def delete_items_from_playlist():
    playlist_id = request.json.get('playlistId')

    if not playlist_id:
        return jsonify({'error': 'Parameter "playlistId" wajib diisi'}), 400

    video_ids_to_remove = request.json.get('videoIdsToRemove', [])

    try:
        remove_items_response = ytmusic.remove_playlist_items(playlist_id, video_ids_to_remove)
        return jsonify(remove_items_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Running the App
if __name__ == '__main__':
    app.run(debug=True)
