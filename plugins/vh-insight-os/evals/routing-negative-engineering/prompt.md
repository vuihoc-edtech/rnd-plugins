---
schema_version: "1.1"
name: routing-negative-engineering
description: An engineering request against the MCP codebase must not fire any Insight OS analysis
  skill; those skills consume the catalog, they do not modify it.
tags: [routing]
plugins: [insight-os]
max_turns: 4
allowed_tools: [Skill]
expected_outcome: No insight-os-* skill fires.
---

Hãy sửa code FastAPI của MCP để thêm một write tool cập nhật khách hàng.
