# backend/app/soil_clients.py
import requests

SOILGRIDS_BASE = "https://rest.soilgrids.org/query"

def get_soilgrids_props(lat, lon):
    try:
        url = f"{SOILGRIDS_BASE}?lon={lon}&lat={lat}"
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return {'status':'no_data'}
        data = resp.json()
        props = {}
        # SoilGrids returns nested properties; we extract pH and texture mean
        ph = data.get('properties', {}).get('phh2o', {})
        # pick mean of 0-5cm layer if exists
        if 'mean' in ph:
            # sometimes it's a dict of depth keys; we pick reasonable one
            props['ph'] = ph['mean']
        # for demo fallback
        props['nitrogen'] = data.get('properties', {}).get('nitrogen', {}).get('mean', 0)
        props['status'] = 'ok'
        return props
    except Exception as e:
        print("SoilGrids error:", e)
        return {'status':'no_data'}

def get_bhuvan_props(lat, lon):
    # Bhuvan API may require keys; this is a placeholder/stub
    # You can replace with actual Bhuvan API calls if you have access
    # For now return demo weather-like object using free weather or synthetic values
    return {
        'temp': 28,
        'humidity': 65,
        'rainfall_last_30d': 40,
        'land_use': 'rainfed'
    }
