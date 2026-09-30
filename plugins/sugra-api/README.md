# sugra-api

Official Sugra API skills for Claude. HTTPS and MCP. Plugin `sugra-api` in marketplace `sugra-api-skills`.

This folder is the Claude package: `.claude-plugin/plugin.json`, `.mcp.json`, `skills/`. The skills are copied from the repository's `skills/` folder by `scripts/sync.py`; edit them there.

Hosted MCP: `.mcp.json` connects the Sugra API MCP server at `https://app.sugra.ai/mcp` (`type: http`). The plugin carries no key; the server asks each person to sign in. The server receives the tool calls Claude makes to it (endpoint names and parameters). The skills themselves run nothing.

Documentation: https://docs.sugra.ai
