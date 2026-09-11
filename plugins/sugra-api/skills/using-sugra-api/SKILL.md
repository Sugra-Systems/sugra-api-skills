---
name: using-sugra-api
description: Call the Sugra API over HTTPS from any agent. Use when the task needs live data from markets, macro, entities, news, climate, maritime, or government. Default path is HTTP to sugra.ai. MCP is optional.
---

# Using the Sugra API

Sugra API is intelligence infrastructure. One HTTPS API, one key, 1,500+ endpoints across 160+ primary sources and 36 domains. Domain-agnostic. Do not frame it through one vertical.

The default way to use it is a direct HTTP call. Any agent that can GET/POST a URL can use Sugra. Do not add an MCP server unless the client cannot call HTTPS (ChatGPT connector UI) or the user already asked for MCP.

## Base URL and key

- Base: `https://sugra.ai`
- Data calls: `https://sugra.ai/api/v1/...`
- Header: `x-api-key: sugra_...`
- Free key: https://app.sugra.ai/settings/billing (50 requests/day)

Do not log the key. Do not put it in a skill file, commit, or chat.

## Public system endpoints (no key)

| Path | What it is |
|---|---|
| `GET /health` | liveness |
| `GET /about` | product surface |
| `GET /services` | service list |
| `GET /sources` | source families |
| `GET /openapi.json` | full operation list |

## First data call

```
GET https://sugra.ai/api/v1/etf/sectors/relative-strength?window=1m
x-api-key: sugra_...
```

Parse `{data, meta}`. Cite `meta` (source and `data_time`). Read quota headers. Details: skills `discover-and-call`, `auth-and-quota`, `envelope-and-attribution`.

## When MCP is the right tool

Only if the host cannot call HTTPS itself, or the user already connected `https://mcp.sugra.ai/mcp`. Then read skill `mcp-connector`. Otherwise stay on HTTP.
