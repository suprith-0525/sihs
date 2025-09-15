# backend/app/market_client.py
def get_market_price(crop_name):
    # For prototype, return a mocked market price (or hit Agmarknet)
    sample = {
        "crop": crop_name,
        "price_per_qtl": 1850,
        "trend": "rising"
    }
    return sample
