# REAPER React Bridge: Development Plan

## Quick Context

Building a bridge between React (modern UI) and REAPER (professional DAW) to create custom effect interfaces that don't suck.

**Current state:** Proof-of-concept with HTTP polling  
**Target state:** Production-ready WebSocket architecture with Python bridge

**Philosophy:** Personal infrastructure first, shareable tool second. Build features when I need them for actual music work.

---

## The Real Problem

### What I'm Solving
JSFX effects in REAPER are powerful but UI-limited:
- Built-in sliders are basic (circa 1995)
- No modern components (knobs, visualizers, responsive layouts)
- Limited styling and customization
- As a professional developer, I want professional tools

### What I'm NOT Solving
- Not replacing REAPER's native UI system
- Not building a VST/AU plugin wrapper
- Not creating a commercial product
- Not targeting non-developers

---

## Architecture Evolution

### Version 1.0 (Current/Proof-of-Concept)
```
React → HTTP requests → REAPER Web Control → ExtState → Lua → JSFX
```

**Problems:**
- HTTP polling is laggy
- Multiple middleware layers
- No real-time feedback
- Awkward to debug

### Version 2.0 (Target Architecture)
```
React ⟷ WebSocket ⟷ Python Bridge ⟷ REAPER (ExtState/ReaScript) ⟷ JSFX
```

**Improvements:**
- Real-time bidirectional updates
- Python handles REAPER quirks
- Clean separation of concerns
- Integrates with Songster workflows

---

## Development Phases

### Phase 1: Core Infrastructure (Week 1-2)
**Goal:** Get WebSocket communication working end-to-end

**Tasks:**
- [x] Design WebSocket message protocol
- [ ] Build Python FastAPI bridge
  - WebSocket server
  - REAPER ExtState integration
  - Basic health checks
- [ ] Create React useReaperEffect hook
  - WebSocket connection management
  - Parameter state synchronization
  - Connection status handling
- [ ] Test with simple slider example
- [ ] Document the protocol

**Success metric:** Change a React slider, hear JSFX parameter update in real-time

---

### Phase 2: Example Effect (Week 2-3)
**Goal:** One complete, polished effect UI

**Tasks:**
- [ ] Port existing CustomDelay JSFX
- [ ] Build React DelayEffect component
  - Time knob (0-2000ms)
  - Feedback knob (0-100%)
  - Mix slider (0-100%)
- [ ] Add basic visualization
- [ ] Handle edge cases (connection loss, REAPER restart)
- [ ] Write usage documentation

**Success metric:** Ship a delay effect UI I actually want to use

---

### Phase 3: Component Library (Week 3-4)
**Goal:** Reusable components for future effects

**Tasks:**
- [ ] Build or integrate knob component
  - Research: react-rotary-knob vs custom
  - Implement with proper touch/mouse handling
  - Add value display and units
- [ ] Build slider component
  - Horizontal and vertical variants
  - Smooth dragging with acceleration
- [ ] Build toggle/button components
- [ ] Build preset selector dropdown
- [ ] Create shared styling system
- [ ] Document component API

**Success metric:** Can build a new effect UI in <1 hour

---

### Phase 4: Developer Experience (Week 4-5)
**Goal:** Make it easy to create new effects

**Tasks:**
- [ ] Effect template generator
  - `python create_effect.py --name MyEffect`
  - Generates JSFX boilerplate
  - Generates React component boilerplate
  - Adds to config.yaml
- [ ] Hot reload for JSFX changes
- [ ] Parameter range validation
- [ ] Better error messages
- [ ] Development mode with debug UI

**Success metric:** New effect from idea to working UI in 15 minutes

---

### Phase 5: Polish & Features (Week 5-6)
**Goal:** Production-ready for personal use

**Tasks:**
- [ ] Preset management
  - Save/load presets from UI
  - Store in REAPER project data
  - Share presets as JSON
- [ ] MIDI learn integration
  - Click "learn" in UI
  - REAPER captures MIDI CC
  - Bind to parameter
- [ ] Multi-instance support
  - Multiple effect windows open
  - Each tracks different JSFX instance
- [ ] Keyboard shortcuts
- [ ] Responsive layouts (desktop/tablet)

**Success metric:** Actually prefer this over native REAPER UI

---

### Phase 6: Advanced Features (Future)
**Goal:** Nice-to-haves when needed

**Potential features:**
- [ ] OSC support (alternative to ExtState)
- [ ] ReaScript API integration (bypass ExtState)
- [ ] Audio visualization (waveform, spectrum)
- [ ] Multi-track control (bus effects)
- [ ] Integration with Songster workflows
- [ ] Mobile app (React Native)
- [ ] Modulation visualization
- [ ] A/B comparison mode

**Build these only when I need them for actual music work.**

---

## Technical Decisions

### Communication Layer: WebSocket (Chosen)
**Why:**
- Real-time bidirectional
- Efficient for parameter streams
- Standard protocol, many libraries
- Works in browsers natively

**Alternatives considered:**
- HTTP polling: Too laggy ❌
- OSC: Over-engineered for this ❌
- gRPC: Overkill ❌

### Python Bridge: FastAPI (Chosen)
**Why:**
- Modern, fast, async support
- WebSocket built-in
- Can serve React build
- Easy integration with Songster
- I know it well

**Alternatives considered:**
- Node.js: Adds another runtime ❌
- Pure Lua in REAPER: Too limited ❌
- Direct React to REAPER: Protocol mismatch ❌

### REAPER Integration: ExtState (Current)
**Why:**
- Simple key-value store
- Works across all REAPER versions
- JSFX can read it natively
- No external dependencies

**Future alternatives:**
- ReaScript API: More direct, needs Python extension
- OSC: More flexible, more complex

### React State Management: Context + Hooks (Chosen)
**Why:**
- Built-in, no extra dependencies
- Sufficient for parameter state
- Clean with useReaperEffect hook

**Alternatives considered:**
- Redux: Over-engineered ❌
- Zustand: Maybe later if needed
- Jotai: Interesting, but unnecessary

### UI Components: Start Custom, Evaluate Libraries Later
**Why:**
- Full control over behavior
- Learn what I actually need
- Can integrate libraries incrementally

**Libraries to evaluate:**
- react-rotary-knob
- react-input-slider
- wavesurfer.js (for visualization)
- tone.js (for audio analysis)

---

## Integration Points

### With Songster
```python
# Launch effect UI during song processing
from reaper_bridge import launch_effect_ui

def process_song_with_custom_reverb(mp3_path):
    stems = separate_stems(mp3_path)
    
    # Launch reverb UI for vocals
    reverb_ui = launch_effect_ui('reverb', track='vocals')
    
    # User adjusts reverb while stems play
    # Continue when satisfied
```

### With REAPER Actions
```lua
-- Custom action to launch UI
function launch_delay_ui()
  local track = reaper.GetSelectedTrack(0, 0)
  os.execute("python bridge.py --effect delay --track " .. track)
end
```

### With External Controllers
```python
# MIDI controller integration
def midi_learn(param_name):
    # Listen for MIDI CC
    # Bind to parameter
    # Update both REAPER and React UI
```

---

## Testing Strategy

### Unit Tests
- Python bridge functions
- React hooks
- WebSocket message parsing
- Parameter validation

### Integration Tests
- Full message flow (React → Python → REAPER)
- Connection loss recovery
- Multi-instance handling
- Preset save/load

### Manual Testing
- Real music production use
- Different REAPER versions
- Different OS (Linux primary, Mac/Windows secondary)
- Performance with multiple effects

**Philosophy:** Test what matters. I'm the primary user, so real-world use is the best test.

---

## Performance Considerations

### WebSocket Message Rate
- Target: <10ms parameter update latency
- Throttle rapid changes (mousemove) to 60fps
- Batch multiple parameter changes
- Monitor WebSocket queue depth

### REAPER ExtState Access
- JSFX reads ExtState every @block (typically 64-512 samples)
- Acceptable latency for most effects
- For real-time needs, consider ReaScript API

### React Rendering
- Debounce non-critical UI updates
- Use React.memo for expensive components
- Virtual scroll for large preset lists
- Profile with React DevTools

**Philosophy:** Optimize when it's noticeable. Premature optimization is the root of all evil.

---

## Deployment Strategy

### Development
```bash
# Terminal 1: Python bridge with hot reload
python bridge.py --dev

# Terminal 2: React dev server
cd react-ui && npm start

# Terminal 3: REAPER
# Add effect, open UI, iterate
```

### Personal Use (Production)
```bash
# Build React
cd react-ui && npm run build

# Run bridge (serves built React)
python bridge.py --production

# Add to REAPER startup script
```

### Sharing (If Others Want It)
```bash
# Install script
./install.sh

# Copies JSFX to REAPER
# Sets up Python environment
# Builds React UI
# Creates launcher scripts
```

---

## Documentation Plan

### For Me (Primary)
- README.md: Quick reference, architecture overview
- PLAN.md: This file - ongoing strategy
- API.md: WebSocket protocol, message formats
- Each component: JSDoc comments explaining why, not just what

### For Others (Secondary)
- Getting Started guide
- Effect creation tutorial
- Troubleshooting common issues
- Video walkthrough (maybe, if people care)

**Philosophy:** Document for future me first. If it helps others, great.

---

## Success Metrics

### Phase 1-2: Minimum Viable Bridge
- ✅ WebSocket latency <10ms
- ✅ Can control one JSFX effect from React
- ✅ Connection survives REAPER restart
- ✅ Clear error messages when things break

### Phase 3-4: Daily Use Ready
- ✅ Used for actual music production
- ✅ Prefer it over REAPER's native UI
- ✅ Can create new effect UI in <1 hour
- ✅ Hasn't crashed in a week

### Phase 5-6: Share-Worthy
- ✅ Documentation complete
- ✅ Install process tested
- ✅ GitHub repo clean and organized
- ✅ At least 2 complete effect examples

**If it's only me using it, that's success.**  
**If others find it useful, that's a bonus.**

---

## Known Challenges

### Challenge 1: REAPER API Limitations
**Problem:** ExtState is simple but limited
**Solutions:**
- Start with ExtState (good enough)
- Add ReaScript API support later if needed
- OSC as fallback for complex cases

### Challenge 2: React Build Complexity
**Problem:** npm, webpack, build pipeline
**Solutions:**
- Python bridge serves built React automatically
- Development mode with hot reload
- Clear documentation of setup steps

### Challenge 3: Cross-Platform Support
**Problem:** Different OS, REAPER versions
**Solutions:**
- Primary target: Ubuntu Studio (my environment)
- Document differences for Mac/Windows
- Community can contribute platform-specific fixes

### Challenge 4: State Synchronization
**Problem:** REAPER automation vs UI changes
**Solutions:**
- UI always shows REAPER's actual value
- Bidirectional WebSocket updates
- Visual indicator when values diverge

---

## Why This Approach Works

### Personal Infrastructure Philosophy
- **Built for real use:** Every feature solves a problem I have
- **Iterate in context:** Test during actual music production
- **No imagined markets:** Not trying to serve hypothetical users
- **Sustainable pace:** 64 years old, retired, no deadlines

### Technical Philosophy
- **Modern tools:** React/Python because they're good at what they do
- **Simple protocols:** WebSocket + JSON is sufficient
- **Modular design:** Can swap React for something else later
- **Fail loudly:** Errors should be obvious, not silent

### Sharing Philosophy
- **Document for myself:** If others understand it, bonus
- **No support promises:** Community help is welcome, not expected
- **Open everything:** MIT license, no secrets
- **Honest framing:** Personal tool that might be useful to others

---

## Timeline (Realistic)

### Weeks 1-2: Core Infrastructure
Get basic WebSocket communication working

### Weeks 3-4: First Complete Effect
One polished example (CustomDelay)

### Weeks 5-6: Component Library
Reusable pieces for future effects

### Weeks 7-8: Polish & Real Use
Actually use it for music production, fix what's annoying

### Month 3+: Advanced Features
Build what I need when I need it

**No hard deadlines.** Build when inspired, use when needed.

---

## What Could Derail This

### Risk 1: WebSocket Performance Issues
**Mitigation:** Profile early, optimize message rate

### Risk 2: REAPER API Proves Insufficient
**Mitigation:** Have ReaScript/OSC fallback plans

### Risk 3: React Build Complexity
**Mitigation:** Keep it simple, document thoroughly

### Risk 4: Loss of Interest
**Mitigation:** Only build features I actually need

**Most likely outcome:** It works for me, maybe helps a few others, and that's perfectly fine.

---

## Future Possibilities (Dream Big, Build Small)

### If This Works Well
- Create effect packs (delay, reverb, compressor, EQ)
- Mobile app for remote control
- Integration with hardware controllers
- Visual programming for effect chains
- Community effect marketplace

### If Others Get Excited
- Accept contributions
- Create video tutorials
- Write about the process on Substack
- Maybe a Discord for collaborators

### If It Stays Personal
- Keep using it for my music
- Share the code openly
- Update when I need features
- No pressure, just tools

---

## Related Context

This is part of my broader music production infrastructure:

- **Songster:** MP3 → practice-ready REAPER projects
- **This Project:** Better UIs for custom effects
- **Future:** Integration between them

**The vision:** Complete control over my creative tools, from song prep to effect design to final production.

**The reality:** I'm 64, retired, making music with professional-grade custom tools because I can.

---

## Next Immediate Steps

1. **Create the GitHub repo** ✓ (about to do)
2. **Build Python bridge** (Week 1)
3. **Build React hook** (Week 1)
4. **Test with simple example** (Week 1)
5. **Write about the process** (Substack)

---

## Questions I Can Answer

**Q: Is this a product?**  
A: No. Personal infrastructure, shared openly.

**Q: Will you add feature X?**  
A: If I need it for my music, probably. Otherwise, pull requests welcome.

**Q: Why not use [existing solution]?**  
A: Tried them. Didn't fit my workflow. Building what I need.

**Q: Can I use this commercially?**  
A: Yes (MIT license), but it's experimental personal tooling.

**Q: Will you support this long-term?**  
A: As long as I'm making music and building effects, yes.

---

## Final Thought

**This isn't a product looking for users.**  
**It's a craftsperson's workshop with the door open.**

I'm building tools I need, documenting the process, and sharing the code. If it helps you build better effect UIs, great. If not, that's fine too. I'll still be here, making music with professional custom tools.

---

*Last updated: October 2025*  
*Living document - evolves as the work evolves*