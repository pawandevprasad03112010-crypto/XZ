import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Aapki Google Maps API Key
API_KEY = os.environ.get("MAPS_API_KEY", "AIzaSyAgEkSeMft18KAUhrysFh1X32XeMp-hk")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    
    # 1. Text Search API call to get places list
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
    response = requests.get(search_url).json()
    
    results = []
    
    if 'results' in response:
        for place in response['results']:
            name = place.get('name', 'N/A')
            place_id = place.get('place_id')
            phone_number = "Phone Not Available"
            
            # 2. Place Details API call to fetch phone number using place_id
            if place_id:
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number&key={API_KEY}"
                details_response = requests.get(details_url).json()
                
                if 'result' in details_response:
                    phone_number = details_response['result'].get('formatted_phone_number', 'Phone Not Available')
            
            results.append({
                'name': name,
                'phone': phone_number
            })
            
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
  
