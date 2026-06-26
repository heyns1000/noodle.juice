# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## What this repository is

**noodle.juice** is the Python orchestration core for the Fruitful/HotStack ecosystem. It unifies five subsystems into a single bootable runtime driven by a 9-second heartbeat (VaultMesh™ pulse). The repository is part of the larger `heyns1000/codenest` meta-repo.

---

## Running the system

```bash
# Install dependencies
pip install -r requirements.txt

# Full boot — 9s heartbeat + webhook server on :5000
python main.py

# Run NoodleNexus demo then exit (no long-running loop)
python main.py --demo

# Start standalone webhook server only
python main.py --webhook --port 5001

# Boot without the heartbeat loop
python main.py --no-heartbeat
```

There is no build step. No package.json. No transpilation.

---

## Architecture

### Layer ordering (bottom → top)

```
ClaimRoot™       systems/claimroot.py       Oracle-bone foundation locking (SHA-256, immutable)
PulseTrade™      systems/pulsetrade.py      9-second rhythmic pulse engine
BareCart™        systems/barecart.py        Grain-level commerce (1 grain = $0.01 USD)
CrateLogic™      systems/cratelogic.py      File migration / backup transport
Store40D™        storage/store40d.py        40-dimensional key-value store (namespace-isolated)
NoodleNexus™     systems/noodle_nexus.py    Central orchestrator — wires all subsystems
SyncBridge       core/sync_bridge.py        GitHub push → task queue → R2 on each SYNC pulse
SeedwaveCore™    core/seedwave_core.py      Single boot entry point (declares genesis signal)
```

### Boot sequence

`main.py` → `SeedwaveCore.__init__()` (declares genesis, creates NoodleNexus + SyncBridge) → `SeedwaveCore.boot()` (async):
1. `NoodleNexus.initialize()` — registers HEARTBEAT, SYNC, BACKUP, METRIC pulse handlers
2. `PulseTrade.register_handler(SYNC, SyncBridge.handle_sync_pulse)` — wires bridge into pulse
3. Flask webhook thread starts (daemon) on `POST /webhook`
4. `PulseTrade.start_heartbeat()` — blocking async loop, fires every 9 seconds

### 9-second pulse types

`PulseType` enum (in `pulsetrade.py`): `HEARTBEAT`, `TRADE`, `SYNC`, `CLAIM`, `BACKUP`, `METRIC`. On each SYNC beat, `SyncBridge.handle_sync_pulse()` drains its file task queue into Cloudflare R2. Failed tasks are pushed back to the front of the queue and retried on the next pulse.

### GitHub → R2 sync path

```
GitHub push event
  └─ POST /webhook (Flask, port 5000)
        └─ SyncBridge._enqueue_push()  # adds put/delete tasks to deque
              └─ every 9s SYNC pulse
                    └─ SyncBridge.handle_sync_pulse()
                          └─ downloads file from raw.githubusercontent.com
                                └─ boto3 → R2 bucket (fruitful-thank-you)
```

Dry-run mode activates automatically when `R2_ACCOUNT_ID` / `R2_ACCESS_KEY` / `R2_SECRET_KEY` are unset — operations print `[DRY]` and succeed silently.

### Store40D dimensions

`DimensionType` has exactly 40 enum values (BRAND, ASSET, LICENSE, USER, PAYMENT, SIGNAL, BUILD, DEPLOY, PULSE, METRIC, CLAIM, VAULT, CART, ORDER, REPO, WEBHOOK, CRATE, SYNC, HEALTH, LOG, CONFIG, SECRET, TOKEN, SESSION, AUDIT, ROYALTY, GLYPH, GRAIN, TERRITORY, SECTOR, PARTNER, CONTRACT, TEMPLATE, DOMAIN, EMAIL, MEDIA, EVENT, TASK, SCHEDULE, ARCHIVE). Each is an isolated namespace bucket inside a single in-memory store.

---

## Environment variables

| Variable | Purpose | Required |
|---|---|---|
| `WEBHOOK_SECRET` | HMAC-SHA256 key for GitHub webhook signature verification | No (skips verification if unset) |
| `GITHUB_TOKEN` | Token for fetching file content from private repos via raw.githubusercontent.com | No (public repos work without it) |
| `R2_ACCOUNT_ID` | Cloudflare account ID for R2 boto3 endpoint | No (dry-run if unset) |
| `R2_ACCESS_KEY` | R2 access key (s3-compatible) | No (dry-run if unset) |
| `R2_SECRET_KEY` | R2 secret key | No (dry-run if unset) |
| `R2_BUCKET` | R2 bucket name (default: `fruitful-thank-you`) | No |

---

## Key design constraints

- `SyncBridge` uses `hmac.new()` — Python stdlib, no extra crypto dependency.
- `NoodleNexus` adds the repo root to `sys.path` via `sys.path.append(os.path.dirname(os.path.dirname(__file__)))` — this is intentional so `storage.*` and `systems.*` are importable from within the `systems/` package.
- All subsystem classes (ClaimRoot, PulseTrade, BareCart, CrateLogic) are thread-safe via `threading.RLock`.
- The `FruitfulWebhook` (`webhook/fruitful_webhook.py`) is a standalone alternative webhook server with decorator-style `@webhook.on('event')` registration. It is NOT used by `SeedwaveCore` — `SyncBridge` has its own Flask app. Use `FruitfulWebhook` for standalone event processing.
- Genesis signal (`signal/SEEDWAVE-011-CORE.json`) is the immutable origin record. Priority date and all numeric claims in it must not be changed.

---

## Webhook endpoints

SyncBridge (`/` when booted via `SeedwaveCore`):
- `POST /webhook` — GitHub push / ping events
- `GET /health` — queue depth, R2 connection status, stats
- `GET /` — service identity

FruitfulWebhook (standalone via `python main.py --webhook`):
- `POST /webhook` — all GitHub events
- `GET /health` — delivery stats
- `GET /events` — last 50 received events
