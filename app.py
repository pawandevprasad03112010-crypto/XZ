import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.environ.get("MAPS_API_KEY", "AIzaSyAgEkSeMft18KAUhrysFh1X32XeMp-hk")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    
    # New Google Places API Endpoint (Text Search v1)
    url = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        # Strictly requesting only Display Name and Phone Number
        "X-Goog-FieldMask": "places.displayName,places.nationalPhoneNumber,places.internationalPhoneNumber"
    }
    
    payload = {
        "textQuery": query
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        # Checking for API Error
        if "error" in data:
            error_msg = data["error"].get("message", "Unknown API Error")
            return jsonify({"error": f"API Error: {error_msg}"}), 400
            
        results = []
        if "places" in data:
            for place in data["places"]:
                name = place.get("displayName", {}).get("text", "N/A")
                # Prefer national phone number, fallback to international
                phone = place.get("nationalPhoneNumber") or place.get("internationalPhoneNumber") or "Phone Not Available"
                
                results.append({
                    "name": name,
                    "phone": phone
                })
                
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
