# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based parametric golf wedge designer using CadQuery to generate production-ready STEP files for CNC machining custom golf wedges. The tool enables rapid iteration of wedge designs through YAML configuration files, outputting machinist-ready 3D models.

**Current Status:** Initial project structure created (Phase 1 complete)
**Next Phase:** Implement core hosel geometry (Phase 2.1)

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify CadQuery installation
python -c "import cadquery as cq; print(f'CadQuery {cq.__version__} installed')"
```

### Testing
```bash
# Test CadQuery installation (generates test cylinder)
python tests/test_basic.py

# Test individual geometry components
python src/geometry/hosel.py
python src/geometry/blade.py
python src/geometry/sole.py

# Test configuration loader
python src/config_loader.py
```

### Generate Wedge
```bash
# Generate wedge from configuration
python src/wedge_generator.py --config configs/vokey_56_8.yaml

# Specify custom output directory
python src/wedge_generator.py --config configs/vokey_56_8.yaml --output output/custom/
```

## High-Level Architecture

### Component-Based Geometry Generation

The wedge is built from three primary geometric components that are generated independently and then combined:

1. **Hosel** (`src/geometry/hosel.py`): Cylindrical component connecting clubhead to shaft
   - Critical dimension: 9.4mm bore diameter (0.370" standard shaft)
   - Must be exact for shaft fitting
   - First component to implement (simplest)

2. **Blade** (`src/geometry/blade.py`): Main hitting surface and body
   - Includes face, topline, heel/toe profiles
   - Incorporates loft angle (face angle)
   - Incorporates lie angle (shaft angle to ground)

3. **Sole** (`src/geometry/sole.py`): Where the art of wedge design lives
   - **Phase 2.4**: Start with flat sole at bounce angle
   - **Phase 3**: Add advanced features (grinds, reliefs, rockers)
   - Bounce angle, heel/toe relief, leading/trailing edge treatment
   - This is the most complex component

### Configuration-Driven Design

All wedge parameters are defined in YAML files (`configs/`):
- `vokey_56_8.yaml`: Baseline Vokey-style 56°/8° wedge (versatile F/M grind)
- `template.yaml`: Empty template for custom designs

The `config_loader.py` module parses YAML and validates parameters using dot-notation access (e.g., `config.get('wedge_specs.hosel.bore_diameter')`).

### Main Orchestrator

`wedge_generator.py` is the entry point that:
1. Loads configuration from YAML
2. Instantiates geometry components (hosel, blade, sole)
3. Combines components into complete wedge
4. Runs validation (weight, CG, dimensions)
5. Exports to STEP format with timestamped filename

### Validation Pipeline

`utils.py` provides validation functions that run before export:
- **Weight estimation**: Calculate volume × material density (8620 steel = 7.85 g/cm³), target 292g ±5g
- **Center of gravity**: Calculate and compare to target CG position
- **Dimension validation**: Verify critical dimensions (hosel bore, blade length, etc.)
- **Geometry validation**: Ensure manifold solid (no gaps, overlaps, or non-manifold geometry)

## Critical Specifications

### Non-Negotiable Dimensions
- **Hosel bore diameter**: 9.4mm (0.370") - must be exact for standard shaft fitting
- **Hosel bore depth**: 38mm
- **Material density**: 8620 carbon steel at 7.85 g/cm³ for weight calculations

### Angles (Vokey 56/8 baseline)
- **Loft**: 56° (face angle)
- **Lie**: 64° (shaft angle to ground)
- **Bounce**: 8° (measured at center of sole)

### Target Metrics
- **Head weight**: 292g ±5g tolerance
- **Groove spacing**: 3.81mm (USGA maximum, cannot exceed)

## Implementation Approach

### Build Incrementally (Phase-by-Phase)

Follow `docs/development_plan.md` for detailed guidance. Key phases:

1. **Phase 1** (✅ Complete): Environment setup
2. **Phase 2** (Current): Core geometry
   - 2.1: Hosel (cylinder with bore) - **START HERE**
   - 2.2: Blade profile (rectangular, no complex sole)
   - 2.3: Loft/lie angles (position and rotate blade)
   - 2.4: Basic flat sole (bounce angle only)
3. **Phase 3**: Advanced sole (leading edge, trailing edge relief, heel/toe relief, bounce rocker)
4. **Phase 4**: Face details (groove patterns, USGA compliance)
5. **Phase 5**: Parametric config system (make all dimensions YAML-driven)
6. **Phase 6**: Validation tools (weight, CG, dimension checking)
7. **Phase 7**: Export & documentation
8. **Phase 8**: Testing & iteration (multiple wedge designs)
9. **Phase 9**: Polish & delivery

### Test After Each Component

Export STEP files frequently to validate geometry:
- Hosel alone: `output/hosel_only.step`
- Blade profile: `output/blade_profile.step`
- Basic wedge: `output/basic_wedge_no_sole.step`
- Flat sole: `output/wedge_flat_sole.step`
- With grind: `output/wedge_with_grind.step`

Open STEP files in FreeCAD (free) or Fusion 360 to visually inspect geometry.

### The Art is in the Sole (Phase 3)

The sole grind is what differentiates wedges:
- **Heel relief**: Additional camber at heel (1.5° for Vokey baseline) - allows opening face without digging
- **Toe relief**: Additional camber at toe (2° for Vokey baseline) - enables square/closed face versatility
- **Leading edge radius**: Subtle 0.6mm radius (not sharp, not blunt)
- **Trailing edge relief**: 2mm relief starting 15mm from back edge - prevents digging when hitting down
- **Bounce rocker**: 180mm radius front-to-back curve - helps club glide through turf

Use CadQuery's loft/spline operations to create smooth transitions between different bounce angles along the sole.

## Code Organization

### Geometry Modules Pattern

Each geometry component follows this structure:
```python
class WedgeComponent:
    def __init__(self, config: Dict):
        # Extract parameters from config dict
        self.param1 = config.get('param1', default)

    def generate(self) -> cq.Workplane:
        # Generate CadQuery geometry
        # Return Workplane object

    def validate(self) -> bool:
        # Validate parameters are within acceptable ranges
        # Raise ValueError if invalid
```

### Configuration Access Pattern

Use dot-notation for nested YAML access:
```python
config = load_config('configs/vokey_56_8.yaml')
loft = config.get('wedge_specs.loft')  # Returns 56
bore = config.get('wedge_specs.hosel.bore_diameter')  # Returns 9.4
```

### Units Consistency

All dimensions in **millimeters**, all angles in **degrees**, all weights in **grams**.

## Important Context

### Manufacturability is Critical

Generated STEP files must:
- Open cleanly in any CAD software
- Have all dimensions within specified tolerances
- Contain no gaps, overlaps, or non-manifold geometry
- Have smooth, machinable surfaces

The fabricator should be able to quote and manufacture from the STEP file + `docs/fabricator_specs.md` alone.

### Material Considerations

8620 carbon steel is soft (requires heat treatment):
- Face hardness: 50-52 HRC after heat treatment
- Body hardness: 30-35 HRC (softer for feel)
- Document heat treatment requirements for machinist

### USGA Compliance

If conforming clubs are desired:
- Groove spacing: 3.81mm maximum (cannot exceed)
- Groove width: 0.9mm for V-groove
- Groove depth: 0.4mm
- Edge clearance: 3mm from heel/toe

## Development Workflow

1. Read `PROJECT_BRIEF.md` for mission and specifications
2. Follow `docs/development_plan.md` phase-by-phase
3. Implement geometry in order: hosel → blade → sole
4. Test each component by exporting standalone STEP files
5. Validate dimensions early and often
6. Keep code modular (easy to swap grind algorithms later)
7. Use `utils.py` validation functions before final export

## Next Steps (Phase 2.1)

Implement hosel geometry in `src/geometry/hosel.py`:
1. Create outer cylinder (height=42mm, diameter=14.5mm)
2. Create bore (depth=38mm, diameter=9.4mm)
3. Subtract bore from outer cylinder
4. Export test file to verify dimensions
5. Validate bore diameter is exactly 9.4mm

This validates CadQuery workflow before moving to more complex components.
