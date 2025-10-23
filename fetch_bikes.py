import requests
import json
from datetime import datetime, timezone

url_status = "https://api.wstw.at/gateway/WL_WIENMOBIL_API/1/station_status.json"
url_info = "https://api.wstw.at/gateway/WL_WIENMOBIL_API/1/station_information.json"


status = requests.get(url_status, timeout=20)
status.raise_for_status()
status = status.json()

info = requests.get(url_info, timeout=20)
info.raise_for_status()
info = info.json()

info_dict = {s["station_id"]: s for s in info ["data"]["stations"]}

timestamp = datetime.now(timezone.utc).isoformat()
combined = []
for s in status["data"]["stations"]:
    station_id = s["station_id"]
    station_info = info_dict.get(station_id, {})
    combined.append({
        "timestamp": timestamp,
        "station_id": station_id,
        "name": station_info.get("name"),
        "lat": station_info.get("lat"),
        "lon": station_info.get("lon"),
        "num_bikes": s.get("num_bikes_available"),
        "num_docks": s.get("num_docks_available")
    })

try:
    with open("bike_data_all.json", "r", encoding="utf-8") as f:
        old_data = json.load(f)
except FileNotFoundError:
    old_data = []

old_data.append(combined)

with open("bike_data_all.json", "w", encoding="utf-8") as f:
    json.dump(old_data, f, indent=2)

print("Data added successfully!")
