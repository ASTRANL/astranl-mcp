# Contributing to AstraNL

This repository is the public listing of the AstraNL MCP server: the README, registry metadata and the AstraLock tree-head log. The server itself runs at `https://astranl.com/mcp/streamable`; its source code is not in this repository.

## Report a broken tool

Open an issue with the **Broken tool report** form and give:

- the tool name exactly as `tools/list` returns it, for example `nl_municipal_build_rules`;
- the exact input (the arguments you sent);
- the output or error you received, including any request or receipt id;
- what you expected, and the source that shows it, for example the official register or regulation page;
- your client and when it happened (UTC).

Issues are public. Remove personal data, API keys and agent keys before you post.

## Propose a tool

Open an issue with the **Tool request** form. Describe the real task an agent has to do, who needs the result, and the official source the answer must come from. A tool is added only when a real, named source backs it and its limits can be stated.

## Truth rules

AstraNL publishes only what it can show. Contributions follow the same rules:

- **No fake data.** No invented companies, KvK or VAT numbers, prices, cases, users, reviews, payments or stars. Use real public examples or values clearly marked as test values.
- **Cite the source.** A report that a tool is wrong needs the official source that shows the right answer.
- **Unknown stays unknown.** When a source does not say something, the answer is UNKNOWN, not a guess.
- **No personal data of other people** in issues, examples or pull requests.
- **Wording.** The words AstraNL never uses about itself are listed as `forbidden_words` in the canonical facts: https://astranl.com/.well-known/astranl-facts.json

## Pull requests

`README.md` and `astralock/` are written by automation, so edits there are overwritten; propose changes to them in an issue. For anything else, open an issue first so the change can be checked against the live server.

## Security

Do not report a vulnerability in a public issue. See [SECURITY.md](SECURITY.md).
