from flask import Flask, request, jsonify, send_from_directory
from google.cloud import firestore
import os

app = Flask(__name__, static_folder='.')

# Initialize Firestore
db = firestore.Client()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    
    if not name or not email:
        return jsonify({"error": "Missing name or email"}), 400
    
    try:
        # Save lead to Firestore
        doc_ref = db.collection('leads').document()
        doc_ref.set({
            'name': name,
            'email': email,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        return jsonify({"message": "Success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to save lead"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # In production, we don't call app.run() directly but use Gunicorn
    app.run(host='0.0.0.0', port=port, debug=True)
