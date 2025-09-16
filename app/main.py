# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from soil_clients import get_soilgrids_props, get_bhuvan_props
from market_client import get_market_price
from ml_model import load_model_and_predict
from db_cache import CacheDB
import uvicorn
import os

app = FastAPI(title="Crop Recommendation Backend (Prototype)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 allows all origins, you can restrict later
    allow_credentials=True,
    allow_methods=["*"],   # allow all HTTP methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],   # allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running 🚀"}

cache = CacheDB("cache.db")

class LocationRequest(BaseModel):
    lat: float
    lon: float
    demo_mode: bool = False
    lang: str = "en"

@app.post("/predict")
def predict(req: LocationRequest):
    # If demo_mode true, return cached sample farm (for hackathon)
    if req.demo_mode:
        sample = cache.get_demo_location()
        soil = sample['soil']
        weather = sample['weather']
        market = sample['market']
    else:
        # Fetch soil data (SoilGrids)
        soil = get_soilgrids_props(req.lat, req.lon)
        # Fetch weather/land from Bhuvan - stubbed
        weather = get_bhuvan_props(req.lat, req.lon)
        # Fetch market price (closest mandi/crop)
        market = get_market_price("maize")  # example as stub

        # If soil seems "urban/no-data", switch to fallback demo (handled by frontend ideally)
        if soil.get('status') == 'no_data':
            raise HTTPException(status_code=422, detail="No farmland data for this location. Try demo_mode or select farm location.")

    # Construct features for ML model
    features = {
        'N': soil.get('nitrogen', 100),
        'P': soil.get('phosphorus', 40),
        'K': soil.get('potassium', 40),
        'pH': soil.get('ph', 6.2),
        'temperature': weather.get('temp', 28),
        'humidity': weather.get('humidity', 60),
        'rainfall': weather.get('rainfall_last_30d', 50)
    }

    recommendation = load_model_and_predict(features)
    # Save to cache
    cache.save_recommendation(req.lat, req.lon, features, recommendation)

    return {
        "soil": soil,
        "weather": weather,
        "market": market,
        "recommendation": recommendation
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
