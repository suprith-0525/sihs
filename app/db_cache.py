# backend/app/db_cache.py
import sqlite3
import json
from datetime import datetime

class CacheDB:
    def __init__(self, path="cache.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY,
            lat REAL,
            lon REAL,
            ts TEXT,
            features TEXT,
            recommendation TEXT
        )
        """)
        # demo location
        cur.execute("""
        CREATE TABLE IF NOT EXISTS demo_locations (
          id INTEGER PRIMARY KEY,
          name TEXT,
          lat REAL,
          lon REAL,
          soil TEXT,
          weather TEXT,
          market TEXT
        )
        """)
        self.conn.commit()
        # insert a sample demo if missing
        cur.execute("SELECT count(*) FROM demo_locations")
        if cur.fetchone()[0] == 0:
            sample_soil = json.dumps({'ph':6.1,'nitrogen':120,'phosphorus':45,'potassium':50})
            sample_weather = json.dumps({'temp':27,'humidity':70,'rainfall_last_30d':60})
            sample_market = json.dumps({'maize':1800})
            cur.execute("INSERT INTO demo_locations (name,lat,lon,soil,weather,market) VALUES (?,?,?,?,?,?)",("Nalgonda_Farm", 17.0, 79.0, sample_soil, sample_weather, sample_market))

            self.conn.commit()

    def save_recommendation(self, lat, lon, features, recommendation):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO recommendations (lat,lon,ts,features,recommendation) VALUES (?,?,?,?,?)",
                    (lat, lon, datetime.utcnow().isoformat(), json.dumps(features), json.dumps(recommendation)))
        self.conn.commit()

    def get_demo_location(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name,lat,lon,soil,weather,market FROM demo_locations LIMIT 1")
        r = cur.fetchone()
        return {
            'name': r[0],
            'lat': r[1],
            'lon': r[2],
            'soil': json.loads(r[3]),
            'weather': json.loads(r[4]),
            'market': json.loads(r[5])
        }
