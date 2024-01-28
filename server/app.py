from flask import Flask, jsonify
from flask_cors import CORS
from speaker_recoginition import create_audio
app = Flask(__name__)
CORS(app, resources={r"/recordvoice": {"origins": "http://localhost:3000"}})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'data': 'This is data from the Flask server'})

if __name__ == '__main__':
    app.run(debug=True)
