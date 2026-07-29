---
description: Nghiên cứu nhu cầu, pain point, xu hướng hoặc verify nhận định thị trường từ Insight OS MCP
argument-hint: "<chủ đề | nhận định cần verify> [segment] [khoảng thời gian]"
disable-model-invocation: true
---

Invoke the `insight-os-market-intelligence` skill and follow its workflow exactly. That skill owns
the facet discovery, cluster verification, and claim-verdict rules — do not restate or shortcut
them here.

Topic or claim supplied by the user: $ARGUMENTS

If the request is an outcome-cohort comparison such as won-vs-no_order or won-vs-lost, stop and
use the `insight-os-conversion-research` skill instead; that boundary belongs to conversion
research, not market intelligence.
