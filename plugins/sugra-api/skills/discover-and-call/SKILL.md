---
name: discover-and-call
description: Find the right Sugra operation and call it over HTTPS or MCP. Use when the path or operation_id is unknown, before guessing parameter names, or when a catalog miss might be a bad query. Do not invent routes.
---

# Discover and call

Do not invent paths or `operation_id`s. Live map: skill `live-docs`. Two complete loops, same API.

## HTTP loop

1. If the path is already known, skip to step 4.
2. `GET https://sugra.ai/openapi.json` (no key). Find an operation by `summary`, `tags`, or path. `GET /services` and `GET /sources` are the coarse map.
3. Read `parameters` and, for POST, `requestBody`. Required names come from the spec.
4. Call `https://sugra.ai` with `x-api-key`. GET uses query params. POST uses JSON body plus any path/query params the spec lists.
5. Parse `{data, meta}`. Cite source and `data_time`. Read `X-RateLimit-Remaining`.

```
GET https://sugra.ai/api/v1/etf/sectors/relative-strength?window=1m
x-api-key: sugra_...
```

## MCP loop

Works on hosted (11 tools) and stdio (8 tools). Do not call hosted-only names on stdio.

1. `search_endpoints(query=..., toolset=None, source=None, limit=10)` - natural language. Unknown `toolset` / `source` returns `unknown_toolset` / `unknown_source` with the valid set, not an empty hit list.
2. Pick an `operation_id` from `results`. Do not invent ids.
3. `describe_endpoint(operation_id=...)` - params, `request_body_schema` on POST, `agent_hints` (`duration_class` fast/slow/heavy, `max_concurrency`, `bulk_cost`).
4. `call_endpoint(operation_id=..., params={...}, body=...)`.

`fetch_data(query=...)` is a one-shot shortcut. If it misses, fall back to the four-step loop. `list_toolsets` and `list_sources` (and resources `sugra://catalog/domains`, `sugra://catalog/sources`) are the map, not the query.

`call_endpoint` / `fetch_data` shaping: `limit`, `fields` (dotted paths), `include_raw`. `limit` bounds only the top-level list. `meta.shaped` reports what actually applied.

Hosted only: `resolve_entity`, `get_snapshot`, `get_timeseries`. For LEI/VAT identity and sanctions on every transport: `sugra_entity_lookup`, `sugra_entity_screen`.

Six MCP prompts (`market_snapshot`, `macro_briefing`, `sanctions_screening`, `sector_compare`, `earth_conditions`, `source_overview`) are numbered recipes over the eight gateway tools. They are not the catalog.

## Misses

A miss is not "Sugra has no data". Widen the query. Drop a bad `toolset`/`source` filter. If MCP search still misses, fetch live `/openapi.json` (the wheel catalog can lag). Then HTTP-call if the spec has it.

Do not add per-endpoint MCP tools to skip this loop.

## Timeouts

30 seconds covers most GETs. Bulk or live-upstream POSTs can run longer. MCP `agent_hints.duration_class` is the budget hint. Do not treat a timeout as empty data.
