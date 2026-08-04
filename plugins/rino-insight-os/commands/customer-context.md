---
description: Chuẩn bị context khách hàng trước cuộc gọi từ Insight OS MCP
argument-hint: "<tên khách | số điện thoại | contact_id>"
disable-model-invocation: true
---

Invoke the `insight-os-customer-context` skill and follow its workflow exactly. That skill owns
the capability chain, the scope rules, and the output contract — do not restate or shortcut them
here.

Customer identifier supplied by the user: $ARGUMENTS

If the identifier is empty, ask for a name, phone fragment, or `contact_id` before calling any
tool. Do not scan for customers without an identifier.
