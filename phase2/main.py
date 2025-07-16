import requests
import csv
import json
from io import StringIO
from pathlib import Path
from tools.tools import (
    is_industrial_zoning,
    validate_required_fields,
    detect_outliers,
    log_validation_error
)

RAW_PATH = Path("data/raw/raw_data.json")
CLEAN_PATH = Path("data/processed/cleaned_data.json")

def detect_format(content_type: str, url: str) -> str:
    if "json" in content_type or url.endswith(".json"):
        return "json"
    elif "csv" in content_type or url.endswith(".csv"):
        return "csv"
    elif "geojson" in content_type or url.endswith(".geojson"):
        return "geojson"
    return "unknown"

def download_and_parse_data(api_url: str):
    print(f"Downloading data from {api_url}...")
    response = requests.get(api_url)
    response.raise_for_status()

    format_type = detect_format(response.headers.get("Content-Type", ""), api_url)

    if format_type == "json":
        return response.json()
    elif format_type == "csv":
        csv_file = StringIO(response.text)
        return list(csv.DictReader(csv_file))
    elif format_type == "geojson":
        geojson_data = response.json()
        return geojson_data.get("features", [])
    else:
        raise ValueError("Unsupported data format")

def main():
    api_url = input("Enter a full API endpoint (e.g., https://...): ").strip()
    
    records = download_and_parse_data(api_url)
    
    # Extract properties for geojson, or use raw directly
    normalized_records = [
        rec["properties"] if "properties" in rec else rec
        for rec in records
    ]

    # Save raw data
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    with open(RAW_PATH, "w") as f:
        json.dump(normalized_records, f, indent=2)
    print(f"Raw data saved to: {RAW_PATH}")

    # Clean and process
    cleaned = []
    for record in normalized_records:
        if not is_industrial_zoning.invoke({"record": record}):
            continue

        validation = validate_required_fields.invoke({"record": record})
        if not validation["valid"]:
            log_validation_error(record, validation["errors"])
            continue

        outlier = detect_outliers.invoke({"record": record})
        if outlier["is_outlier"]:
            log_validation_error(record, ["outlier"])
            continue

        cleaned.append(record)

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    with open(CLEAN_PATH, "w") as f:
        json.dump(cleaned, f, indent=2)
    print(f"Cleaned data saved to: {CLEAN_PATH}")
    print(f"Total valid industrial records: {len(cleaned)}")

if __name__ == "__main__":
    main()
