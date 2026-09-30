# Client attach blocks

Stdio MCP (local package). Replace the key.

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

## Claude Desktop

File: macOS `~/Library/Application Support/Claude/claude_desktop_config.json`; Windows `%APPDATA%\Claude\claude_desktop_config.json`. Linux has no Desktop build: use Claude Code, an IDE, or hosted MCP. Restart after edit.

## Claude Code

```bash
claude mcp add sugra -- sugra-api-mcp
export SUGRA_API_KEY=sugra_...
```

Same JSON in `~/.claude/config.json`.

## Gemini CLI

User `~/.gemini/settings.json` or project `.gemini/settings.json`, same `mcpServers` block. Or:

```bash
gemini mcp add --scope user -e SUGRA_API_KEY=sugra_... sugra sugra-api-mcp
gemini mcp add --scope user --transport http --header "Authorization: Bearer sugra_..." sugra https://mcp.sugra.ai/mcp
```

`gemini mcp list`, then `/mcp` in session.

## Cursor, VS Code, Zed, Cline, Continue.dev, Windsurf

Each has an MCP settings file (`mcp.json` or equivalent). Use the stdio block above or hosted `https://mcp.sugra.ai/mcp` with Bearer.

## Grok

Hosted MCP as a remote server, or local stdio with `SUGRA_API_KEY`. This skill plugin is separate from the MCP server: install the plugin, then still connect MCP or HTTP.

## xAI SDK / Responses API

Remote MCP tools against `https://mcp.sugra.ai/mcp` with Bearer.

## ChatGPT and claude.ai

Hosted connector only. No SKILL.md load on ChatGPT.
