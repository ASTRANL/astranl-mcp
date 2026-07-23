# AstraNL MCP Server

[![astranl-mcp MCP server](https://glama.ai/mcp/servers/vxwvj77twe/badges/score.svg)](https://glama.ai/mcp/servers/vxwvj77twe)

AstraNL is a coordination platform in the Netherlands that gives AI agents a
way to act in the physical world through one MCP endpoint.

## Endpoint (remote, no install)

- **Streamable HTTP (recommended):** `POST https://astranl.com/mcp/streamable`
- Legacy SSE: `GET https://astranl.com/mcp/sse`
- Tool schemas: <https://astranl.com/mcp/tools.json>
- Live metrics (honest, pre-revenue shown as-is): <https://astranl.com/health>
- Registry name: `com.astranl/mcp` (official MCP Registry)

## Public tools

| Tool | What an agent gets |
|---|---|
| `create_task` | A real service task in NL: matched provider, escrow payment, released after client confirmation |
| `check_task` | Status of a task |
| `compose_parts_basket` | Brand- and size-matched purchase list for a trade job with live merchant prices and stock |
| `report_order_exception` | Returns / shortages / damage handled under the merchant own terms |
| `search` / `fetch` | Generic discovery over robots registry and merchant SKUs |
| `estimate_cost` | Human vs robot price band for a task category |
| `search_robots` | Robot registry lookup |

## Roles, honestly

AstraNL acts as a **coordination broker**: the client and the service provider
always contract directly with each other; payment is held in escrow until the
client confirms. Coordination fee: **1%** of paid tasks only - **0% until
31 August 2026**.

Operator: AstraNL (ZZP), KvK 88449335, Amsterdam, NL. EU jurisdiction
(GDPR, EU AI Act aligned).
