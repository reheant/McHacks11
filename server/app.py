from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from speaker_recoginition import create_audio
from Pdf2Text import extract_text_from_pdf


app = Flask(__name__)

CORS(app, origins=["*"])


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'data': 'This is data from the Flask server'})


@app.route('/Initialization', methods=['POST'])
def record_voice():
    try:
        data = request.json
        userName = data.get('userName')
        create_audio(f"{userName}.wav")
        return jsonify({'status': 'success'})
    except Exception as e:
        print(e) 
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
