# Parametric Golf Wedge Designer

A Python-based tool using CadQuery to generate production-ready STEP files for CNC machining custom golf wedges.

## Overview

This tool allows you to specify wedge parameters (loft, bounce, sole geometry, etc.) and outputs machinist-ready 3D models. Start with proven designs like the Vokey 56°/8° and iterate to create your custom grinds.

## Features

- Parametric wedge geometry generation
- YAML-based configuration for easy customization
- Production-ready STEP file export
- Weight and center of gravity estimation
- Multiple grind profiles
- USGA-compliant groove patterns

## Quick Start

### Installation

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Generate Your First Wedge

```bash
# Generate the baseline Vokey 56°/8° clone
python src/wedge_generator.py --config configs/vokey_56_8.yaml

# Output will be in: output/step_files/vokey_56_8_[timestamp].step
```

### View Your Design

Open the generated STEP file in:
- FreeCAD (free, cross-platform)
- Fusion 360 (free for hobbyists)
- Any CAD software that supports STEP format

## Configuration

Edit `configs/vokey_56_8.yaml` to customize your wedge:

```yaml
wedge_specs:
  loft: 56          # Change to 52, 54, 58, 60, etc.
  bounce: 8         # Adjust bounce angle
  sole_width: 21    # Modify sole width
  # ... see file for all parameters
```

## Project Structure

```
wedge-designer/
├── src/
│   ├── wedge_generator.py    # Main geometry generator
│   ├── geometry/
│   │   ├── hosel.py          # Hosel component
│   │   ├── blade.py          # Blade/face component
│   │   └── sole.py           # Sole and grind profiles
│   ├── config_loader.py      # YAML configuration parser
│   └── utils.py              # Calculations and validation
├── configs/
│   ├── vokey_56_8.yaml       # Baseline Vokey-style specs
│   └── template.yaml         # Empty template for custom designs
├── output/
│   └── step_files/           # Generated STEP files go here
├── docs/
│   ├── fabricator_specs.md   # Specifications for machinist
│   └── development_plan.md   # Detailed implementation roadmap
├── tests/
│   └── test_basic.py         # Basic validation tests
├── requirements.txt
└── README.md
```

## Sending to Fabricator

1. Generate your STEP file using this tool
2. Provide the STEP file + `docs/fabricator_specs.md` to your machinist
3. They should be able to quote and manufacture from these files alone

## Development Roadmap

See `docs/development_plan.md` for the complete phase-by-phase implementation plan.

**Current Status:** Initial project structure created
**Next Phase:** Implement core hosel geometry (Phase 2.1)

## Requirements

- Python 3.9+
- CadQuery 2.x
- PyYAML
- NumPy

## Future Enhancements

- [ ] Multiple grind presets (S, M, K, L, D grinds)
- [ ] Interactive parameter adjustment
- [ ] Visual preview generation
- [ ] STL export for 3D printing prototypes
- [ ] Swingweight calculator integration
- [ ] Custom stamp/logo placement

## Resources

- [CadQuery Documentation](https://cadquery.readthedocs.io/)
- [USGA Groove Rules](https://www.usga.org/content/usga/home-page/equipment-standards.html)
- [Wedge Design Fundamentals](https://www.vokey.com/wedge-selector)

## License

MIT License - Use freely for personal or commercial wedge manufacturing

## Contributing

This is a personal project, but suggestions and improvements welcome via issues.

---

**Note for Claude Code:** This project is designed to be built incrementally. Start with Phase 1 (environment setup) and progress through each phase as documented in `docs/development_plan.md`.
