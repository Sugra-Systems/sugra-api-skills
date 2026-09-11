---
name: live-docs
description: Find current Sugra API documentation, OpenAPI, source list, MCP tool list, and live counts. Use before inventing a path, quoting an endpoint count, or when a skill might be stale.
---

# Live docs

This skill pack is a map. It is not the catalog. Paths, parameters, tool counts, and package version change. Fetch live documents. Do not quote numbers from memory.

## Always-current (no key)

Fetch these from `https://sugra.ai` when the question is "what exists now":

| URL | What it is |
|---|---|
| `GET /health` | liveness |
| `GET /about` | product surface |
| `GET /services` | service list |
| `GET /sources` | source families, named under copy rules |
| `GET /openapi.json` | full HTTP operations, parameters, bodies |
| `GET /stats` | live endpoint / source / domain counts |

Public copy still uses hedges (1,500+ / 160+ / 36). `/stats` is the live counter. Do not equate `/stats` with the MCP bundled catalog (the wheel can lag a few operations).

## HTTP vs MCP catalogs

- HTTP: live OpenAPI is the map. A miss on OpenAPI is a miss on the API.
- MCP: `search_endpoints` / `list_toolsets` / `list_sources` read a catalog bundled in the package. Hosted MCP tracks git main of `sugra-api-mcp`. A PyPI stdio install is whatever version was tagged. If MCP search misses, fetch `/openapi.json` before saying Sugra has no data.

MCP live surface after connect: `initialize` (`serverInfo.version`), `tools/list`, `prompts/list`, `resources/list`. Resources include `sugra://catalog/domains`, `sugra://catalog/sources`, `sugra://attribution`, `sugra://skills/...`.

## Human docs and code

| Where | What |
|---|---|
| https://sugra.ai | product |
| https://app.sugra.ai | keys, billing, playground |
| https://app.sugra.ai/settings/billing | issue a key |
| https://sugra.systems | company, legal |
| https://docs.sugra.ai | documentation |
| https://pypi.org/project/sugra-api-mcp/ | MCP package version |
| https://github.com/Sugra-Systems/sugra-api-mcp | MCP server, `FACTS.md`, README, self-hosting |
| https://github.com/Sugra-Systems/sugra-api-cookbook | runnable HTTP recipes |
| https://github.com/Sugra-Systems/openbb-sugra | OpenBB provider |
| https://github.com/Sugra-Systems/sugra-api-skills | this skill pack (after publish) |

Legal: https://sugra.systems/terms-of-service, `/privacy-policy`, `/data-use-policy`, `/acceptable-use-policy`, `/data-processing-agreement`, `/service-level-agreement`. Contacts: `support@`, `legal@`, `privacy@`, `abuse@` sugra.systems.

## Do not

- Do not invent a path or `operation_id`.
- Do not treat a stale README, cookbook, or this SKILL.md as the operation list.
- Do not name commercial upstreams. Use Sugra wrappers or the live `/sources` document.
