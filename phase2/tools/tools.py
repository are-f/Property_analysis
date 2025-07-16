import json
from pathlib import Path
from langchain_core.tools import tool

@tool
def validate_required_fields(record: dict) -> dict:
    """Validate if record contains required fields like zoning and square_feet."""
    required = ["property_type", "zoning_classification", "square_feet"]
    errors = [field for field in required if field not in record or not record[field]]
    return {
        "valid": not errors,
        "errors": errors
    }

@tool
def is_industrial_zoning(record: dict) -> bool:
    """Check if zoning classification is industrial (M1, M2, I-1, I-2)."""
    zoning_codes = ["M1", "M2", "I-1", "I-2"]
    zoning = record.get("zoning_classification", "").upper()
    return any(code in zoning for code in zoning_codes)

@tool
def detect_outliers(record: dict) -> dict:
    """Detect if square_feet value is outlier or invalid."""
    area = record.get("square_feet", 0)
    try:
        area = float(area)
        is_outlier = area > 1_000_000 or area <= 0
    except:
        is_outlier = True
    return {
        "is_outlier": is_outlier,
        "square_feet": area
    }

def log_validation_error(record, errors, log_path="data/logs/validation_errors.log"):
    """Log records with missing fields or outliers to a log file."""
    Path("data/logs").mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps({"record": record, "errors": errors}) + "\n")
