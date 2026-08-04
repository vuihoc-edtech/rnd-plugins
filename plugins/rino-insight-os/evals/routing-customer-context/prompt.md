---
schema_version: "1.1"
name: routing-customer-context
description: Resolving one customer by phone before a call is customer context, even though
  "buying signals" is shared vocabulary with market intelligence.
tags: [routing]
plugins: [insight-os]
max_turns: 4
allowed_tools: [Skill]
expected_outcome: The insight-os-customer-context skill fires; market-intelligence does not.
---

Tìm khách theo số điện thoại rồi tóm tắt buying signals trước cuộc gọi.
