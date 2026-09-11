---
name: connect
description: Attach a client to Sugra over HTTPS or MCP. Use when setting up Claude Desktop, Claude Code, ChatGPT, claude.ai, Cursor, VS Code, Gemini CLI, Grok, a custom HTTP agent, or self-hosted MCP.
---

# Connect

Same key for every path: issue at https://app.sugra.ai/settings/billing. Shape `sugra_...`. Do not log it.

## 1. HTTPS API (any HTTP agent)

```
GET https://sugra.ai/api/v1/...
x-api-key: sugra_...
```

System endpoints (`/health`, `/about`, `/services`, `/sources`, `/openapi.json`) need no key. Data endpoints do. Recipes: https://github.com/Sugra-Systems/sugra-api-cookbook

## 2. Hosted MCP (no local install)

Canonical: `https://mcp.sugra.ai/mcp`
Permanent alias: `https://app.sugra.ai/mcp`

Auth: `Authorization: Bearer sugra_...` or OAuth (audience `https://app.sugra.ai/mcp`, scope `sugra:read`). Discovery (`initialize`, `tools/list`, `prompts/list`, `resources/list`, `ping`) is public. `tools/call` and `resources/read` need Bearer.

- claude.ai: Settings -> Connectors -> Add custom connector
- ChatGPT: Settings -> Connectors -> Add MCP server (ChatGPT does not load SKILL.md from disk)
- Any Streamable HTTP MCP client: that URL plus Bearer

Hosted tools: 8 gateway + 3 composed (`resolve_entity`, `get_snapshot`, `get_timeseries`). Confirm with live `tools/list`.

## 3. Local MCP stdio (`pip install sugra-api-mcp`)

```bash
pip install sugra-api-mcp
export SUGRA_API_KEY=sugra_...
```

Eight gateway tools only. Catalog search works without the key; `call_endpoint` / `fetch_data` / entity tools return `missing_api_key` until it is set.

If `sugra-api-mcp` is not on PATH: `"command": "python", "args": ["-m", "sugra_api_mcp"]`.

CLI of the same package:

```bash
sugra-api-mcp doctor
sugra-api-mcp search "NASDAQ futures"
sugra-api-mcp describe cot_financial
sugra-api-mcp call quotes_symbol_price --params "{\"symbol\":\"AAPL\"}"
```

### Claude Desktop

`claude_desktop_config.json`:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: no Desktop build. Use Claude Code, an IDE, or hosted MCP.

```json
{
  "mcpServers": {
    "sugra": {
      "command": "sugra-api-mcp",
      "env": { "SUGRA_API_KEY": "sugra_..." }
    }
  }
}
```

Restart the app.

### Claude Code

```bash
claude mcp add sugra -- sugra-api-mcp
export SUGRA_API_KEY=sugra_...
```

Same JSON shape in `~/.claude/config.json`.

### Gemini CLI

User file `~/.gemini/settings.json` or project `.gemini/settings.json`, same `mcpServers` stdio block. Or:

```bash
gemini mcp add --scope user -e SUGRA_API_KEY=sugra_... sugra sugra-api-mcp
gemini mcp add --scope user --transport http --header "Authorization: Bearer sugra_..." sugra https://mcp.sugra.ai/mcp
```

`gemini mcp list`, then `/mcp` in session. New folders may need `gemini trust`.

### Cursor, VS Code, Zed, Cline, Continue.dev, Windsurf

Each has an MCP settings file (`mcp.json` or equivalent). Use the same stdio block as Claude Desktop, or the hosted URL with Bearer.

### Grok

Hosted MCP as a remote server, or local stdio with `SUGRA_API_KEY`. Skills from this repo are separate from the MCP server: install the plugin, then still connect MCP or HTTP.

### xAI SDK / Responses API

Remote MCP tools against `https://mcp.sugra.ai/mcp` with Bearer.

## 4. Self-hosted MCP HTTP

```bash
sugra-api-mcp --transport streamable-http --port 8001
```

Or Docker Compose in the `sugra-api-mcp` repo (port 8001, path `/mcp`). Operator CORS/host/OAuth env: `docs/self-hosting.md` in that repo. Do not put `INTERNAL_API_TOKEN` or JWKS URLs in a skill, README Try-form, or chat.

Self-hosted is the eight-tool gateway, not the three hosted-only tools.

## 5. OpenBB

Public extension `openbb-sugra` fetches through the HTTPS API. That is HTTP, not MCP.

## Pick

| Host | Typical attach |
|---|---|
| Script, custom agent, OpenBB | HTTPS `x-api-key` |
| ChatGPT, claude.ai | Hosted MCP connector |
| Claude Desktop / Code, Cursor, VS Code, Gemini CLI, Grok | stdio package or hosted MCP |
| Your own HTTP MCP process | self-host |
