---
name: auth-and-quota
description: Authenticate to Sugra API and stay inside the daily request quota. Use when setting up a client, or when a call returns 401, 403, or 429.
---

# Auth and quota

## HTTP (default)

Every data endpoint takes the key in a header:

```
x-api-key: sugra_...
```

Not `Authorization: Bearer` on `https://sugra.ai`. Bearer is only for the hosted MCP connector.

Get a key at https://app.sugra.ai/settings/billing. Every plan sees every endpoint. Gating is volume, not surface.

| Plan | Requests / day |
|---|---|
| Free | 50 |
| Dev | 5,000 |
| Pro | 50,000 |

Some bulk endpoints cost more than 1 request. The response header `X-RateLimit-Cost` is that cost.

## Headers on every data response

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | daily quota |
| `X-RateLimit-Remaining` | left today |
| `X-RateLimit-Reset` | when the window resets (UTC) |
| `X-RateLimit-Cost` | cost of this call |

## Errors

| Status | Meaning | What to do |
|---|---|---|
| 401 | missing or invalid key | stop. Do not retry the same call. |
| 403 | key cannot use this route | stop. |
| 429 | daily quota exhausted | wait until `X-RateLimit-Reset`. Do not spin. |
| 5xx | upstream or platform fault | retry once with backoff. Then report. |

Do not retry 4xx except 429 after the reset.

## MCP (only if already connected)

Hosted MCP (`https://mcp.sugra.ai/mcp`) uses `Authorization: Bearer` (raw key or OAuth JWT, audience `https://app.sugra.ai/mcp`). The MCP tool envelope does not forward `X-RateLimit-*`. On 429 wait for JSON `retry_after` (seconds). Downstream calls from MCP still use `x-api-key`.
