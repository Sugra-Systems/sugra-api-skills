---
name: using-sugra-api
description: Work with the Sugra API from any agent over HTTPS or MCP. Use when the task needs data from markets, macro, entities, news, climate, maritime, government, or network. Start here for the map of surfaces, then connect, discover, and call.
---

# Using the Sugra API

Sugra API is intelligence infrastructure. One product, two complete ways in. Domain-agnostic. Do not frame it through one vertical.

Public hedge (do not treat as a live count): 1,500+ endpoints, 160+ primary sources, 36 domains. Live counts: `GET https://sugra.ai/stats` and skill `live-docs`.

## Two complete surfaces

| Surface | When it is the right tool | How |
|---|---|---|
| HTTPS API `https://sugra.ai` | The agent can GET/POST a URL | `x-api-key` on `/api/v1/...` |
| MCP | The host is an MCP client (ChatGPT, claude.ai, Claude Desktop, Claude Code, Cursor, Gemini CLI, VS Code, Grok, ...) | hosted `https://mcp.sugra.ai/mcp` or local `sugra-api-mcp` |

Both reach the same API. Both need a key from https://app.sugra.ai/settings/billing (Free: 50 requests/day). Do not log the key. Do not put it in a skill file, commit, or chat.

Use the surface the host already has. If the host can do HTTP, use HTTP. If the host is already an MCP client, use MCP. If the user named one, use that one. Do not add MCP to skip HTTP, and do not skip MCP when it is already connected.

## Skill map

| Need | Skill |
|---|---|
| Where live docs and counts live | `live-docs` |
| How to attach HTTP, hosted MCP, stdio, self-host, each client | `connect` |
| Key, plans, 401/429, Bearer vs `x-api-key` | `auth-and-quota` |
| Find an operation and call it (HTTP and MCP) | `discover-and-call` |
| `{data, meta}`, sources, clocks, MCP shaping | `envelope-and-attribution` |
| Two or three domains in one answer | `cross-domain-briefing` |

## Minimal examples

HTTP:

```
GET https://sugra.ai/api/v1/etf/sectors/relative-strength?window=1m
x-api-key: sugra_...
```

MCP (after connect): `search_endpoints` then `describe_endpoint` then `call_endpoint` (or `fetch_data` for a one-shot). Hosted also has `resolve_entity`, `get_snapshot`, `get_timeseries`. Stdio does not.
