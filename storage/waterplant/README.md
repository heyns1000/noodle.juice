# Waterplant Memory Ledger

This is an append-only, evidence-first ledger for the Explorer Ecosystem — Finding the Tail.

## Rules

- `origin-gorilla` is the root memory and is never overwritten.
- Each later instruction is recorded as a downward drop with an explicit parent link.
- Corrections are new drops; earlier drops remain intact.
- A branch may name GitHub, Supabase, Cloudflare, Vercel, documents, or dashboards only after its destination and approval scope are explicit.
- Session context is not durable evidence. Commits, signed events, database rows, and deployment receipts are durable only when linked.
- A memory record does not authorize merges, secrets access, deployments, public releases, or database writes.
- **Next-commit documentation rule:** before the next implementation commit, add or update the relevant Waterplant document record with the clear finding, source link, open unverified tail, next document destination, and explicit approval boundary. The implementation commit must link back to that record.
- **Cross-pollination rule:** do not flow into another document, repository, service, or system until reciprocal durable links exist in both directions and the destination approval scope is explicit.

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
    └─ 💧 waterplant-0005 — drip when full; cross-pollination boundary
```

## Commit documentation checklist

Before committing implementation work, record:

1. **Finding:** What changed or was learned.
2. **Evidence:** A source link, commit link, or explicitly empty evidence list.
3. **Open tail:** What remains unverified or incomplete.
4. **Destination:** The next document, branch, page, or system being proposed.
5. **Approval boundary:** What the record does not authorize.
6. **Lineage:** The immediate Waterplant parent record.

## Open tails

- **Critical:** Supabase project reference, memory-event schema/table, RLS policy, and approved write role are unresolved.
- **High:** The exact original prompt and pre-existing records for `waterplant-0001` through `waterplant-0003` have not been independently recovered from a durable ledger.
- **High:** `banimal-giving-loop` has no reciprocal durable evidence link and remains an unverified seed.
- **Medium:** Expand `core/` or `systems/` into evidence-linked module indexes.
