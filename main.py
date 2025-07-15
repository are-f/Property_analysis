from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from tools.tools import (
    inspect_api_schema_tool,
    field_variation_mapper_tool,
    auth_requirement_checker_tool,
    rate_limit_detector_tool,
    missing_data_detector_tool,
    batching_and_retry_tool,
    api_documentation_generator_tool,
)
import json
from pathlib import Path

def full_pipeline(api_url: str) -> str:
    print(f" Inspecting API schema at: {api_url}")
    schema = inspect_api_schema_tool.invoke(api_url)

    print(" Mapping field variations...")
    fields = list(schema.keys()) if isinstance(schema, dict) else []
    field_map = field_variation_mapper_tool.invoke({"fields": fields})


    print(" Checking authentication...")
    auth_check = auth_requirement_checker_tool.invoke(api_url)

    print("Checking rate limits...")
    rate_limits = rate_limit_detector_tool.invoke(api_url)

    print(" Detecting missing data...")
    missing_data = missing_data_detector_tool.invoke(api_url)

    print(" Performing batching and retry logic...")
    batch_results = batching_and_retry_tool.invoke(api_url)

    print("Generating documentation...")
    metadata = {
        "schema": schema,
        "field_variations": field_map,
        "auth": auth_check,
        "rate_limits": rate_limits,
        "missing_data_summary": missing_data,
        "batching_test": batch_results,
    }

    # Generate Markdown doc
    markdown_doc = api_documentation_generator_tool.invoke({"metadata": metadata})
    return markdown_doc

def main():
    url = input(" Enter a full API endpoint (e.g., https://datacatalog.cookcountyil.gov/resource/a7ds-fgg3.json): ").strip()
    result = full_pipeline(url)

    print("\n Final Markdown Output:\n")
    print(result)

    # Save to file
    Path("outputs").mkdir(exist_ok=True)
    with open("outputs/structured_api_report.md", "w", encoding="utf-8") as f:
        f.write(result)
    print(" Saved to: outputs/structured_api_report.md")

if __name__ == "__main__":
    main()
