from google.genai import types

from app.adapters.jsearch import search_jobs
from app.agents.base import BaseAgent

SYSTEM_INSTRUCTION = """\
You are a job search assistant specialized in finding job listings.

When the user provides a search query, use the search_jobs tool to find \
relevant positions. Present the results in a clear, organized format \
highlighting:
- Job title
- Company name
- Location (city/state/country)
- Whether it's remote
- Employment type
- A brief description
- Application link (when available)

Always respond in the same language as the user's query.\
"""

search_jobs_declaration = types.FunctionDeclaration(
    name="search_jobs",
    description="Search for job listings on various job boards and platforms",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "query": types.Schema(
                type=types.Type.STRING,
                description="Job search query (e.g. 'back-end developer', 'python engineer')",
            ),
            "work_from_home": types.Schema(
                type=types.Type.BOOLEAN,
                description="Filter for remote / work-from-home positions only",
            ),
            "country": types.Schema(
                type=types.Type.STRING,
                description="Country code for location filter (e.g. 'br', 'us')",
            ),
            "page": types.Schema(
                type=types.Type.INTEGER,
                description="Page number for pagination (starts at 1)",
            ),
            "num_pages": types.Schema(
                type=types.Type.INTEGER,
                description="Number of result pages to return",
            ),
            "date_posted": types.Schema(
                type=types.Type.STRING,
                description="Date filter: 'all', 'today', '3days', 'week', 'month'",
            ),
        },
        required=["query"],
    ),
)

search_jobs_tool = types.Tool(function_declarations=[search_jobs_declaration])


def create_jobs_agent() -> BaseAgent:
    return BaseAgent(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[search_jobs_tool],
        tool_functions={"search_jobs": search_jobs},
    )
