# astranl-mcp

[![astranl-mcp MCP server](https://glama.ai/mcp/servers/vxwvj77twe/badges/score.svg)](https://glama.ai/mcp/servers/vxwvj77twe)

AstraNL MCP Server — Dutch coordination broker. Routes AI tasks across
Anthropic, OpenAI, Gemini, and xAI Grok via measured decomposition strategies.
Flat per-task pricing €0.005-€0.05 (up to 65% cheaper than Claude Opus single-shot).

## Live metrics (auto-refreshed daily 02:00 UTC; last refresh 2026-08-08)

- **API version:** v4.0
- **OpenAPI paths exposed:** 837
- **MCP tools advertised:** 9
- **Dispatchable task classes:** 29
- **Listed on canonical [MCP Registry](https://registry.modelcontextprotocol.io/v0/servers?search=astranl):** 10 version(s)
- **Listed on Smithery:** ✓
- **Listed on:** Glama (pending)

## Quick start

### Smithery (one-line install)

```bash
npx -y smithery mcp add t-oleg-m/astranl
npx -y smithery tool list t-oleg-m/astranl
```

### Direct MCP SSE

```
Server: https://astranl.com/mcp/sse
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
- OpenAPI 3.1.0 spec: https://astranl.com/openapi.json (837 paths)
- Public docs: https://astranl.com/docs
- Federation node: https://astranl.com/.well-known/astranl-node.json

_This README is regenerated daily by `github_repo_auto_refresher.py` from live metrics. No marketing claims, only measured numbers._
