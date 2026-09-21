# FAA.ZONE Repository Wireframe Extension

## Purpose

This extension records repository identity and evidence flow for FAA.ZONE-related deployment work. It is documentation only. It does not change, mirror, or replace the `heyns1000/faa.zone` repository.

## Boundary

- `heyns1000/faa.zone` is read-only for this extension.
- Each repository retains its own branches, pull requests, CI/CD, and deployment authority.
- A merge is a source-control event, not proof of deployment.
- A deployment is verified only with a provider receipt tied to a commit SHA.
- Events are append-only. Corrections use a superseding event rather than modifying prior evidence.

## Waterhook Event Schema

```yaml
event_id: PENDING
waterhook_origin: PENDING
previous_event_id: PENDING
event_type: pr_merged | commit_merged | deployment_verified | superseded
repository_full_name: PENDING
repository_identity_url: PENDING
target_branch: PENDING
pr_number: PENDING
merge_commit_sha: PENDING
merged_at_utc: PENDING
source_url: PENDING
change_summary: PENDING
evidence_hash: PENDING
approval_authority: PENDING
deployment_receipt_url: PENDING
verification_state: sourced | reviewed | deployed_verified | superseded
```

## Cloudflare Evidence

- Cloudflare configuration must use provider-managed secrets or CI secret stores.
- Do not commit API tokens, zone IDs, private keys, recovery phrases, or secret values.
- Safe placeholders are permitted only when they are clearly non-functional:

```text
CLOUDFLARE_API_TOKEN=[SET_IN_CLOUDFLARE_SECRET_STORE]
GITHUB_TOKEN=[SET_IN_GITHUB_ACTIONS_OR_SECRET_STORE]
ZONE_ID=[SET_IN_CLOUDFLARE_SECRET_STORE]
DEPLOYMENT_RECEIPT_URL=[PENDING]
```

## Required Verification

For a `deployment_verified` event, attach:

1. Repository and commit SHA.
2. Deployment provider and environment.
3. Timestamp in UTC.
4. Provider deployment, Worker, or CI receipt URL/identifier.
5. Evidence hash.
6. Reviewer or approval authority.

## Open Tail

- The live FAA.ZONE deployment provider, production mapping, and deployment receipt are unverified in this extension.
- This extension does not authorize a deployment.
