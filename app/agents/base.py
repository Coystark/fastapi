import logging
from collections.abc import Callable, Coroutine
from typing import Any

from google.genai import types

from app.adapters.gemini import get_client

logger = logging.getLogger("app")

ToolFunction = Callable[..., Coroutine[Any, Any, dict]]

MAX_ITERATIONS = 10


class BaseAgent:
    """Gemini agent that loops over tool calls until it produces a final text
    response.  Subclass or instantiate with different tools / system prompts to
    create specialised agents."""

    def __init__(
        self,
        *,
        system_instruction: str,
        tools: list[types.Tool],
        tool_functions: dict[str, ToolFunction],
        model: str = "gemini-2.5-flash",
    ) -> None:
        self.system_instruction = system_instruction
        self.tools = tools
        self.tool_functions = tool_functions
        self.model = model

    async def run(self, message: str) -> str:
        client = get_client()
        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            tools=self.tools,
        )
        contents: list[types.Content] = [
            types.Content(role="user", parts=[types.Part.from_text(text=message)])
        ]

        for _ in range(MAX_ITERATIONS):
            response = await client.aio.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )

            candidate = response.candidates[0]
            function_calls = [
                part for part in candidate.content.parts if part.function_call
            ]

            if not function_calls:
                return response.text or ""

            contents.append(candidate.content)

            fn_response_parts: list[types.Part] = []
            for part in function_calls:
                fc = part.function_call
                logger.info("Tool call: %s(%s)", fc.name, fc.args)
                result = await self._execute(fc.name, fc.args)
                fn_response_parts.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response=result,
                    )
                )

            contents.append(types.Content(parts=fn_response_parts))

        return "Maximum tool-call iterations reached."

    async def _execute(self, name: str, args: dict) -> dict:
        fn = self.tool_functions.get(name)
        if fn is None:
            return {"error": f"Unknown tool: {name}"}
        try:
            return await fn(**args)
        except Exception as exc:
            logger.exception("Tool '%s' failed", name)
            return {"error": str(exc)}
