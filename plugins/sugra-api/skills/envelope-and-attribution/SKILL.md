---
name: envelope-and-attribution
description: Parse Sugra API payloads over HTTPS or MCP, keep source attribution, and tell observation time from request time. Use when reading a response, citing a figure, or shaping a large payload.
license: MIT
metadata:
  author: Sugra Systems, Inc.
---

# Envelope and attribution

The API is LLM-friendly: one JSON envelope on every direction. Envelope detail also lives on https://docs.sugra.ai.

Most responses:

```json
{
  "data": {},
  "meta": {
    "endpoint": "/api/v1/...",
    "data_time": "2026-06-12T19:30:00Z",
    "response_time": "2026-06-12T19:30:01Z",
    "provider": "Sugra API"
  }
}
```

Some payloads are envelope-less (a flat object with `meta` or `_meta` on the same record). Provenance keys still apply.

HTTP: this JSON body plus `X-RateLimit-*` headers.

MCP: `call_endpoint` / `fetch_data` return the same payload (a top-level array is wrapped as `{data: ...}`). Shaping args `limit`, `fields`, `include_raw` apply to `data`. `meta.shaped` reports `fields_applied`, `fields_unmatched`, `limit_applied`. `limit` bounds only the top-level list.

## Time

`meta.data_time` is the observation or publication clock of the data, not the HTTP response time. A row-level `as_of` is the period the figure is about. Quote both when they differ. Do not describe a delayed series as a live tick.

## Attribution

Every figure needs a source and an as-of. Read them from `meta` / `_meta`. Live list: https://sugra.ai/sources (MCP resource `sugra://attribution`).

- Sovereign, intergovernmental, and academic sources are named openly (for example FRED, IMF, ECB, NOAA, World Bank, SEC EDGAR).
- Commercial upstreams appear under Sugra-branded wrappers (Sugra Finance, Sugra News, Sugra Crypto, Sugra Forex, Sugra Weather). Do not substitute a commercial vendor name.

This is data presentation, not investment, legal, or compliance advice. Screening tools return a signal, not a determination.
