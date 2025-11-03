# 🏌️ START HERE - Wedge Designer Project Launch Guide

Welcome to your Parametric Golf Wedge Designer project! This guide will get you up and running in minutes.

---

## 📦 What You've Got

Your project is fully structured and ready to build:

```
wedge-designer/
├── 📄 README.md                    # Project overview and documentation
├── 📄 PROJECT_BRIEF.md             # Mission, context, and specifications
├── 📄 requirements.txt             # Python dependencies
│
├── 📁 src/                         # Source code (Python modules)
│   ├── wedge_generator.py         # Main orchestrator (entry point)
│   ├── config_loader.py           # YAML configuration parser
│   ├── utils.py                   # Weight, CG, validation tools
│   └── geometry/                  # Geometry generation modules
│       ├── __init__.py
│       ├── hosel.py               # Hosel geometry
│       ├── blade.py               # Blade/face geometry
│       └── sole.py                # Sole and grind profiles
│
├── 📁 configs/                     # Configuration files
│   └── vokey_56_8.yaml            # Baseline Vokey 56°/8° specs
│
├── 📁 docs/                        # Documentation
│   ├── development_plan.md        # Phase-by-phase implementation guide
│   └── fabricator_specs.md        # Specifications for machinist
│
├── 📁 tests/                       # Test scripts
│   └── test_basic.py              # CadQuery installation test
│
└── 📁 output/
    └── step_files/                # Generated STEP files go here
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
cd wedge-designer

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install CadQuery and dependencies
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
python tests/test_basic.py
```

**Expected output:**
```
Testing CadQuery installation...
CadQuery version: 2.x.x
Creating test cylinder...
Exporting to: output/step_files/test_cylinder.step
✓ Success! Test cylinder exported (XXXX bytes)

CadQuery is properly installed and working!
```

### Step 3: Launch with Claude Code
Now you're ready to start building! Use Claude Code to implement the actual geometry.

**Copy this command to Claude Code:**
```
I'm building a parametric golf wedge designer using CadQuery. 

The project structure is already set up in /home/claude/wedge-designer with:
- Configuration system (YAML-based)
- Utilities for weight/CG calculations
- Placeholder geometry modules for hosel, blade, and sole

Please read PROJECT_BRIEF.md and docs/development_plan.md to understand the mission and approach.

Then let's start with Phase 2.1: Implement the hosel geometry in src/geometry/hosel.py. 
The hosel should create a cylinder with a precise bore for golf shaft fitting.

Key specs for hosel (from configs/vokey_56_8.yaml):
- Height: 42mm
- Outer diameter: 14.5mm  
- Bore diameter: 9.4mm (0.370" - critical dimension!)
- Bore depth: 38mm

After implementing, we'll test by exporting a standalone hosel STEP file.
```

---

## 📋 Implementation Roadmap

Follow `docs/development_plan.md` for detailed phase-by-phase guidance:

**Phase 1:** ✅ Environment Setup (COMPLETE)
**Phase 2:** Core Geometry (hosel → blade → sole) - **START HERE**
**Phase 3:** Advanced Sole (grinds, reliefs, rockers)
**Phase 4:** Face Details (grooves)
**Phase 5:** Parametric Config System
**Phase 6:** Validation Tools
**Phase 7:** Export & Documentation
**Phase 8:** Testing & Iteration
**Phase 9:** Polish & Delivery

**Estimated time:** 17-24 hours active development

---

## 🎯 Key Files to Know

### For Claude Code to Read:
1. **PROJECT_BRIEF.md** - Understanding the mission and specifications
2. **docs/development_plan.md** - Step-by-step implementation guide
3. **configs/vokey_56_8.yaml** - All the specs for the baseline wedge
4. **docs/fabricator_specs.md** - What the machinist needs

### Code You'll Build:
1. **src/geometry/hosel.py** - First component to implement
2. **src/geometry/blade.py** - Second component
3. **src/geometry/sole.py** - Most complex (the art!)
4. **src/wedge_generator.py** - Orchestrates everything

### Generated Output:
- **output/step_files/** - Your STEP files will appear here
- Open in FreeCAD, Fusion 360, or any CAD software

---

## 🔑 Critical Specifications (Don't Forget!)

From `configs/vokey_56_8.yaml`:

**Hosel (MOST CRITICAL):**
- Bore diameter: **9.4mm (0.370")** - Must be exact for shaft fitting!
- Bore depth: 38mm

**Angles:**
- Loft: 56°
- Lie: 64°
- Bounce: 8°

**Dimensions:**
- Blade length: 74mm
- Face height: 49mm
- Sole width (center): 21mm
- Target weight: 292g

**Material:**
- 8620 carbon steel (7.85 g/cm³)

---

## 🧪 Testing Your Work

After implementing each component:

```bash
# Test hosel generation
python src/geometry/hosel.py

# Test blade generation  
python src/geometry/blade.py

# Test complete wedge generation
python src/wedge_generator.py --config configs/vokey_56_8.yaml
```

Open generated STEP files in FreeCAD (free) to inspect geometry.

---

## 📐 Design Philosophy

**Build incrementally:**
1. Start simple (hosel cylinder with bore)
2. Test frequently (export STEP files after each component)
3. Add complexity gradually (flat sole → ground sole → grooves)
4. Validate dimensions (weight, CG, critical tolerances)

**The art is in the sole:**
- Phase 2: Basic flat sole (just bounce angle)
- Phase 3: Advanced grinds (heel/toe relief, rockers)
- This is where wedge performance comes alive

---

## 🛠️ Tools & Resources

**CAD Viewers (Free):**
- FreeCAD: https://www.freecad.org/
- Fusion 360: https://www.autodesk.com/products/fusion-360 (free for hobbyists)

**CadQuery Documentation:**
- Docs: https://cadquery.readthedocs.io/
- Examples: https://github.com/CadQuery/cadquery/tree/master/examples

**Golf Wedge Design:**
- Vokey wedge selector: https://www.vokey.com/wedge-selector
- Understanding bounce/grinds: Built into your config!

---

## 🎓 Learning Notes

**If you're new to CadQuery:**
- It's Python-based CAD (code → 3D models)
- Chainable operations: `cq.Workplane("XY").rect(10,5).extrude(3)`
- Think in terms of: create shapes → combine → subtract → fillet

**Golf wedge basics:**
- **Loft:** Face angle (determines trajectory)
- **Lie:** Shaft angle (affects strike pattern)
- **Bounce:** Sole angle (prevents digging)
- **Grind:** Heel/toe relief (adds versatility)

---

## ✅ Success Criteria

You'll know you're done when:
- [ ] Generate valid STEP files from YAML config
- [ ] Hosel bore is exactly 9.4mm
- [ ] Weight within ±5g of target (292g)
- [ ] Grooves are USGA-compliant spacing
- [ ] Sole has proper grind profile
- [ ] Fabricator can quote from STEP file alone

---

## 🚨 Common Issues

**CadQuery won't install:**
- Make sure you're using Python 3.9+
- Try: `pip install --upgrade pip` first
- See: https://cadquery.readthedocs.io/en/latest/installation.html

**STEP files won't open:**
- Check file size (should be >10KB)
- Try different CAD software
- Verify geometry is valid (no gaps/errors)

**Dimensions off:**
- Check units (everything in millimeters)
- Validate after each component
- Use `utils.py` validation functions

---

## 🎯 Your First Goal

**Implement hosel geometry (Phase 2.1):**

The hosel is the simplest component - a cylinder with a bore. This validates:
1. CadQuery is working
2. You can create geometry
3. You can export STEP files
4. Critical dimensions are accurate

Once the hosel works, the rest follows the same pattern!

---

## 📞 Next Steps

1. ✅ Dependencies installed (`pip install -r requirements.txt`)
2. ✅ Installation tested (`python tests/test_basic.py`)
3. 🔄 **Launch Claude Code** with the command above
4. 🔄 Implement hosel geometry (Phase 2.1)
5. 🔄 Test hosel STEP export
6. 🔄 Move to blade, then sole...

---

## 💡 Pro Tips

- **Read the development plan first** - it has all the details
- **Test after every component** - don't wait until the end
- **Visualize early and often** - open STEP files in FreeCAD
- **Start with flat sole** - add grinds in Phase 3
- **Validate dimensions** - especially the hosel bore!

---

**Ready?** Copy the Claude Code command above and start building!

The project structure is complete. The specs are defined. The roadmap is clear.

Now it's time to turn code into clubs. 🏌️⛳

---

*This project bridges traditional clubmaking craftsmanship with modern CAD/CAM manufacturing. You're not just writing code - you're designing a tool that lets you iterate wedge designs faster than any club maker in history could grind them by hand.*

**Let's build something great!**
