"""AstraNL tools in LangChain through langchain-mcp-adapters.

Requires: pip install langchain-mcp-adapters   (Python 3.10+; names checked against
langchain-mcp-adapters 0.3.2: MultiServerMCPClient, get_tools, StreamableHttpConnection
with transport "streamable_http")

The script loads the AstraNL tools as LangChain tools and calls one read-only tool
directly. Pass the same `tools` list to your own LangChain or LangGraph agent.
"""
import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    client = MultiServerMCPClient(
        {
            "astranl": {
                "transport": "streamable_http",
                "url": "https://astranl.com/mcp/streamable",
            }
        }
    )
    tools = await client.get_tools()
    print(len(tools), "tools:", ", ".join(sorted(t.name for t in tools)))

    by_name = {t.name: t for t in tools}
    result = await by_name["nl_municipal_build_rules"].ainvoke(
        {"municipality": "Amsterdam", "bouwkosten_eur": 12000}
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
