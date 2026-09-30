# sugra-api for ChatGPT and Codex

Official Sugra API skills. HTTPS and MCP. Agent Plugins 1.0.0 package: `plugin.json` (with `extensions.com.openai`), `mcp.json` (not in a `--skills-only` ZIP), `skills/`, `assets/`.

Codex installs it from marketplace `sugra-api-skills` (`.agents/plugins/marketplace.json`). The Plugins Directory package is a ZIP of this folder built by `python scripts/build_openai_zip.py`; with `--skills-only` the ZIP leaves `mcp.json` out.

`mcp.json` connects the Sugra API MCP server at `https://app.sugra.ai/mcp` (`streamable-http`). Without it, as in a `--skills-only` ZIP, add that server as a hosted connector instead. The skills are copied from the repository's `skills/` folder by `scripts/sync.py`; edit them there.

Documentation: https://docs.sugra.ai
