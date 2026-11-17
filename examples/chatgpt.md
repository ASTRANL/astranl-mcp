# AstraNL in ChatGPT

AstraNL is a remote MCP server. Connector URL:

```
https://astranl.com/mcp/streamable
```

Authentication: none. Smaller tool sets: append `?profile=protocol` (18 tools) or
`?profile=counterparty` (4 tools) to the URL. Counts as observed on 2026-11-17.

## Add it as a custom MCP server

OpenAI's guide for custom MCP servers in ChatGPT, read on 2026-11-17, describes these steps. ChatGPT menus
change over time; follow the current guide if the labels differ:
https://developers.openai.com/api/docs/guides/custom-mcp-server

1. Open ChatGPT Plugins at chatgpt.com/plugins.
2. Select the plus button, then Add custom MCP server.
3. Enter a name, for example AstraNL, and optionally a description.
4. Under Connection, enter the server URL above.
5. Set authentication to No authentication.
6. Review the risk warning, confirm, and select Create as a plugin.

The guide lists SSE and streaming HTTP as supported transports. The URL above is the
streaming HTTP endpoint; the older SSE endpoint is `https://astranl.com/mcp/sse`.

## What ChatGPT will ask you to approve

Per the same guide, ChatGPT honors the MCP `readOnlyHint` annotation and treats tools without
it as write actions that need your confirmation. AstraNL marks 28 of its 41 tools read-only,
for example `estimate_cost`, `nl_municipal_build_rules`, `check_counterparty_nl`,
`construction_summary`, `search` and `fetch`. The other 13, such as `create_task`,
`order_materials`, `commitment_attest`, `record_counterparty_check` and `read_with_receipt`,
create a record or a log entry, so ChatGPT asks before running them.

## Try it

- What does it cost to paint 40 m2 of interior walls in Haarlem?
- What permit fee does Amsterdam charge for a dakkapel with 12000 EUR bouwkosten?
- Check KvK 17001910 with the name Koninklijke Philips N.V. before I approve a supplier.

The steps above were not executed against a ChatGPT account in this check; the server side
was checked with the live handshake in `python_raw_http.py` and `transcripts/`.
