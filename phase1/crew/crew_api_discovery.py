from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

from tools.tools import (
    discover_api_endpoints_tool,
    inspect_api_schema_tool,
    field_variation_mapper_tool,
    auth_requirement_checker_tool,
    rate_limit_detector_tool,
    missing_data_detector_tool,
    batching_and_retry_tool,
    api_documentation_generator_tool
)

# Load OpenAI LLM
llm = ChatOpenAI(temperature=0, model="gpt-4")

# List of tools
tools = [
    discover_api_endpoints_tool,
    inspect_api_schema_tool,
    field_variation_mapper_tool,
    auth_requirement_checker_tool,
    rate_limit_detector_tool,
    missing_data_detector_tool,
    batching_and_retry_tool,
    api_documentation_generator_tool
]

# Initialize LangChain agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)
