# llm-failover-router-demo

OpenAI-compatible routing and failover examples for teams that want a practical starting point for reliability work: fallback between models, health-aware routing, retry boundaries, and a simple latency/cost-minded strategy.

Repo: https://github.com/XidaoApi/llm-failover-router-demo
Related assets:
- https://github.com/XidaoApi/xidao-python-examples
- https://github.com/XidaoApi/xidao-nodejs-examples
- https://github.com/XidaoApi/xidao-cookbook
- https://github.com/XidaoApi/llm-provider-migration-checklist

## Why this exists

Switching or multi-homing LLM traffic is not just about changing `base_url`. In production, reliability usually depends on:
- timeouts and retry boundaries
- fallback model selection
- health checks before routing more traffic
- partial degradation instead of full outages
- visibility into which backend actually served the request

This repo gives a minimal Python-first reference for those patterns using the OpenAI SDK with an OpenAI-compatible endpoint.

## What’s inside

- `examples/basic_fallback.py` — try a primary model first, then fail over cleanly
- `examples/health_aware_router.py` — route around unhealthy targets based on a cheap probe
- `examples/latency_tier_router.py` — prefer a fast/cheap tier for low-risk traffic and escalate when needed
- `src/router.py` — reusable tiny router helpers
- `.env.example` — XiDao/OpenAI-compatible configuration

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python examples/basic_fallback.py
```

## Environment

```env
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=https://global.xidao.online/v1
PRIMARY_MODEL=gpt-4.1-mini
FALLBACK_MODEL=gpt-4o-mini
HEALTHCHECK_MODEL=gpt-4.1-mini
REQUEST_TIMEOUT_SECONDS=25
```

## Reliability notes

1. Keep fallback explicit rather than letting all failures silently retry forever.
2. Separate *provider unavailable* from *bad prompt / bad request* errors.
3. Probe health with cheap, short prompts before shifting more traffic.
4. Log which route was chosen so debugging and cost analysis stay possible.
5. Use this as a demo scaffold; real systems usually add circuit breakers, budgets, and tracing.

## XiDao fit

If you already use the OpenAI SDK, you can adapt these examples with a compatible `base_url` and model mapping. That makes this repo useful for:
- migration testing
- backup routing experiments
- latency-aware workload splitting
- showing teams how to reduce outage blast radius

## Suggested next extensions

- add streaming fallback handling
- add JSON-mode/schema validation fallback
- add provider-specific error classification
- add Prometheus/OpenTelemetry instrumentation

## License

MIT
