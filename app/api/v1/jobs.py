from fastapi import APIRouter

from app.agents.jobs import create_jobs_agent
from app.models.schemas import AgentResponse, JobSearchRequest

router = APIRouter(tags=["jobs"])


@router.post("/jobs/search", response_model=AgentResponse)
async def search_jobs(request: JobSearchRequest) -> AgentResponse:
    agent = create_jobs_agent()

    message = f"Search for jobs: {request.query}"
    if request.work_from_home:
        message += "\nFilter: remote / work-from-home positions only"

    result = await agent.run(message)
    return AgentResponse(response=result)
