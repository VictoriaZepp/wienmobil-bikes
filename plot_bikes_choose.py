import json
import matplotlib.pyplot as plt

with open("bike_data_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)


all_stations = {station["name"] for station in data[0]}
print("Available stations:")
for name in sorted(all_stations):
    print("-", name)

station_name = input("\nEnter the station name: ")


timestamps = []
num_bikes = []

for snapshot in data:
    for station in snapshot:
        if station_name.lower() in station.get("name", "").lower():
            ts = station.get("timestamp")
            bikes = station.get("num_bikes")

            if ts is not None and bikes is not None:
                timestamps.append(ts)
                num_bikes.append(bikes)


if not timestamps:
    print(f"\nNo data found for {station_name}. Check the name and try again.")
else:
    plt.plot(timestamps, num_bikes, marker="o")
    plt.title(f"Available Bikes at {station_name}")
    plt.xlabel("Time")
    plt.ylabel("Number of Bikes")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()