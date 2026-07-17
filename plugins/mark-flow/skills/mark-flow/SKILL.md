---
name: mark-flow
description: Uses the bundled `markflow` MCP server to search, inspect, summarize, compare, and review MarkFlow Hub scripts, daily scripts, catalog metadata, comments, and review timelines. Use when a user asks about MarkFlow script content, daily script content, approval/review context, comments, classes, subjects, teams, target audiences, or MCP-backed MarkFlow data access.
---

# MarkFlow

Use the configured `markflow` MCP server first for MarkFlow Hub business questions. Treat MCP tool descriptions and schemas as the source of truth for parameters, validation, and return shapes. Answer only from returned records.

## Business Context

- Normal scripts are section-based lesson/production scripts with catalog metadata, sections, dialogue, performance style, and teacher/actor context.
- Daily scripts are item-based daily content with team/type metadata, note, caption, item voice, and item source.
- Comments are unit-level feedback: normal scripts group by section order; daily scripts group by item order.
- Timelines are workflow events. Use them for audit history, approval flow, rejection reasons, and actor/date context.

## Playbook

- Catalog name resolution: resolve named classes, subjects, teams, or target audiences before applying numeric filters. Preserve Vietnamese text and mention ambiguity when multiple catalog items look plausible.
- Search first, then fetch detail for likely records. Include sections/items only when the user needs content summary, review, or comparison.
- For rejected, approved, pending, blocked, or audit-history questions, fetch timeline first; add comments when the user asks for feedback details or blockers.
- For subject requests, remember normal script search has no subject filter. Search by keyword, then inspect likely details for subject snapshots.
- For comparisons, compare status/catalog metadata before section or item content.

## Answer Rules

- Lead with the direct business answer, then list evidence records. Include IDs when the user may need follow-up detail.
- Separate record facts from your interpretation. Use phrases like "Based on returned comments..." for conclusions.
- Preserve user-provided Vietnamese keywords exactly unless the user asks for translation or normalization.
- Do not invent catalog names, statuses, reasons, comments, or missing records. If no data returns, say so and suggest the next narrower or broader query.
- The bundled MCP tools are read-only. For create/update/approve/reject/delete/schedule requests, say the MCP cannot perform that action and offer to help with API/code work if relevant.
