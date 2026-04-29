import os

from src.router import Route, try_routes

PROMPT = 'In 3 bullet points, explain why graceful LLM failover matters in production.'


def log_error(route_name: str, exc: Exception) -> None:
    print(f'route failed: {route_name}: {exc}')


if __name__ == '__main__':
    primary = Route('primary', os.getenv('PRIMARY_MODEL', 'gpt-4.1-mini'), timeout=25)
    fallback = Route('fallback', os.getenv('FALLBACK_MODEL', 'gpt-4o-mini'), timeout=25)
    route_name, output = try_routes(PROMPT, [primary, fallback], on_error=log_error)
    print(f'served_by={route_name}')
    print(output)
