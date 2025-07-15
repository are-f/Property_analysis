from langchain_core.tools import tool
import requests
import time
from typing import List, Dict


@tool
def inspect_api_schema_tool(api_url: str) -> Dict[str, str]:
    """Inspect an API endpoint and return field names with inferred data types."""
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        sample = data[0] if isinstance(data, list) and data else data
        schema = {k: type(v).__name__ for k, v in sample.items()}
        return schema
    except Exception as e:
        return {"error": str(e)}


@tool
def field_variation_mapper_tool(fields: List[str]) -> Dict[str, List[str]]:
    """Map field name variations to a standard field name group."""
    variations = {
        "square_feet": ["sqft", "area", "building_area", "sq_feet", "square_footage"],
        "zip_code": ["zipcode", "zip", "postal_code", "zip_code"],
        "city": ["town", "municipality"],
        "property_type": ["type", "property_category"]
    }
    mapping = {}
    for field in fields:
        for standard, aliases in variations.items():
            if field in aliases or field == standard:
                mapping.setdefault(standard, []).append(field)
    return mapping


@tool
def auth_requirement_checker_tool(api_url: str) -> str:
    """Check if the API endpoint requires authentication."""
    try:
        r = requests.get(api_url, timeout=10)
        if r.status_code == 401:
            return "Authentication required (401)"
        return "No authentication required"
    except Exception:
        return "Could not determine"


@tool
def rate_limit_detector_tool(api_url: str) -> Dict[str, str]:
    """Detect if the API provides rate-limiting information in headers."""
    try:
        r = requests.get(api_url, timeout=10)
        return {
            "X-RateLimit-Limit": r.headers.get("X-RateLimit-Limit", "N/A"),
            "X-RateLimit-Remaining": r.headers.get("X-RateLimit-Remaining", "N/A"),
            "Retry-After": r.headers.get("Retry-After", "N/A"),
        }
    except Exception as e:
        return {"error": str(e)}


@tool
def missing_data_detector_tool(api_url: str) -> Dict[str, float]:
    """Detect percentage of missing fields in the API response."""
    try:
        r = requests.get(api_url, timeout=10)
        r.raise_for_status()
        data = r.json()
        sample_data = data if isinstance(data, list) else [data]
        if not sample_data:
            return {"error": "No data available."}
        total = len(sample_data)
        keys = sample_data[0].keys()
        return {
            key: round(sum(1 for row in sample_data if not row.get(key)) / total * 100, 2)
            for key in keys
        }
    except Exception as e:
        return {"error": str(e)}


@tool
def batching_and_retry_tool(api_url: str) -> Dict[str, any]:
    """Simulate paginated fetching and retry on rate limit errors."""
    results = []
    for i in range(1, 4):  # simulate 3 pages
        try:
            paged_url = f"{api_url}?$limit=100&$offset={(i - 1) * 100}"
            response = requests.get(paged_url, timeout=10)
            if response.status_code == 429:
                time.sleep(1)
                response = requests.get(paged_url)
            response.raise_for_status()
            data = response.json()
            results.extend(data if isinstance(data, list) else [data])
        except Exception:
            continue
    return {
        "records_fetched": len(results),
        "sample_record": results[0] if results else {}
    }


@tool
def api_documentation_generator_tool(metadata: dict = {}) -> str:
    """Generate simple Markdown documentation from API metadata."""
    if not metadata:
        return " No metadata provided to document."

    lines = ["# API Documentation\n"]
    for key, value in metadata.items():
        lines.append(f"## {key}\n")
        lines.append("```json\n" + str(value) + "\n```\n")
    return "\n".join(lines)
