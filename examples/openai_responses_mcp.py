"""AstraNL as a remote MCP tool in the OpenAI Responses API.

Requires: pip install openai   (field names checked against openai 3.53.0:
openai/types/responses/tool_param.py, class Mcp)
Environment: OPENAI_API_KEY; optionally OPENAI_MODEL.

require_approval "never" is used together with allowed_tools, so the model can only
reach tools that AstraNL itself marks readOnlyHint=true. Do not add record-creating
tools such as create_task, order_materials or commitment_attest to allowed_tools
without an approval step.
"""
import os

from openai import OpenAI

# Any Responses API model that supports the remote MCP tool; this default is a placeholder.
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")

READ_ONLY_TOOLS = [
    "ask_astranl",
    "estimate_cost",
    "nl_municipal_build_rules",
    "check_counterparty_nl",
    "construction_summary",
    "construction_permits",
]

client = OpenAI()

response = client.responses.create(
    model=MODEL,
    tools=[
        {
            "type": "mcp",
            "server_label": "astranl",
            "server_description": "Dutch construction, cost, permit-fee and counterparty checks with sources.",
            "server_url": "https://astranl.com/mcp/streamable",
            "allowed_tools": READ_ONLY_TOOLS,
            "require_approval": "never",
        }
    ],
    input=(
        "What is a planning cost figure for painting 40 m2 of interior walls in Haarlem, "
        "and what is the Amsterdam permit fee (leges) for a dakkapel with 12000 EUR bouwkosten? "
        "Quote the sources AstraNL returns."
    ),
)

print(response.output_text)
