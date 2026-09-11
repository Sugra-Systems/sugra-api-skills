# sugra-api-skills

Official Sugra API skills for agents.

Sugra API is intelligence infrastructure: one HTTPS API, one key, 1,500+ endpoints across 160+ primary sources and 36 domains. An agent that can GET a URL can use it. MCP is optional.

This repository is the skill marketplace. It is not the MCP server (`sugra-api-mcp`) and not the HTTP cookbook (`sugra-api-cookbook`).

**Not on GitHub yet.** Local draft. Do not `/plugin marketplace add` a GitHub path until this repo is published.

## What the plugin teaches

Plugin name: `sugra-api`. Six skills, HTTP first:

| Skill | When |
|---|---|
| `using-sugra-api` | start here: base URL, key, first GET |
| `auth-and-quota` | `x-api-key`, plans, 401/429 |
| `discover-and-call` | find a path in OpenAPI, then call it |
| `envelope-and-attribution` | `{data, meta}`, source names, clocks |
| `cross-domain-briefing` | two or three domains in one answer |
| `mcp-connector` | only if the host cannot call HTTPS, or MCP is already connected |

Default call:

```
GET https://sugra.ai/api/v1/etf/sectors/relative-strength?window=1m
x-api-key: sugra_...
```

Free key: [app.sugra.ai/settings/billing](https://app.sugra.ai/settings/billing) (50 req/day).

## Install (after GitHub publish)

Intended remote: `Sugra-Systems/sugra-api-skills`.

Claude Code:

```
/plugin marketplace add Sugra-Systems/sugra-api-skills
/plugin install sugra-api@sugra-api-skills
```

Grok (from this folder today; from GitHub after publish):

```bash
grok plugin marketplace add ./sugra-api-skills
grok plugin install sugra-api --trust
```

Codex: copy each folder under `plugins/sugra-api/skills/` into `$HOME/.agents/skills/<slug>/` or `~/.codex/skills/<slug>/`.

Cursor: copy into `.cursor/skills/` or `~/.cursor/skills/`.

ChatGPT does not load SKILL.md from disk. Point it at the hosted MCP connector `https://mcp.sugra.ai/mcp`.

## Local check

```bash
python scripts/check.py
```

## License

MIT. Data from each endpoint carries its own upstream terms. See https://sugra.ai/sources and per-response `meta`.
