---
name: discover-and-call
description: Find the right Sugra API path and call it over HTTPS. Use when the path is unknown, before guessing parameter names, or when OpenAPI is the map. Do not invent routes.
---

# Discover and call

Do not invent paths or query names. The map is the live OpenAPI document.

## Loop (HTTP)

1. If the path is already known, skip to step 4.
2. `GET https://sugra.ai/openapi.json` (no key). Find an operation by `summary`, `tags`, or path. `GET https://sugra.ai/services` and `GET https://sugra.ai/sources` are the coarse map.
3. Read `parameters` and, for POST, `requestBody`. Required names come from the spec, not from memory.
4. Call `https://sugra.ai` with `x-api-key`. GET uses query params. POST uses JSON body plus any path/query params the spec lists.
5. Parse `{data, meta}`. Cite source and `data_time`. Read `X-RateLimit-Remaining`.

Example once the path is known:

```
GET https://sugra.ai/api/v1/etf/sectors/relative-strength?window=1m
x-api-key: sugra_...
```

A catalog miss is not "Sugra has no data". Widen the search terms. Try `/services` tags. Then OpenAPI again.

## Timeouts

30 seconds is enough for most GETs. Bulk or live-upstream POSTs can run longer. Do not treat a timeout as empty data.

## MCP shortcut (optional)

If the session already has Sugra MCP connected, `search_endpoints` then `describe_endpoint` then `call_endpoint` is the same loop over a bundled catalog. It is not required. Do not add per-endpoint MCP tools to skip this loop.
