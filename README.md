# astranl-mcp

[![astranl-mcp MCP server](https://glama.ai/mcp/servers/vxwvj77twe/badges/score.svg)](https://glama.ai/mcp/servers/vxwvj77twe)

AstraNL MCP Server — verified human hands for AI agents.

An agent opens an errand in the PHYSICAL world (inspect a car before purchase,
view a property, collect or deliver an item, verify something on site). The
proof criterion is agreed BEFORE the work; Stripe holds the budget; a
register-verified executor delivers the proof; the principal confirms and only
then is the money captured. AstraNL brokers at a published fee and never holds
funds. This is not insurance.

Ordering is open worldwide. Execution happens where a register-verified
executor stands — today the Netherlands (KvK). No country is claimed before an
executor stands in it.

Public capabilities: `astranl_execute`, `astranl_procure`, `astranl_verify`,
`astranl_find`, `astranl_coordinate` (plus `search`, `fetch` and
`compose_parts_basket`).

## Live metrics (auto-refreshed daily 02:00 UTC; last refresh 2026-08-23)

- **API version:** v4.0
- **OpenAPI paths exposed:** 987
- **MCP tools advertised:** 8
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
- OpenAPI 3.1.0 spec: https://astranl.com/openapi.json (987 paths)
- Public docs: https://astranl.com/docs
- Federation node: https://astranl.com/.well-known/astranl-node.json

_This README is regenerated daily by `github_repo_auto_refresher.py` from live metrics. No marketing claims, only measured numbers._
