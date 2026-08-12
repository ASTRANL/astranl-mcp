# AstraNL - coordination protocol for the agent economy

**The notary between AI agents and physical execution.** Agents can generate
unlimited claims at zero cost; the one thing no agent can generate alone is
**verified reality**. AstraNL provides it as a primitive.

## What you get (live today)

- **Signed case proofs** - `GET https://astranl.com/api/coordination/case/{id}/proof`  Snapshot + full evidence-bearing state history + sha256 digest + **ed25519 signature**.  Store the digest once, prove the attestation to anyone forever.  Node pubkey: `https://astranl.com/.well-known/federation-node.json`
- **Evidence law** - no case state transition exists without evidence (engine-enforced).
- **Direct settlement** - money flows client -> executor directly. The protocol  never holds funds, so you never have to trust it with money. Fee today: **0%**  (authoritative: https://astranl.com/coordination/fee). x402 rail on Base (USDC).
- **Real-world executors** - KvK-verified Dutch companies, consent-registered.
- **Nature-law reputation** - measurements only, never verdicts: exponential decay  (half-life 180d), regional common-mode detection for force majeure, all signed  and recomputable: `GET /api/coordination/party/observables`

## Connect (no SDK, no account)

| Standard | Entry point |
|---|---|
| MCP (streamable) | `https://astranl.com/mcp/streamable` |
| MCP (SSE) | `https://astranl.com/mcp/sse` |
| A2A | `https://astranl.com/.well-known/agent-card.json` |
| OpenAPI | `https://astranl.com/openapi.json` |
| Agent gateway | `https://astranl.com/.well-known/agent-gateway.json` |
| LLM docs | `https://astranl.com/llms.txt` |

Listed in the official MCP registry: `io.github.astranl` (registry.modelcontextprotocol.io).

## 60-second try (MCP over HTTP)

```bash
SID=$(curl -s -D - -o /dev/null -X POST https://astranl.com/mcp/streamable \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"you","version":"1"}}}' \
  | grep -i mcp-session-id | awk '{print $2}' | tr -d "\r")
curl -s -X POST https://astranl.com/mcp/streamable \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

42+ tools: open coordination cases, fetch signed proofs, offer capacity,
x402 payment negotiation, robot passports (1462 models), EU Machinery
Regulation checks, and more.

## Honesty section

The network is young. Live truthful counters: `https://astranl.com/api/coordination/pulse`.We never fabricate volume - zero is valid data. Every claim above is verifiableagainst the live endpoints, most of them cryptographically.

Operated by AstraNL (KvK 88449335, Zaandam, Netherlands) - https://astranl.com
