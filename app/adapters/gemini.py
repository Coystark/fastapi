from google import genai

from app.core.config import get_settings

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        settings = get_settings()
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


async def generate_content(
    prompt: str,
    model: str = "gemini-2.0-flash",
) -> str:
    client = _get_client()
    response = await client.aio.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text or ""
