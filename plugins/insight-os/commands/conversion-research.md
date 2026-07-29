---
description: So sánh outcome cohort và tạo messaging hypothesis có evidence từ Insight OS MCP
argument-hint: "[target vs reference outcome] [segment] [khoảng thời gian]"
disable-model-invocation: true
---

Invoke the `insight-os-conversion-research` skill and follow its workflow exactly. That skill owns
the outcome-comparison path, the signed `evidence_query` passthrough, and the association-not-cause
rule — do not restate or shortcut them here.

Cohorts and scope supplied by the user: $ARGUMENTS

When no outcomes are named, use the skill's default target and reference cohorts. If the request is
about how a salesperson handled objections rather than which cohort a signal co-occurs with, use
the `insight-os-sales-coaching` skill instead.
