# REAPER React Bridge

**Build professional effect UIs for REAPER using React + Python**

Stop fighting with JSFX's 1995-era UI toolkit. Build gorgeous, responsive effect interfaces using modern web technologies, while keeping REAPER's rock-solid audio processing.

---

## What This Is

A bridge between React (modern UI framework) and REAPER (professional DAW), enabling you to build custom effect interfaces that feel like 2025, not 1995.

**The Problem:**
- JSFX UI elements are limited and dated
- REAPER's built-in controls don't match modern UX expectations
- You're a professional developer who wants professional tools

**The Solution:**
- Build UIs in React (component libraries, state management, hot reload)
- Python bridge handles REAPER communication
- WebSockets provide real-time bidirectional updates
- Your JSFX processes audio, React controls parameters

---

## Who This Is For

**Professional developers making music:**
- You know React (or want to learn it properly)
- You use REAPER for music production
- You want custom effect UIs that match your workflow
- You're tired of parameter limitations

**This is NOT:**
- A replacement for REAPER's built-in UI
- Beginner-friendly (assumes dev experience)
- A VST wrapper or plugin format
- Production-ready (it's a bridge for custom workflows)

---

## Architecture

```
┌──────────────────────┐
│   React UI           │  Modern web UI (localhost:3000)
│   - Components       │  Hot reload, TypeScript, libraries
│   - State mgmt       │  Beautiful knobs, sliders, visualizers
│   - Hot reload       │
└──────────┬───────────┘
           │
      WebSocket
           │
┌──────────▼───────────┐
│  Python Bridge       │  FastAPI server (localhost:8765)
│  - WebSocket server  │  Translates between React and REAPER
│  - REAPER API        │  Handles ExtState, ReaScript, OSC
│  - State management  │
└──────────┬───────────┘
           │
    REAPER ExtState
    or ReaScript API
           │
┌──────────▼───────────┐
│  REAPER              │  Your DAW
│  - JSFX effects      │  Reads parameters, processes audio
│  - Lua scripts       │  Optional middleware
└──────────────────────┘
```

**Key Points:**
- React never touches REAPER directly
- Python handles all REAPER-specific quirks
- WebSocket enables real-time updates both ways
- JSFX focuses on audio, not UI

---

## Features

### ✅ Current
- WebSocket-based real-time communication
- React hooks for clean REAPER integration
- Python bridge with FastAPI
- ExtState-based parameter passing
- Example delay effect with modern UI
- Hot reload during development

### 🔨 In Progress
- Multiple effect support
- Preset management
- MIDI learn integration
- Visualization components

### 📋 Planned
- ReaScript API integration (bypass ExtState)
- OSC support for additional control
- Mobile-responsive layouts
- Integration with Songster workflows
- Component library for common audio controls

---

## Quick Start

### Prerequisites
```bash
# System requirements
- REAPER (any recent version)
- Python 3.8+
- Node.js 16+
- Linux/Mac/Windows

# Install Python dependencies
pip3 install fastapi uvicorn websockets pyyaml

# Install Node dependencies
cd react-ui
npm install
```

### 1. Start the Python Bridge
```bash
python bridge.py

# Bridge runs on localhost:8765
# Serves React build on localhost:8765
# WebSocket available at ws://localhost:8765/ws
```

### 2. Start React Dev Server (Development)
```bash
cd react-ui
npm start

# Development server on localhost:3000
# Hot reload enabled
# Connects to Python bridge on 8765
```

### 3. Add JSFX to REAPER
```bash
# Copy effects to REAPER
cp jsfx/*.jsfx ~/.config/REAPER/Effects/

# In REAPER: Add effect to track
# Effect reads parameters from ExtState
```

### 4. Open the UI
```
http://localhost:3000/delay

# Change parameters in browser
# Hear changes in REAPER instantly
```

---

## Project Structure

```
reaper-react-bridge/
├── README.md                    # This file
├── PLAN.md                      # Development plan and roadmap
├── LICENSE                      # MIT License
│
├── bridge.py                    # Main Python FastAPI server
├── reaper_api.py               # REAPER communication layer
├── config.yaml                  # Bridge configuration
├── requirements.txt             # Python dependencies
│
├── react-ui/                    # React application
│   ├── src/
│   │   ├── hooks/
│   │   │   └── useReaperEffect.ts    # Main React hook
│   │   ├── components/
│   │   │   ├── Knob.tsx              # Rotary knob component
│   │   │   ├── Slider.tsx            # Slider component
│   │   │   └── Visualizer.tsx        # Audio visualizer
│   │   ├── effects/
│   │   │   ├── DelayEffect.tsx       # Example delay UI
│   │   │   └── ReverbEffect.tsx      # Example reverb UI
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
│
├── jsfx/                        # REAPER JSFX effects
│   ├── CustomDelay.jsfx
│   └── CustomReverb.jsfx
│
├── lua/                         # Optional Lua helpers
│   └── extstate_helper.lua
│
└── docs/
    ├── ARCHITECTURE.md          # Detailed architecture docs
    ├── API.md                   # WebSocket API reference
    └── INTEGRATION.md           # Integrating with other tools
```

---

## Usage Examples

### Basic Effect Control

```typescript
// DelayEffect.tsx
import { useReaperEffect } from '../hooks/useReaperEffect';

export function DelayEffect() {
  const { connected, sendParam, currentValues } = useReaperEffect('CustomDelay');

  return (
    <div>
      <input 
        type="range" 
        value={currentValues.time || 500}
        min={0}
        max={2000}
        onChange={(e) => sendParam('time', Number(e.target.value))}
      />
    </div>
  );
}
```

### With Component Library

```typescript
import { Knob } from '../components/Knob';

<Knob
  label="Delay Time"
  value={currentValues.time}
  min={0}
  max={2000}
  unit="ms"
  onChange={(value) => sendParam('time', value)}
/>
```

### Launch from Songster

```python
# In your Songster workflow
from reaper_bridge import launch_effect_ui

def process_song(mp3_path):
    # Process stems...
    
    # Launch custom reverb UI for vocals
    launch_effect_ui('reverb', track='vocals')
```

---

## Development Workflow

### 1. Create New Effect

**Create JSFX:**
```javascript
// MyEffect.jsfx
desc: My Custom Effect

@init
ext_noinit = 1;

@block
time = ext_get_value("MyEffect", "time", 500);
feedback = ext_get_value("MyEffect", "feedback", 0.5);

// Process audio with parameters
```

**Create React UI:**
```typescript
// MyEffect.tsx
export function MyEffect() {
  const { sendParam, currentValues } = useReaperEffect('MyEffect');
  
  return (
    <div>
      <Knob label="Time" onChange={(v) => sendParam('time', v)} />
      <Knob label="Feedback" onChange={(v) => sendParam('feedback', v)} />
    </div>
  );
}
```

**Register in Bridge:**
```yaml
# config.yaml
effects:
  - name: MyEffect
    parameters:
      - time
      - feedback
```

### 2. Test Locally
```bash
# Terminal 1: Python bridge
python bridge.py

# Terminal 2: React dev server  
cd react-ui && npm start

# Terminal 3: REAPER
# Add effect, open UI, test
```

### 3. Build for Production
```bash
cd react-ui
npm run build

# Serves from bridge.py automatically
python bridge.py --production
```

---

## Configuration

### config.yaml
```yaml
bridge:
  host: "localhost"
  port: 8765
  websocket_path: "/ws"
  
reaper:
  extstate_method: true      # Use ExtState
  reascript_method: false    # Or use ReaScript API
  osc_method: false          # Or use OSC
  
effects:
  - name: CustomDelay
    parameters:
      - time
      - feedback
      - mix
    ranges:
      time: [0, 2000]
      feedback: [0, 100]
      mix: [0, 100]
```

---

## API Reference

### WebSocket Messages

**Client → Server (Set Parameter):**
```json
{
  "type": "set_param",
  "effect": "CustomDelay",
  "param": "time",
  "value": 750
}
```

**Server → Client (Parameter Update):**
```json
{
  "type": "param_update",
  "effect": "CustomDelay",
  "param": "time",
  "value": 750,
  "source": "automation"
}
```

**Server → Client (Connection Status):**
```json
{
  "type": "status",
  "connected": true,
  "effects": ["CustomDelay", "CustomReverb"]
}
```

---

## Integrations

### With Songster
```python
# Launch effect UI during song processing
from reaper_bridge import launch_effect_ui

effect_ui = launch_effect_ui('delay', track=1)
# Continue processing while UI is open
```

### With REAPER Actions
```lua
-- lua/launch_ui.lua
function launch_effect_ui(effect_name)
  os.execute("python bridge.py --effect " .. effect_name .. " &")
end
```

---

## Troubleshooting

### WebSocket Won't Connect
```bash
# Check bridge is running
curl http://localhost:8765/health

# Check firewall
sudo ufw allow 8765
```

### REAPER Not Reading Parameters
```javascript
// In JSFX, check ExtState access
@block
test = ext_get_value("MyEffect", "time", 0);
ext_noinit && ext_noinit = 0;
```

### React Changes Not Updating REAPER
- Check WebSocket connection status in browser console
- Verify effect name matches exactly (case-sensitive)
- Check REAPER ExtState values: `Preferences > Plug-ins > ReaScript`

---

## Contributing

This is a personal tool shared publicly. Contributions welcome:

- **Bug reports:** Open an issue with reproduction steps
- **Feature requests:** Describe your use case
- **Pull requests:** Keep them focused, well-documented
- **Effect examples:** Share your custom UIs

**No contribution too small.** Fixed a typo? Found a better approach? Share it.

---

## Philosophy

**Why this exists:**
- JSFX is powerful but UI-limited
- Modern web tools solve UI problems elegantly
- Musicians who code deserve better tools
- Open source enables experimentation

**What this is NOT:**
- Not a commercial product
- Not trying to replace REAPER's native UI
- Not a plugin standard (VST/AU/AAX)
- Not beginner-friendly (assumes dev skills)

**What this IS:**
- Personal infrastructure for creative work
- Shared because others might find it useful
- Experimental and evolving
- Built by musicians who code

---

## Background

Built by a 64-year-old guitarist with 50+ years of playing and 35+ years of professional software development (PE). 

Got tired of JSFX UI limitations while building custom effects. Wanted React's power and polish. Built a bridge. Works for me. Sharing it.

Part of the broader [Songster](https://github.com/owencorpening/songster) project - personal music production infrastructure.

---

## Related Projects

- **Songster:** Music production workflow automation
- **REAPER:** https://www.reaper.fm/
- **ReaPack:** Plugin package manager for REAPER
- **JSFX:** REAPER's built-in effect format

---

## License

MIT License - Use it, modify it, share it. Just credit the source.

See [LICENSE](LICENSE) for details.

---

## Contact

- **GitHub Issues:** Bug reports, questions, feature requests
- **Discussions:** Share your effect UIs, integration ideas
- **Substack:** https://owencorpening.substack.com/ (writing about the process)

---

**Status:** Experimental. Works for personal use. Shared for others who might find it useful.

**Last Updated:** October 2025