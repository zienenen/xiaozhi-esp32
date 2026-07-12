# agents

Owns role/agent configuration and context generation.

Phase 1 scope:
- Agent name
- Personality prompt
- Voice reference
- Dataset reference
- Marketization placeholders such as series and rarity
- `/api/v1/agents/{agent_id}/context`

The xiaozhi-side tool/MCP entry should call the context endpoint instead of
copying full scenic knowledge into the xiaozhi console.
