#!/usr/bin/env python3
"""Bounded public reads for the 2026-09-09 Torquantis interoperability request."""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import urllib.request

MCP = "https://torquantis.com/mcp"
BOARD = "https://gofrantic.com/v1/board"
ALLOW_TOOLS = {"list_markets", "get_orderbook"}
UA = "AstraNL/1.0 public-read-only coordination research"
READS = []


def exchange(url, payload=None):
    if url not in {MCP, BOARD}:
        raise ValueError("Endpoint is outside this bounded read-only probe")
    headers = {"User-Agent": UA, "Accept": "application/json, text/event-stream"}
    if payload is not None:
        if url != MCP:
            raise ValueError("Only MCP public reads use POST")
        method = payload["method"]
        if method not in {"initialize", "tools/call"}:
            raise ValueError("MCP method is not a permitted read")
        if method == "tools/call" and payload["params"]["name"] not in ALLOW_TOOLS:
            raise ValueError("MCP tool is not a permitted public read")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=None if payload is None else json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        raw = response.read(500001)
        if len(raw) > 500000:
            raise ValueError("Response exceeds the evidence bound")
        if response.status != 200:
            raise ValueError("Public read did not return HTTP 200")
        text = raw.decode("utf-8")
        if text.lstrip().startswith("{"):
            value = json.loads(text)
        else:
            messages = [json.loads(line[6:]) for line in text.splitlines() if line.startswith("data: ")]
            matching = [x for x in messages if x.get("id") == payload["id"]]
            if len(matching) != 1:
                raise ValueError("MCP response is missing or ambiguous")
            value = matching[0]
        if "error" in value or value.get("result", {}).get("isError"):
            raise ValueError("Remote read reported an error")
        READS.append({"url": url, "request": payload, "http_status": response.status,
                      "sha256_raw_response": hashlib.sha256(raw).hexdigest(),
                      "bytes": len(raw), "observed_at": dt.datetime.now(dt.timezone.utc).isoformat()})
        return value


def mcp(name, args):
    result = exchange(MCP, {"jsonrpc": "2.0", "id": len(READS) + 1, "method": "tools/call",
                            "params": {"name": name, "arguments": args}})["result"]
    texts = [x["text"] for x in result.get("content", []) if x.get("type") == "text"]
    if len(texts) != 1:
        raise ValueError("Expected one JSON content result")
    return json.loads(texts[0])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path)
    options = parser.parse_args()
    initialized = exchange(MCP, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2024-11-05", "capabilities": {},
        "clientInfo": {"name": "astranl-readonly-coordination", "version": "1.0"}}})["result"]
    markets = mcp("list_markets", {})
    if not isinstance(markets, list) or not markets:
        raise ValueError("Missing market snapshot; cannot infer zero demand")
    summaries = []
    for market in markets:
        stats = market["stats"]
        for key in ("best_bid_usdc", "best_ask_usdc", "trades_24h", "open_jobs"):
            if key not in stats:
                raise ValueError("Missing market field: " + key)
        summaries.append({"market": market["id"], **stats})
    books = [mcp("get_orderbook", {"market": name, "depth": 5})
             for name in ("research-brief", "code-task", "web-fetch")]
    for book in books:
        if not all(isinstance(book.get(key), list) for key in ("bids", "asks", "trades")):
            raise ValueError("Incomplete order book; cannot infer zero demand")
    board_result = exchange(BOARD)
    if board_result.get("ok") is not True:
        raise ValueError("Frantic board did not report success")
    board = board_result["board"]
    report = {"case": "torquantis-frantic-interoperability", "read_only": True,
              "mcp_server": initialized["serverInfo"], "market_summaries": summaries,
              "sampled_orderbooks": books,
              "frantic": {"open_bounties": [{k: x[k] for k in
                            ("number", "title", "price_usd", "funded", "claim_slots", "actions")}
                           for x in board["open_bounties"]]},
              "claim_limits": {"private_rfqs_not_read": True, "asks_are_not_buyer_demand": True,
                               "house_trades_are_not_independent_demand": True,
                               "no_assignment_or_payment_operation": True}, "reads": READS}
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if options.output:
        options.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
