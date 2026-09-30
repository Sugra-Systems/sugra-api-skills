# sugra-api for Grok

Official Sugra API skills. HTTPS and MCP. Grok package: `.grok-plugin/plugin.json`, `.mcp.json`, `skills/`.

```
grok plugin marketplace add Sugra-Systems/sugra-api-skills
grok plugin install sugra-api --trust
```

`.mcp.json` connects the Sugra API MCP server at `https://app.sugra.ai/mcp` (`type: http`). The skills are copied from the repository's `skills/` folder by `scripts/sync.py`; edit them there.

Documentation: https://docs.sugra.ai
