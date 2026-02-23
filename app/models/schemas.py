from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    app_name: str
    debug: bool


class JobSearchRequest(BaseModel):
    query: str
    work_from_home: bool = True


class AgentResponse(BaseModel):
    response: str
