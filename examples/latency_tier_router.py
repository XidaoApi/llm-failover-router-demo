import os

from src.router import Route, try_routes

LOW_RISK_PROMPT = 'Summarize the benefit of routing low-risk AI tasks to a cheaper tier in 2 sentences.'
HIGHER_RISK_PROMPT = 'Write a cautious deployment note about LLM fallback and observability in 4 bullet points.'


def run(prompt: str, prefer_fast: bool) -> None:
    fast_model = os.getenv('FALLBACK_MODEL', 'gpt-4o-mini')
    strong_model = os.getenv('PRIMARY_MODEL', 'gpt-4.1-mini')
    routes = [
        Route('fast-tier', fast_model, timeout=20),
        Route('strong-tier', strong_model, timeout=25),
    ] if prefer_fast else [
        Route('strong-tier', strong_model, timeout=25),
        Route('fast-tier', fast_model, timeout=20),
    ]

    route_name, output = try_routes(prompt, routes)
    print(f'served_by={route_name}')
    print(output)


if __name__ == '__main__':
    run(LOW_RISK_PROMPT, prefer_fast=True)
    print('---')
    run(HIGHER_RISK_PROMPT, prefer_fast=False)
