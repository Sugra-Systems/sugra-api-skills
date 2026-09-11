# sugra-api-skills

Official [Sugra API](https://sugra.ai) skills for agents.

Sugra API is intelligence infrastructure: one HTTP API, one key, seven product directions (Sugra Finance, Sugra Macro, Sugra Entity, Sugra Net Atlas, Sugra News, Sugra Earth, Sugra Research). An agent works it over HTTPS, over MCP, or both.

**Documentation truth:** [https://docs.sugra.ai](https://docs.sugra.ai) (search and Ask AI). This repository does not copy the endpoint catalog.

This is not the MCP server ([sugra-api-mcp](https://github.com/Sugra-Systems/sugra-api-mcp)) and not the HTTP cookbook ([sugra-api-cookbook](https://github.com/Sugra-Systems/sugra-api-cookbook)).

**Not on GitHub yet.** Local draft. Do not `/plugin marketplace add` a GitHub path until this repo is published.

Public hedge (not a live count): 1,500+ endpoints, 160+ primary sources, 36 domains. Live counts: https://sugra.ai/stats and docs.sugra.ai.

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

## Install (after GitHub publish)

Intended remote: `Sugra-Systems/sugra-api-skills`.

Claude Code:

```
/plugin marketplace add Sugra-Systems/sugra-api-skills
/plugin install sugra-api@sugra-api-skills
```

Grok (this folder today):

```bash
grok plugin marketplace add C:\DEV-SUGRA\sugra-api-skills
grok plugin install sugra-api --trust
```

Codex: install the plugin from this repo (`.codex-plugin/plugin.json`), or copy each folder under `plugins/sugra-api/skills/` into `$HOME/.agents/skills/<slug>/`.

Cursor: copy into `.cursor/skills/` or `~/.cursor/skills/`.

Gemini CLI: `npx skills add` against this repo after publish, or copy into `.agents/skills/`.

ChatGPT does not load SKILL.md from disk. Point it at `https://mcp.sugra.ai/mcp`.

## Local check

```bash
python scripts/check.py
```

## License

MIT. Data from each endpoint carries its own upstream terms. See https://sugra.ai/sources and per-response `meta`.
