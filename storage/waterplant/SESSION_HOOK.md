# Waterplant Session Hook

## Trigger phrase

`Sambayo`

## Intent

When the user explicitly says `Sambayo` at the end of a meaningful work session, prepare one append-only Waterplant update for review.

## Required workflow

1. Read `storage/waterplant/memory.jsonl` from `main`.
2. Validate that every non-root record has a parent and that parent exists.
3. Derive the next sequential `waterplant-` identifier without editing any existing JSONL line.
4. Create a dedicated branch and a pull request to `main` containing the proposed new drop.
5. Include source-thread references or Git commit URLs only when available as evidence.
6. Do not merge automatically.
7. Do not write to Supabase, create credentials, deploy, publish, access secrets, or modify an earlier memory record.

## Boundary

`Sambayo` means “prepare the next Waterplant drop for review.” It is not authorization to merge, deploy, access secrets, or write to Supabase.
