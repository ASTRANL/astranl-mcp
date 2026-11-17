# AstraNL MCP examples

Copy-paste setups for connecting an agent or an MCP client to AstraNL. No API key, no account.

| Endpoint | What you get, as observed on 2026-11-17 |
|---|---|
| `https://astranl.com/mcp/streamable` | streamable HTTP, full set: 41 tools, serverInfo `astranl-mcp` 1.37.43 |
| `https://astranl.com/mcp/streamable?profile=protocol` | 18 protocol tools |
| `https://astranl.com/mcp/streamable?profile=counterparty` | 4 tools for checking a Dutch or EU counterparty |
| `https://astranl.com/mcp/sse` | legacy SSE transport; the first event is `endpoint` |

## Files

| File | What it is | How it was checked |
|---|---|---|
| [`python_raw_http.py`](python_raw_http.py) | Zero-dependency Python client: initialize, tools/list, one read-only tools/call | Executed on 2026-11-17, output below |
| [`claude-code.md`](claude-code.md) | `claude mcp add` commands, scopes and a `.mcp.json` form for Claude Code | Syntax from the Claude Code MCP docs; not executed |
| [`claude-desktop.json`](claude-desktop.json) | Claude Desktop config using the `mcp-remote` stdio bridge through `npx` | Arguments from the mcp-remote README, version 0.16.6; not executed |
| [`cursor-mcp.json`](cursor-mcp.json) | Cursor config for `.cursor/mcp.json` or `~/.cursor/mcp.json` | Format from the Cursor MCP docs; not executed |
| [`vscode-mcp.json`](vscode-mcp.json) | VS Code config for `.vscode/mcp.json` | Format from the VS Code MCP configuration reference; not executed |
| [`chatgpt.md`](chatgpt.md) | Adding AstraNL to ChatGPT as a custom MCP server | Steps from OpenAI's custom MCP server guide; not executed |
| [`openai_responses_mcp.py`](openai_responses_mcp.py) | OpenAI Responses API with the remote `mcp` tool, limited to read-only tools | Field names checked in the openai 3.53.0 package source; not executed, needs `OPENAI_API_KEY` |
| [`langchain_mcp_adapters.py`](langchain_mcp_adapters.py) | LangChain tools through `MultiServerMCPClient` with transport `streamable_http` | Names checked in the langchain-mcp-adapters 0.3.2 package source; not executed |
| [`transcripts/`](transcripts/) | Trimmed real JSON-RPC exchanges | Recorded on 2026-11-17; each file says what was trimmed |

The calls in this folder are read-only live calls made by the AstraNL maintainers to show
the interface. They are not customer jobs and they create no task, order or record.

## Live run of python_raw_http.py

```
$ python3 python_raw_http.py
server: {'name': 'astranl-mcp', 'version': '1.37.43'} protocol: 2025-06-18 session: stateless (131 ms)
tools: 41 total, 28 marked readOnlyHint
tools/call estimate_cost isError=False (267 ms)
{
  "category": "painting",
  "area_m2": 40.0,
  "labor_hours": 12.0,
  "labor_rate": 53.87,
  "location_mult": 1.0,
  "labor_cost": 646.44,
  "material_cost": 104.48,
  "total": 750.92,
  "timeline_days": 2
}
```

Observed at 2026-11-17T20:02:34Z. The figure is a planning cost in EUR for painting 40 m2 of
interior walls in Haarlem, not a quote. Labour is 12.0 h x 53.87 EUR x 1.0; AstraNL states that
it has no sourced regional factor for this work, so `location_mult` stays 1.0. The full result
also lists each material line with its price source; see
[`transcripts/estimate_cost_painting_haarlem.json`](transcripts/estimate_cost_painting_haarlem.json).

Any other read-only tool works the same way:

```bash
python3 python_raw_http.py nl_municipal_build_rules '{"municipality": "Amsterdam", "bouwkosten_eur": 12000}'
ASTRANL_MCP_URL='https://astranl.com/mcp/streamable?profile=counterparty' python3 python_raw_http.py check_counterparty_nl '{"kvk_number": "17001910", "company_name": "Koninklijke Philips N.V."}'
```

Both commands above were also run on 2026-11-17 and returned `isError=False`; the
counterparty profile listed 4 tools, 2 of them marked readOnlyHint.

## Protocol notes, as observed

- `initialize` with protocolVersion `2025-06-18` is accepted and echoed back.
- The server is stateless: it returns no `Mcp-Session-Id`, so there is no session to keep.
- Replies to POST come as `text/event-stream`, one `data:` event per reply; send
  `Accept: application/json, text/event-stream`. `notifications/initialized` gets HTTP 202.
- Tool results are JSON inside a single `text` content block; parse `content[0].text`.
- `tools/list` returned all tools in one page, with no `nextCursor`.

## Read-only and record-creating tools

From the tool annotations served on 2026-11-17, full endpoint.

Marked `readOnlyHint: true`, 28 tools:
ask_astranl, check_counterparty_nl, check_estimate_materials, check_material, check_task,
commitment_verify, construction_economy, construction_events, construction_laws,
construction_leadtimes, construction_natura, construction_permits, construction_summary,
construction_tenders, construction_zones, coordination_contract, estimate_case_status,
estimate_cost, fetch, find_offers, get_evidence, ground_astranl, machines_search,
market_indicators, network_door, nl_municipal_build_rules, search, verify_astranl.

Not marked read-only, 13 tools; they create a task, order, case, attestation or log entry:
commitment_attest, commitment_confirm, create_task, estimate_case_answer, estimate_case_create,
estimate_case_files, estimate_case_video, ground_citation, ground_component, housing_need,
order_materials, read_with_receipt, record_counterparty_check.

Clients that honor annotations, such as ChatGPT, ask before running the second group. If you
turn approvals off, as in `openai_responses_mcp.py`, limit the agent to the first group.

## Client notes

- Claude Desktop: merge `claude-desktop.json` into `claude_desktop_config.json`, on macOS in
  `~/Library/Application Support/Claude/`, on Windows in `%APPDATA%\Claude\`. It needs
  Node.js with `npx`.
- VS Code: the VS Code reference marks the `.vscode/mcp.json` format as part of a deprecated
  harness to be removed in February 2027 and recommends its newer `mcpServers` config files;
  see https://code.visualstudio.com/docs/copilot/reference/mcp-configuration
