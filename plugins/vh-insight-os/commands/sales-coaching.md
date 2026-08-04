---
description: Chọn ưu tiên coaching và lấy call mẫu có evidence từ Insight OS MCP
argument-hint: "[tên sale | team] [khoảng thời gian]"
disable-model-invocation: true
---

Invoke the `insight-os-sales-coaching` skill and follow its workflow exactly. That skill owns the
team-scan versus single-person paths, the call budget, and the time-language rules — do not
restate or shortcut them here.

Scope supplied by the user: $ARGUMENTS

Read the scope as a salesperson or team plus an optional window. When no salesperson is named,
run the team scan. When only meeting timing is given, apply the skill's rule for choosing and
labelling a diagnosis window rather than treating the meeting date as the analysis window.
