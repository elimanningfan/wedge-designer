# PROJECT BRIEF: Parametric Golf Wedge Designer

## Mission
Build a Python tool using CadQuery that generates production-ready STEP files for CNC machining custom golf wedges. This tool enables rapid iteration of wedge designs by allowing users to specify parameters and export machinist-ready 3D models.

## Context
The user is developing their first custom wedge and wants to use modern CAD-to-CNC workflow rather than traditional hand-grinding. They understand wedge grinds and specifications but need a parametric tool to generate accurate 3D models for local fabrication.

## Initial Target: Vokey 56°/8° Clone
Start with a proven design - a Titleist Vokey-style 56° wedge with 8° bounce (versatile F/M grind). This serves as the baseline to validate the tool before exploring custom designs.

## Technical Approach
- **Language:** Python 3.9+
- **CAD Library:** CadQuery (parametric 3D modeling via Python)
- **Configuration:** YAML files for easy parameter adjustment
- **Output:** STEP files (industry standard for CNC machining)
- **Validation:** Weight estimation, CG calculation, dimension checking

## Critical Success Factors

### 1. Manufacturability
- Generated STEP files must open cleanly in any CAD software
- All dimensions within ±0.1mm tolerance
- No gaps, overlaps, or non-manifold geometry
- Surfaces must be smooth and machinable

### 2. Accuracy
- Hosel bore must be exactly 0.370" (9.4mm) for standard shafts
- Loft and lie angles must be precise
- Bounce angle measured correctly at center of sole
- Weight estimation within ±10g of target

### 3. Usability
- Simple YAML config files (no code editing required)
- Fast regeneration (<30 seconds per wedge)
- Clear validation output
- Comprehensive fabricator documentation

## Key Specifications (Vokey 56°/8° Baseline)

### Primary Geometry
- **Loft:** 56°
- **Lie:** 64°
- **Bounce:** 8° (center of sole)
- **Face progression:** 2.5mm

### Blade Dimensions
- **Length (heel-to-toe):** 74mm
- **Face height:** 49mm
- **Topline thickness:** 3.0mm
- **Target weight:** 292g

### Hosel (CRITICAL - Must be exact)
- **Bore diameter:** 0.370" (9.4mm) - standard shaft fitting
- **Bore depth:** 38mm
- **Outer diameter:** 14.5mm (tapers from 15mm)
- **Height:** 42mm

### Sole Design (The Art of Wedge Making)
- **Width at center:** 21mm
- **Leading edge radius:** 0.6mm
- **Trailing edge relief:** 2mm starting 15mm from back
- **Heel relief:** 1.5° camber beginning 12mm from heel
- **Toe relief:** 2° camber beginning 18mm from toe
- **Bounce rocker:** 180mm radius (subtle front-to-back curve)

### Face & Grooves
- **Groove spacing:** 3.81mm (USGA maximum)
- **Groove width:** 0.9mm (V-groove)
- **Groove depth:** 0.4mm
- **Number of grooves:** 11-12
- **Edge clearance:** 3mm from heel/toe

### Material
- **Steel:** 8620 carbon steel (soft, great feel)
- **Heat treatment:** 50-52 HRC on face
- **Finish:** Raw or chrome (specify for machinist)

## Development Phases (See development_plan.md for details)

1. **Environment Setup** - Project structure, CadQuery installation
2. **Core Geometry** - Hosel, basic blade, loft/lie angles
3. **Advanced Sole** - Grinds, reliefs, bounce curves
4. **Face Details** - Groove patterns, surface specs
5. **Configuration System** - YAML-driven parameters
6. **Validation Tools** - Weight, CG, dimension checking
7. **Export & Documentation** - STEP output, fabricator specs
8. **Testing** - Multiple designs, parameter variations
9. **Polish** - Code cleanup, examples, final docs

## Deliverables

1. ✅ Working Python codebase (modular, well-documented)
2. ✅ YAML configuration system
3. ✅ STEP file export functionality
4. ✅ Fabricator specification document
5. ✅ Weight/CG validation tools
6. ✅ Example wedge designs (3-4 variations)
7. ✅ Complete usage documentation

## Why This Matters

Traditional wedge making requires years of grinding experience. This tool democratizes wedge design by:
- Allowing rapid iteration (test 10 grinds vs. grinding 10 physical clubs)
- Enabling precise, repeatable designs
- Reducing cost (one STEP file → multiple machined heads)
- Preserving knowledge (designs stored as code/config)

Once validated with the Vokey clone, the user can explore custom grinds for their specific swing and course conditions.

## Constraints & Considerations

- **No GUI (yet):** Start with command-line tool, YAML configs
- **8620 Carbon Steel:** Soft, requires heat treatment (document for machinist)
- **USGA Compliance:** Groove spacing must meet rules if user cares about conforming clubs
- **Local Fabrication:** Generated files must work with standard CNC shops (no exotic requirements)

## Getting Started with Claude Code

**First command to Claude Code:**
"I'm building a parametric golf wedge designer using CadQuery. Let's start by setting up the project structure, installing dependencies, and creating a simple test that exports a cylinder as a STEP file to verify CadQuery is working. Use the project structure defined in README.md."

**Suggested approach:**
- Build incrementally (hosel first, then blade, then sole complexity)
- Test exports after each component
- Validate dimensions early and often
- Keep code modular (easy to swap grind algorithms)

---

**Bottom Line:** This isn't just a coding project - it's a tool that bridges traditional clubmaking craftsmanship with modern CAD/CAM manufacturing. The goal is precision, speed, and creative exploration of wedge design.
