from flask import Flask, jsonify
from flask_cors import CORS
from speaker_recoginition import create_audio
app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'data': 'This is data from the Flask server'})

@app.route('/recordvoice', methods=['POST'])
def record_voice():
    data = request.json
    userName = data.get('userName')
    create_audio(userName)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
