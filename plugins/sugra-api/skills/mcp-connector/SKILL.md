---
name: mcp-connector
description: Use Sugra MCP only when the host cannot call HTTPS or the user already connected it. Use when installing a connector, ChatGPT or claude.ai MCP, or a hosted-only tool name fails on stdio.
---

# MCP connector (optional)

Default path is HTTP to `https://sugra.ai` with `x-api-key`. Read `using-sugra-api` and `discover-and-call` first. Use this skill only when the host has no HTTP tool, or the user already pointed a client at hosted MCP.

## Hosted

```
https://mcp.sugra.ai/mcp
```

Permanent alias: `https://app.sugra.ai/mcp`. Auth: `Authorization: Bearer` (API key or OAuth). ChatGPT and claude.ai use the connector UI. They do not load SKILL.md from disk.

## Local package

```
pip install sugra-api-mcp
```

stdio, `SUGRA_API_KEY` in the server process. Eight gateway tools. Hosted adds three composed tools (`resolve_entity`, `get_snapshot`, `get_timeseries`) that do not exist on stdio. Do not call those three on a local session.

Gateway tools on every transport: `fetch_data`, `search_endpoints`, `describe_endpoint`, `call_endpoint`, `list_toolsets`, `list_sources`, `sugra_entity_screen`, `sugra_entity_lookup`.

Do not add per-endpoint MCP tools. Discovery is search, describe, call - or HTTP as in `discover-and-call`.
