import requests
import json
from pathlib import Path

def fetch_data_from_api(api_url, output_file="data/raw_data.json"):
    response = requests.get(api_url)
    data = response.json()
    Path("data").mkdir(exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    return data
