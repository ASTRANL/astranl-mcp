# astranl-mcp

[![astranl-mcp MCP server](https://glama.ai/mcp/servers/vxwvj77twe/badges/score.svg)](https://glama.ai/mcp/servers/vxwvj77twe)

AstraNL MCP Server — verified human hands for AI agents.

AstraNL turns an intent into verified real-world execution: a KvK-registered executor (verification state on its public card) performs the errand; the principal's card hold sits on that executor's own Stripe account and is captured only after the principal confirms the proof agreed before the work; AstraNL receives only its coordination fee.

Money: broker; custody never - the principal's card is authorised (hold) on the executor's own Stripe account (destination charge, executor = payee and merchant of record); captured only after the principal confirms the agreed proof; AstraNL receives only its coordination fee as application fee and never holds third-party funds; contract: https://astranl.com/.well-known/payment-truth.json; an unconfirmed hold auto-releases after 7 days. This is not insurance.

Geography: ordering open to a principal anywhere; execution Netherlands, where KvK-registered executors stand (registry ID checked; each executor's verification state is shown on its card at /truth/executors.json - never a bare "verified"). a country is listed the day a registry-checked, payout-ready executor stands in it, never before.

Public capabilities: `astranl_execute`, `astranl_procure`, `astranl_verify`, `astranl_find`, `astranl_coordinate`, `search`, `fetch`, `compose_parts_basket`.

Canonical source of truth for every channel: https://astranl.com/.well-known/astranl-facts.json (canon block, generated 2026-09-01T01:32:49.521460+00:00).

## Live metrics (auto-refreshed daily 02:00 UTC; last refresh 2026-09-01)

- **API version:** v4.0
- **OpenAPI paths exposed:** 1030
- **MCP tools advertised:** 6
- **Dispatchable task classes:** 29
- **Listed on canonical [MCP Registry](https://registry.modelcontextprotocol.io/v0/servers?search=astranl):** 10 version(s)
- **Listed on Smithery:** ✗
- **Listed on:** Glama (pending)

## Quick start

### Smithery (one-line install)

```bash
npx -y smithery mcp add t-oleg-m/astranl
npx -y smithery tool list t-oleg-m/astranl
```

### Direct MCP SSE

```
Server (streamable HTTP): https://astranl.com/mcp/streamable
Legacy SSE fallback: https://astranl.com/mcp/sse
Server card: https://astranl.com/.well-known/mcp/server-card.json
```

### Direct REST

```bash
curl -X POST https://astranl.com/capabilities/dispatch \
     -H 'X-Agent-Key: YOUR_KEY' \
     -H 'Content-Type: application/json' \
     -d '{"task_class":"detect_language","input":"Bonjour"}'
```

## Pricing manifest

Live at https://astranl.com/capabilities/dispatch/manifest

## Provider

- **Organisation:** AstraNL
- **Jurisdiction:** Netherlands (KvK 88449335, BTW NL004604224B69)
- **Compliance:** EU-AI-Act, GDPR, Wwft
- **Liability:** transition period — no active platform cover; task value limited to €500; replacement cover in progress. Canonical, always-current: https://astranl.com/.well-known/astranl-facts.json
- **License:** Apache-2.0

## Discovery

- A2A agent card: https://astranl.com/.well-known/agent.json
- OpenAPI 3.1.0 spec: https://astranl.com/openapi.json (1030 paths)
- Public docs: https://astranl.com/docs
- Federation node: https://astranl.com/.well-known/astranl-node.json

_This README is regenerated daily by `github_repo_auto_refresher.py` from live metrics. No marketing claims, only measured numbers._
