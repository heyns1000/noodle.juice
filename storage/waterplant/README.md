# Waterplant Memory Ledger

This is an append-only, evidence-first ledger for the Explorer Ecosystem — Finding the Tail.

## Rules

- `origin-gorilla` is the root memory and is never overwritten.
- Each later instruction is recorded as a downward drop with an explicit parent link.
- Corrections are new drops; earlier drops remain intact.
- A branch may name GitHub, Supabase, Cloudflare, Vercel, documents, or dashboards only after its destination and approval scope are explicit.
- Session context is not durable evidence. Commits, signed events, database rows, and deployment receipts are durable only when linked.
- A memory record does not authorize merges, secrets access, deployments, public releases, or database writes.

## Current chain

```text
🦍 origin-gorilla — first prompt / root memory
│
├─ 💧 waterplant-0001 — captured instruction
│   └─ 🌱 preserved session record
│
├─ 💧 waterplant-0002 — CodeNest Explorer created
│   └─ 🌿 Git commit: efd7ed5
│
├─ 💧 waterplant-0003 — noodle.juice root indexed
│   └─ 🌿 Git commit: df1fbef
│
└─ 💧 waterplant-0004 — Waterplant hook instruction
    └─ 🌱 state: captured / internal
```

## Open tails

- **Critical:** Supabase project reference, memory-event schema/table, RLS policy, and approved write role are unresolved.
- **High:** The exact original prompt and pre-existing records for `waterplant-0001` through `waterplant-0003` have not been independently recovered from a durable ledger.
- **Medium:** Expand `core/` or `systems/` into evidence-linked module indexes.
