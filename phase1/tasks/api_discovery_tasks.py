api_discovery_task = {
    "name": "API Discovery and Cataloguing",
    "description": (
        "Given a public government or open data website, discover any available REST APIs. "
        "For each discovered API, analyze and extract the following:\n\n"
        "- List of endpoints\n"
        "- Field names and their data types\n"
        "- Mappings of common field variations (e.g., square_feet vs sqft vs area)\n"
        "- Available query filters (e.g., owner, land_use, zip_code)\n"
        "- Authentication requirements (API key, OAuth, or none)\n"
        "- Rate limits and headers (e.g., X-RateLimit, Retry-After)\n"
        "- Percentage of missing data and inconsistencies in field types\n"
        "- Pagination or batching support with retry logic\n\n"
        "Generate a clear and readable API catalog in Markdown format."
    ),
    "expected_output": (
        "A structured Markdown document summarizing the discovered APIs. "
        "It must include endpoint URLs, field schema, field name standardization, "
        "available filters, rate limits, retry logic, and any auth requirements."
    )
}
