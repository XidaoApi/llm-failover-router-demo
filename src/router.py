import os
import time
from dataclasses import dataclass
from typing import Callable, Iterable

from openai import OpenAI


@dataclass
class Route:
    name: str
    model: str
    timeout: float


def build_client() -> OpenAI:
    return OpenAI(
        api_key=os.environ['OPENAI_API_KEY'],
        base_url=os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
        timeout=float(os.getenv('REQUEST_TIMEOUT_SECONDS', '25')),
    )


def chat_once(client: OpenAI, route: Route, prompt: str) -> str:
    response = client.chat.completions.create(
        model=route.model,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ''


def try_routes(prompt: str, routes: Iterable[Route], on_error: Callable[[str, Exception], None] | None = None) -> tuple[str, str]:
    client = build_client()
    last_error = None
    for route in routes:
        try:
            started = time.time()
            text = chat_once(client, route, prompt)
            elapsed = round(time.time() - started, 2)
            return route.name, f"[{route.name} in {elapsed}s]\n{text}"
        except Exception as exc:  # demo-level broad catch
            last_error = exc
            if on_error:
                on_error(route.name, exc)
    raise RuntimeError(f'All routes failed; last error: {last_error}')


def healthcheck(model: str) -> bool:
    client = build_client()
    try:
        client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': 'Reply with the single word: ok'}],
            temperature=0,
            max_tokens=5,
        )
        return True
    except Exception:
        return False
