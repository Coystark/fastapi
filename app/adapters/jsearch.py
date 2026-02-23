import httpx

from app.core.config import get_settings

JSEARCH_BASE_URL = "https://jsearch.p.rapidapi.com/search"


async def search_jobs(
    query: str,
    work_from_home: bool = True,
    page: int = 1,
    num_pages: int = 1,
    country: str = "br",
    date_posted: str = "all",
) -> dict:
    settings = get_settings()
    headers = {
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": settings.rapidapi_key,
    }
    params = {
        "query": query,
        "page": str(page),
        "num_pages": str(num_pages),
        "country": country,
        "date_posted": date_posted,
        "work_from_home": str(work_from_home).lower(),
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            JSEARCH_BASE_URL,
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        return _extract_jobs(response.json())


def _extract_jobs(data: dict) -> dict:
    """Keep only the fields Gemini needs to avoid blowing up the context."""
    jobs = []
    for job in data.get("data", []):
        description = job.get("job_description") or ""
        jobs.append(
            {
                "job_title": job.get("job_title"),
                "employer_name": job.get("employer_name"),
                "job_city": job.get("job_city"),
                "job_state": job.get("job_state"),
                "job_country": job.get("job_country"),
                "job_is_remote": job.get("job_is_remote"),
                "job_employment_type": job.get("job_employment_type"),
                "job_description": description[:500],
                "job_apply_link": job.get("job_apply_link"),
                "job_posted_at_datetime_utc": job.get("job_posted_at_datetime_utc"),
            }
        )
    return {"jobs": jobs, "total": len(jobs)}
