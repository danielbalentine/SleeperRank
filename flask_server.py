from flask import Flask, request, jsonify
from flask_cors import CORS
from backend import SleeperBackend  # Import your existing py_backend class

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Initialize a global py_backend instance
py_backend = SleeperBackend()

@app.route('/initialize', methods=['POST'])
def initialize():
    data = request.json
    username = data.get('username')
    py_backend.set_username(username)
    py_backend.set_user_id()
    py_backend.get_user_leagues()
    py_backend.get_league_images()
    return jsonify({'message': 'Initialization complete'}), 200

@app.route('/getUserLeagues', methods=['GET'])
def get_user_leagues():
    return jsonify(py_backend.leagueNames), 200

@app.route('/getLeagueImages', methods=['GET'])
def get_league_images():
    images = py_backend.userLeaguesAndImages
    # Convert images to a suitable format for JSON response
    # Here we're assuming you have a way to serialize images, like converting to base64
    image_data = {k: v.tobytes() for k, v in images.items()}  # Example; adjust as needed
    return jsonify(image_data), 200

if __name__ == '__main__':
    app.run(debug=True)
