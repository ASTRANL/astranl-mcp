# Security policy

## Reporting a vulnerability

Report security problems privately by email to **astranl@astranl.com**, the official address published in https://astranl.com/.well-known/astranl-facts.json. Do not open a public issue for a vulnerability.

Please include:

- the affected surface, for example `https://astranl.com/mcp/streamable`, a named tool, an API path or a page on astranl.com;
- steps to reproduce, with the exact request and response;
- the impact you observed.

Do not access, change or delete data that is not yours, do not degrade the service for others, and do not test against other people's accounts.

## Scope

- The public MCP server at `https://astranl.com/mcp/streamable` and the legacy SSE endpoint `https://astranl.com/mcp/sse`
- The public API described at https://astranl.com/openapi.json
- The files in this repository

## Supported versions

Only the live server is supported. Its current version is the one it reports in `serverInfo` on `initialize`.
