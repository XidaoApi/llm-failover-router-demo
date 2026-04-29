import os

from src.router import Route, healthcheck, try_routes

PROMPT = 'Give a concise rollout checklist for routing some AI traffic to a backup model.'


if __name__ == '__main__':
    primary_model = os.getenv('PRIMARY_MODEL', 'gpt-4.1-mini')
    fallback_model = os.getenv('FALLBACK_MODEL', 'gpt-4o-mini')
    health_model = os.getenv('HEALTHCHECK_MODEL', primary_model)

    routes = []
    if healthcheck(health_model):
        routes.append(Route('healthy-primary', primary_model, timeout=25))
    routes.append(Route('fallback', fallback_model, timeout=25))

    route_name, output = try_routes(PROMPT, routes)
    print(f'served_by={route_name}')
    print(output)
