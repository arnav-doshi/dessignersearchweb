from flask import Flask, request, jsonify, render_template
import base64
import requests
import json

import creds

app = Flask(__name__)

API_URL = creds.api

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected for uploading", 400

    if file:
        img_data = file.read()
        # b64 encoding
        img_base64 = base64.b64encode(img_data).decode('utf-8')
        payload = {
            "body": img_base64,
            "headers": {
                "image_name": file.filename
            }
        }

        # POST request
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            # API Response
            api_response = response.json()
            body = json.loads(api_response["body"])

            return render_template('results.html', results=body)
        else:
            return f"Error: {response.status_code}", 500

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
