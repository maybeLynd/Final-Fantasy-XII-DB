---
system: <Short subject: the census, the function, or the evidence the note carries>
category: <parent category folder>
status: STUB | PARTIAL | DOCUMENTED | AUDITED | REOPENED
note_kind: census | evidence | function | residual
parent: <relative path of the SYSTEM / FORMAT / CONTRACT page this note serves>
owner_layer: PrimaryOwner:<Category> | CodeDomain:<Path> | both
evidence_tier: 1-11 (see _index/EVIDENCE-STANDARD.md — lowest tier relied upon)
verified_against:
  exe_sha256: <certified image hash>
last_reviewed: <YYYY-MM-DD>
---

# <Title>

<!--
NOTE template (FABLE ruling 2026-09-30, _index/candidates/status-currency-ruling-fable/note-template-ruling.md).
For a census companion, an evidence or review log, a single-function read, or a residual-cluster read: pages whose job
is to carry evidence for a parent write-up, not to be the system write-up. The player view, call chain, modding notes and
key-address table live on the parent; a note does not repeat them. It must still be evidence-complete: every claim
anchored and tiered, the method reproducible, and every open item registered. The five sections below are required
(numbering and extra sections are free). `documented_rule.py` condition N checks that each heading starts with its keyword, each section has a body, the Evidence section holds a tier table with at least one data row, and `parent:` is an existing .md page, not this note, that links back to this note (repaired 2026-09-30 on SWE2-AUDIT-SEM's review).
-->

## Scope

What the note establishes, for which parent page (link it), and what it deliberately leaves to the parent.

## Findings

The established facts, each with its anchor (instruction / data address, file and offset, or census row).

## Evidence

| claim | evidence | tier |
|---|---|---|
| <one row per load-bearing claim> | <anchor, script + output, or observation id> | <tier> |

## Method

How to reproduce it: script and command, inputs and their identity (image hash, data files), the positive control
that shows the instrument can see what it counts, and the extent read (for a function: the whole body, or which part).

## Limits

What is not established. Every open item names its register id (OPEN / PARTIAL row) or states why it is out of scope.
Prose residue with no id keeps the note PARTIAL, as for any page.
