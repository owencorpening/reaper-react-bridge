# REAPER + React: JSON-Controlled Custom Effect

A proof-of-concept for controlling a REAPER JSFX effect using a modern React UI via REAPER's Web Control interface.

## 🧩 Architecture

- **React UI**: Modern front-end sends JSON-formatted settings.
- **REAPER WebCtl**: Receives HTTP requests and writes settings to `ExtState`.
- **Lua Script**: Parses JSON from `ExtState` and writes parameters for JSFX to consume.
- **JSFX**: Reads `ExtState` values each block and applies to live audio.

## 🛠 Setup

1. **Enable REAPER Web Control** (`Preferences > Control/OSC/web`).
2. Run `processSettings.lua` as a background action in REAPER.
3. Add `MyCustomDelay.jsfx` to a track.
4. Start `react-ui` with `npm start` or serve it into `reaper_www_root`.

## 📦 Features

- JSON-based setting flow
- Modular setup: swap out React UI or effect
- Works with REAPER's built-in scripting and FX systems

## 🧪 Next Steps

- Add WebSocket live update feedback
- Debounce React requests
- Extend to any JSFX or VST parameter mapping
