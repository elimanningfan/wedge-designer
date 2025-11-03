# 🌐 Start the Web Interface

## Quick Start

Run the web interface on localhost:8000:

```bash
# Option 1: Direct command
streamlit run app.py --server.port 8000

# Option 2: Use the startup script
./run_web.sh
```

The web UI will open automatically in your browser at **http://localhost:8000**

---

## Features

### 🎛️ Interactive Controls
- **Real-time parameter adjustment** with sliders
- **Loft, lie, bounce** angle controls
- **Blade dimensions** (length, height, topline)
- **Sole design** (width, heel/toe relief)
- **Hosel specifications** (bore diameter, depth)
- **Groove settings** (count, spacing, width, depth)

### 🎨 Design Feedback
- **Grind profile description** based on your settings
- **USGA compliance check** for groove spacing
- **Weight and CG estimates** after generation
- **Validation warnings** for non-standard dimensions

### 📥 Generate & Download
- **One-click generation** of STEP files
- **Direct download** button
- **File size and metrics** displayed
- **Progress feedback** during generation

### 📊 Visual Summary
- **Design metrics** at a glance
- **Grind type classification** (S, K, L, F/M styles)
- **Compliance indicators** (USGA, standard bore)
- **Target vs actual** weight comparison

---

## Usage Instructions

### 1. Launch the Web UI
```bash
streamlit run app.py --server.port 8000
```

### 2. Adjust Parameters
Use the **left sidebar** to modify:
- Primary angles (loft, lie, bounce)
- Blade dimensions
- Sole design (width, relief angles)
- Hosel specifications
- Groove settings
- Target weight

### 3. Review Summary
The **main panel** shows:
- Current design metrics
- Grind profile description
- USGA compliance status
- Bore diameter warnings (if non-standard)

### 4. Generate Wedge
Click **"Generate STEP File"** in the right panel:
- Watch real-time progress
- See validation results
- View weight and CG calculations

### 5. Download
Click **"Download STEP File"** to save:
- Opens in any CAD software (FreeCAD, Fusion 360)
- Ready for CNC machining
- Includes all features (hosel, blade, sole, grooves)

---

## Example Configurations

### Versatile 56°/8° (Baseline)
```
Loft: 56°
Lie: 64°
Bounce: 8°
Sole Width: 21mm
Heel Relief: 1.5°
Toe Relief: 2.0°
```
**Result:** F/M-grind style, works from most lies

### High Bounce Bunker Wedge
```
Loft: 60°
Lie: 64°
Bounce: 12°
Sole Width: 24mm
Heel Relief: 1.0°
Toe Relief: 1.0°
```
**Result:** K-grind style, bunker specialist

### Low Bounce Sweeper
```
Loft: 54°
Lie: 64°
Bounce: 6°
Sole Width: 18mm
Heel Relief: 0.5°
Toe Relief: 0.5°
```
**Result:** L-grind style, for firm conditions

### Versatile High-Relief
```
Loft: 58°
Lie: 64°
Bounce: 10°
Sole Width: 20mm
Heel Relief: 3.0°
Toe Relief: 3.5°
```
**Result:** S-grind style, can open/close face

---

## Tips for Web UI

### ⚠️ Critical Parameters
- **Hosel bore diameter:** Keep at 9.4mm (0.370") for standard shafts
- **Groove spacing:** Keep ≤ 3.81mm for USGA compliance
- **Weight:** Target 285-300g for standard wedges

### 🎯 Design Strategy
1. **Start with baseline** (56/8 config)
2. **Adjust one parameter** at a time
3. **Generate and review** metrics
4. **Iterate** until satisfied
5. **Download and inspect** in CAD software

### 🔧 Common Adjustments
- **More forgiveness:** Increase bounce + sole width
- **More versatility:** Increase heel/toe relief
- **Tighter lies:** Decrease bounce + sole width
- **Bunker play:** Increase bounce to 10-14°

---

## Troubleshooting

### Port Already in Use
If port 8000 is busy:
```bash
streamlit run app.py --server.port 8001
```

### Slow Generation
First generation may take longer (10-15 seconds) due to:
- CadQuery initialization
- Geometry calculations
- STEP file export

Subsequent generations are faster (5-8 seconds).

### Weight Too Heavy
Current geometry is simplified and weighs ~410g.
This is expected for Phase 1 implementation.
Future enhancements will add mass reduction features.

### Download Not Working
Make sure the STEP file generated successfully:
- Check for green "✓ Wedge generated successfully!" message
- Look for download button to appear
- Check `output/step_files/` directory

---

## Keyboard Shortcuts

- **Ctrl+C** in terminal: Stop server
- **R** in browser: Rerun app (refresh parameters)
- **C** in browser: Clear cache
- **F** in browser: Toggle fullscreen

---

## What to Do Next

1. **Generate a few wedges** with different parameters
2. **Download the STEP files**
3. **Open in FreeCAD** or Fusion 360
4. **Inspect geometry** (zoom in on grooves, sole, hosel bore)
5. **Measure dimensions** to verify accuracy
6. **Send to fabricator** with `docs/fabricator_specs.md`

---

## Benefits of Web UI vs Command Line

| Feature | Web UI | Command Line |
|---------|--------|--------------|
| Parameter adjustment | Interactive sliders | Edit YAML file |
| Visual feedback | Real-time summary | Text output only |
| Quick iteration | Instant changes | Re-run command |
| Learning curve | Intuitive GUI | Requires docs |
| Batch generation | Manual (one at a time) | Easy with scripts |
| Customization | Predefined controls | Full YAML flexibility |

**Recommendation:** Use Web UI for exploration and design, command line for batch production.

---

🏌️ **Happy wedge designing!** Open http://localhost:8000 and start creating!
