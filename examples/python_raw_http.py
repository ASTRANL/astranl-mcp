#!/usr/bin/env python3
"""Zero-dependency AstraNL MCP client (Python 3.8+ standard library only).

Flow: initialize -> notifications/initialized -> tools/list -> one read-only tools/call.
No API key, no account. The default call is estimate_cost, which is read-only.

Usage:
  python3 python_raw_http.py
  python3 python_raw_http.py nl_municipal_build_rules '{"municipality": "Amsterdam", "bouwkosten_eur": 12000}'
  ASTRANL_MCP_URL='https://astranl.com/mcp/streamable?profile=counterparty' python3 python_raw_http.py
"""
import json
import os
import sys
import time
import urllib.request

URL = os.environ.get("ASTRANL_MCP_URL", "https://astranl.com/mcp/streamable")


class MCP:
    def __init__(self, url):
        self.url = url
        self.session_id = None   # sent back if the server issues one
        self.protocol = None     # negotiated protocol version
        self.next_id = 0

    def _post(self, payload):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        if self.protocol:
            headers["MCP-Protocol-Version"] = self.protocol
        req = urllib.request.Request(self.url, data=json.dumps(payload).encode(),
                                     headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            self.session_id = resp.headers.get("Mcp-Session-Id") or self.session_id
            body = resp.read().decode("utf-8")
            ctype = resp.headers.get("Content-Type", "")
        if not body.strip():
            return None                      # notifications get 202 with no body
        if "text/event-stream" in ctype:     # the server may answer as SSE
            events = [line[5:].strip() for line in body.splitlines() if line.startswith("data:")]
            return json.loads(events[-1]) if events else None
        return json.loads(body)

    def request(self, method, params=None):
        self.next_id += 1
        msg = {"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params or {}}
        reply = self._post(msg)
        if reply is None or "error" in reply:
            raise RuntimeError("%s failed: %r" % (method, reply))
        return reply["result"]

    def notify(self, method):
        self._post({"jsonrpc": "2.0", "method": method})


def main():
    tool = sys.argv[1] if len(sys.argv) > 1 else "estimate_cost"
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {
        "category": "painting", "area_m2": 40, "location": "Haarlem"}

    mcp = MCP(URL)
    t0 = time.time()
    init = mcp.request("initialize", {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "python-raw-http-example", "version": "1.0"},
    })
    mcp.protocol = init.get("protocolVersion")
    mcp.notify("notifications/initialized")
    print("server:", init["serverInfo"], "protocol:", mcp.protocol,
          "session:", "stateful" if mcp.session_id else "stateless",
          "(%d ms)" % ((time.time() - t0) * 1000))

    tools, cursor = [], None
    while True:
        page = mcp.request("tools/list", {"cursor": cursor} if cursor else {})
        tools += page.get("tools", [])
        cursor = page.get("nextCursor")
        if not cursor:
            break
    read_only = [t["name"] for t in tools if (t.get("annotations") or {}).get("readOnlyHint")]
    print("tools: %d total, %d marked readOnlyHint" % (len(tools), len(read_only)))

    t1 = time.time()
    result = mcp.request("tools/call", {"name": tool, "arguments": args})
    text = "".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")
    print("tools/call %s isError=%s (%d ms)" % (tool, result.get("isError"), (time.time() - t1) * 1000))
    try:
        data = json.loads(text)              # AstraNL tools return JSON inside a text block
    except ValueError:
        print(text[:1500])
        return
    est = data.get("estimate") if isinstance(data, dict) else None
    if est:
        keys = ("category", "area_m2", "labor_hours", "labor_rate", "location_mult",
                "labor_cost", "material_cost", "total", "timeline_days")
        print(json.dumps({k: est.get(k) for k in keys}, indent=2))
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    main()
