# AstraNL in Claude Code

AstraNL is a remote MCP server over streamable HTTP. No API key and no account are needed.

## Add the server

```bash
# full tool set, 41 tools when checked on 2026-11-17
claude mcp add --transport http astranl https://astranl.com/mcp/streamable

# or a smaller profile
claude mcp add --transport http astranl-protocol "https://astranl.com/mcp/streamable?profile=protocol"
claude mcp add --transport http astranl-counterparty "https://astranl.com/mcp/streamable?profile=counterparty"
```

Quote URLs that contain `?` so your shell does not expand them.

Scope: add `--scope user` to make AstraNL available in every project, or `--scope project`
to write it to `.mcp.json` in the project root so the whole team gets it. The default,
`local`, keeps it to you in the current project.

Project file form, `.mcp.json`:

```json
{
  "mcpServers": {
    "astranl": {
      "type": "http",
      "url": "https://astranl.com/mcp/streamable"
    }
  }
}
```

## Check it

```bash
claude mcp list
claude mcp get astranl
```

Inside a Claude Code session, `/mcp` shows the connection status.

## Try it

Ask in plain words, for example:

- What does it cost to paint 40 m2 of interior walls in Haarlem? Use AstraNL estimate_cost.
- What is the Amsterdam leges for a dakkapel with 12000 EUR bouwkosten? Use nl_municipal_build_rules.
- Check KvK 17001910 with the name Koninklijke Philips N.V. before I onboard them as a supplier.

The AstraNL server marks 28 of its 41 tools with `readOnlyHint: true`. Tools that create a
record, such as `create_task`, `order_materials`, `commitment_attest` or
`record_counterparty_check`, are not marked read-only; approve those only when you mean it.

Command syntax follows the Claude Code MCP documentation: https://code.claude.com/docs/en/mcp
