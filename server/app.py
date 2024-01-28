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
    

@app.route('/upload_pdf', methods=['POST'])
def transform_pdf():
    print("Received a request to '/upload_pdf'")
    
    if 'pdf' not in request.files:
        print("No 'pdf' file in request.files")
        return jsonify({'error': 'No file part'}), 400
    
    pdf_file = request.files['pdf']
    print(f"Received file: {pdf_file.filename}")

    # Assuming extract_text_from_pdf accepts a file stream and returns text
    try:
        extracted_text = extract_text_from_pdf(pdf_file.stream)
        print("Extracted text successfully.")
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        extracted_text = str(e)  # Sending error details for debugging purposes
    
    return jsonify({'extracted_text': extracted_text})


  

@app.route('/Meeting', methods=['POST'])
def HandleMeetingMinutes():
    data = request.json
    meeting_minutes = data.get('meetingMinutes')

    print("Received meeting minutes:", meeting_minutes)

    # Send back a confirmation response
    return jsonify({'status': 'success', 'message': 'Meeting minutes received successfully.'})



if __name__ == '__main__':
    app.run(debug=True)
