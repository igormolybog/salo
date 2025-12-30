from flask import Flask, request, jsonify, send_from_directory
from google.cloud import firestore
import json
import os

app = Flask(__name__, static_folder='.')

# Initialize Firestore
db = firestore.Client()

def log_event(event_name, metadata=None):
    """Structured logging for Cloud Run"""
    metadata = metadata or {}
    page_name = metadata.get('page', 'unknown')
    log_entry = {
        "event": event_name,
        "severity": "INFO",
        "message": f"Analytics: {event_name} (Page: {page_name})",
        "metadata": metadata
    }
    print(json.dumps(log_entry), flush=True)

@app.route('/')
def index():
    log_event("page_view", {"page": "home"})
    return send_from_directory('.', 'index.html')

@app.route('/track', methods=['POST'])
def track_event():
    event_data = request.json
    event_name = event_data.get('event', 'unknown_click')
    log_event(event_name, event_data.get('metadata', {}))
    return jsonify({"status": "ok"}), 200

@app.route('/<path:path>')
def static_files(path):
    # Track views for significant pages
    if path == 'signup.html':
        log_event("page_view", {"page": "signup_page"})
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
