# sugra-api-skills

<p align="center">
  <img src="https://app.sugra.ai/images/brand/sugra-app-icon.svg" alt="sugra.ai" width="112" height="112" />
</p>

<p align="center">
  <a href="https://github.com/Sugra-Systems/sugra-api-skills/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Sugra-Systems/sugra-api-skills?label=License&color=F5A623" alt="License"></a>
</p>

Official [Sugra API](https://sugra.ai) skills for Claude, Grok, Codex, Cursor, Gemini, and ChatGPT.

One HTTP API, one key, seven product directions (Sugra Finance, Sugra Macro, Sugra Entity, Sugra Net Atlas, Sugra News, Sugra Earth, Sugra Research). Work it over HTTPS, over MCP, or both.

This is not the MCP server ([sugra-api-mcp](https://github.com/Sugra-Systems/sugra-api-mcp)) and not the HTTP cookbook ([sugra-api-cookbook](https://github.com/Sugra-Systems/sugra-api-cookbook)).

Public hedge (not a live count): 1,500+ endpoints, 160+ primary sources, 36 domains. Live counts: https://sugra.ai/stats.

## Install

Get a key at [app.sugra.ai/settings/billing](https://app.sugra.ai/settings/billing) (Free: 50 requests/day).

### Claude Code

```
/plugin marketplace add Sugra-Systems/sugra-api-skills
/plugin install sugra-api@sugra-api-skills
```

### Grok

```
grok plugin marketplace add Sugra-Systems/sugra-api-skills
grok plugin install sugra-api --trust
```

### Codex

```
cp -R plugins/sugra-api/skills/. ~/.agents/skills/
```

### Cursor

```
cp -R plugins/sugra-api/skills/. ~/.cursor/skills/
```

### Gemini CLI

```
cp -R plugins/sugra-api/skills/. ~/.gemini/skills/
```

### ChatGPT

```
# hosted MCP connector; ChatGPT does not load SKILL.md
https://mcp.sugra.ai/mcp
```

## Plugin `sugra-api`

| Skill | When |
|---|---|
| `using-sugra-api` | map of surfaces and directions |
| `live-docs` | docs.sugra.ai, OpenAPI, sources, blog |
| `connect` | HTTPS, hosted MCP, stdio, self-host, clients |
| `auth-and-quota` | `x-api-key`, Bearer, OAuth, 401/429 |
| `discover-and-call` | find and call on HTTP or MCP |
| `envelope-and-attribution` | `{data, meta}`, source names, clocks |
| `cross-domain-briefing` | two or three directions in one answer |

Author: Sugra Systems, Inc. License: MIT. Skills follow the [Agent Skills](https://agentskills.io/specification) format.

## Documentation

Endpoint reference, search, and Ask AI: [https://docs.sugra.ai](https://docs.sugra.ai)

Machine companions: `https://sugra.ai/openapi.json`, `/sources`, `/stats`.

## Local check

```
python scripts/check.py
```

## License

MIT. Data from each endpoint carries its own upstream terms. See https://sugra.ai/sources and per-response `meta`.
