# CLAUDE.md — reaper-react-bridge

## Status
- **State:** In Progress
- **Next action:** Migrate from HTTP polling proof-of-concept to WebSocket architecture per PLAN.md.
- **Last updated:** 2026-04-30

## What this is

Bridge between React (modern UI) and REAPER (DAW) to drive custom JSFX effect interfaces. Python backend (`bridge.py`, `reaper_api.py`) connects to REAPER's OSC/API layer; React UI (`react-ui/`) renders knobs, sliders, and visualizers that REAPER's native UI can't do.

**Current state:** HTTP polling proof-of-concept (single commit)  
**Target state:** WebSocket architecture — see `PLAN.md` for full roadmap

## Stack

- `bridge.py` — Python FastAPI bridge to REAPER
- `reaper_api.py` — REAPER API abstraction
- `react-ui/` — React frontend
- `jsfx/` — JSFX effect scripts

## Run

```bash
# Activate venv
source venv/bin/activate

# Start bridge
python bridge.py
```

## Related

- `~/dev/Reaper_InsertLyrics` — companion Lua script for lyrics insertion
- `~/dev/wraith` — Songster project context (stem separation + Whisper + REAPER)
