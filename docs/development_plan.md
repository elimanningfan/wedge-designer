# Development Plan: Parametric Golf Wedge Designer

**Project Goal:** Build a Python/CadQuery tool that generates production-ready STEP files for custom golf wedges.

**Estimated Timeline:** 17-24 hours active development (spread over 3-5 work sessions)

---

## PHASE 1: Environment Setup (30 minutes)

### Step 1.1 - Initialize Project Structure
**Status:** ✅ COMPLETE (pre-built structure provided)

**Directory structure:**
```
wedge-designer/
├── src/
│   ├── geometry/           # Geometry component modules
│   ├── wedge_generator.py  # Main orchestrator
│   ├── config_loader.py    # YAML parser
│   └── utils.py            # Helper functions
├── configs/                # YAML configuration files
├── output/step_files/      # Generated STEP files
├── docs/                   # Documentation
├── tests/                  # Test scripts
├── requirements.txt
└── README.md
```

### Step 1.2 - Install Dependencies
**Command:**
```bash
cd wedge-designer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Dependencies:**
- `cadquery>=2.4.0` - Core 3D modeling library
- `pyyaml>=6.0` - Configuration file parsing
- `numpy>=1.24.0` - Numerical calculations

**Validation:**
```bash
python -c "import cadquery as cq; print(f'CadQuery {cq.__version__} installed')"
```

### Step 1.3 - Verify CadQuery Installation
**Create test file:** `tests/test_basic.py`

**Test script:**
```python
import cadquery as cq

# Create a simple cylinder
cylinder = cq.Workplane("XY").cylinder(10, 5)

# Export to STEP
cq.exporters.export(cylinder, "output/test_cylinder.step")
print("✓ CadQuery working - test cylinder exported")
```

**Run test:**
```bash
python tests/test_basic.py
```

**Success criteria:**
- No import errors
- `output/test_cylinder.step` file created
- File opens in FreeCAD or other STEP viewer

---

## PHASE 2: Core Geometry Engine (2-3 hours)

### Step 2.1 - Build Hosel Component
**File:** `src/geometry/hosel.py`

**Objectives:**
- Create parametric hosel cylinder
- Add shaft bore (critical dimension)
- Validate bore diameter/depth
- Export standalone for testing

**Key parameters:**
- Height: 42mm
- Outer diameter: 14.5mm
- Bore diameter: 9.4mm (0.370")
- Bore depth: 38mm

**Test output:** `output/hosel_only.step`

**Code structure:**
```python
class WedgeHosel:
    def __init__(self, height, outer_dia, bore_dia, bore_depth):
        # Store parameters
        
    def generate_geometry(self):
        # Create outer cylinder
        # Subtract inner bore
        # Return CadQuery object
        
    def export_step(self, filename):
        # Export to STEP file
```

**Validation:**
- Bore diameter exactly 9.4mm
- Bore depth 38mm from top
- No modeling errors

### Step 2.2 - Build Basic Blade Profile
**File:** `src/geometry/blade.py`

**Objectives:**
- Create rectangular blade profile (no complex sole yet)
- Define face plane
- Set blade dimensions
- Position relative to hosel

**Key parameters:**
- Blade length: 74mm (heel to toe)
- Face height: 49mm
- Topline thickness: 3.0mm

**Test output:** `output/blade_profile.step`

**Code structure:**
```python
class WedgeBlade:
    def __init__(self, length, height, topline_thickness):
        # Store parameters
        
    def generate_profile(self):
        # Create 2D profile outline
        # Extrude to thickness
        # Return CadQuery object
```

### Step 2.3 - Add Loft and Lie Angles
**File:** `src/wedge_generator.py` (main orchestrator)

**Objectives:**
- Position blade at correct loft (56°)
- Rotate for lie angle (64°)
- Join hosel to blade
- Export combined geometry

**Key concepts:**
- Loft = angle of face relative to vertical
- Lie = angle of hosel/shaft relative to ground
- Face progression = blade position fore/aft

**Test output:** `output/basic_wedge_no_sole.step`

**Validation:**
- Loft angle measures 56° ±0.5°
- Lie angle measures 64° ±0.5°
- Hosel and blade properly joined (no gaps)

### Step 2.4 - Build Basic Sole
**File:** `src/geometry/sole.py`

**Objectives:**
- Create flat sole surface
- Apply bounce angle (8°)
- Attach to blade
- Export complete wedge with flat sole

**Key parameters:**
- Sole width: 21mm
- Bounce angle: 8°
- Sole thickness: ~8mm

**Test output:** `output/wedge_flat_sole.step`

**Code structure:**
```python
class WedgeSole:
    def __init__(self, width, bounce_angle, thickness):
        # Store parameters
        
    def generate_flat_sole(self):
        # Create rectangular sole
        # Rotate for bounce angle
        # Return CadQuery object
```

**Milestone:** At end of Phase 2, you have a basic wedge shape with correct loft/lie/bounce (no grinds yet).

---

## PHASE 3: Advanced Sole Geometry (3-4 hours)

### Step 3.1 - Leading Edge Definition
**Objectives:**
- Add subtle radius to leading edge (0.6mm)
- Ensure smooth face-to-sole transition
- Avoid sharp edge (playability issue)

**Implementation:**
- Fillet operation on leading edge
- Tangent blend between face and sole

**Test:** Visual inspection in STEP viewer (zoom in on leading edge)

### Step 3.2 - Trailing Edge Relief
**Objectives:**
- Create 2mm relief at back of sole
- Start relief 15mm from trailing edge
- Smooth curve transition

**Key insight:** Trailing edge relief prevents club from digging when hitting down on ball.

**Implementation:**
- Spline or bezier curve from full sole to relieved edge
- Blend tangently

### Step 3.3 - Heel and Toe Relief (The Grind)
**THIS IS THE ART OF WEDGE MAKING**

**Objectives:**
- Add heel camber (1.5° over 12mm)
- Add toe camber (2° over 18mm)
- Blend smoothly into center sole
- Maintain 8° bounce at center measurement point

**Why this matters:**
- Heel relief: Allows opening face without digging leading edge
- Toe relief: Enables square or closed face versatility
- Center sole: Provides stability and forgiveness

**Implementation approach:**
```python
def create_sole_relief(self, heel_relief, toe_relief, blend_distance):
    # Define sole curve from heel to toe
    # Apply variable camber across width
    # Use loft/spline for smooth transitions
    # Return modified sole surface
```

**Test output:** `output/wedge_with_grind.step`

**Validation:**
- Cross-section at heel shows 1.5° camber
- Cross-section at toe shows 2° camber
- Center still measures 8° bounce
- No discontinuities in surface

### Step 3.4 - Bounce Rocker
**Objectives:**
- Add subtle front-to-back curve (180mm radius)
- Helps club glide through turf
- Maintains center bounce angle

**Implementation:**
- Apply radius to sole in longitudinal direction
- Verify bounce angle preserved at center

**Test:** Generate cross-section views to verify curve

**Milestone:** At end of Phase 3, you have a fully-featured wedge with proper grind. This is where the club goes from "looks like a wedge" to "plays like a wedge."

---

## PHASE 4: Face Details & Grooves (2 hours)

### Step 4.1 - Groove Pattern Layout
**Objectives:**
- Calculate groove positions (3.81mm spacing)
- Ensure USGA compliance
- 11-12 grooves depending on face height
- 3mm clearance from edges

**Implementation:**
```python
def calculate_groove_positions(face_height, spacing, edge_clearance):
    # Determine number of grooves that fit
    # Calculate center positions
    # Return list of Y-coordinates
```

### Step 4.2 - Array Grooves on Face
**Objectives:**
- Create single groove geometry (0.9mm wide, 0.4mm deep, V-profile)
- Array across face
- Boolean subtract from face surface

**V-Groove profile:**
- 0.9mm wide at surface
- 0.4mm deep
- ~30° included angle (typical V-groove)

**Implementation:**
- Create triangular cross-section
- Sweep across face width
- Pattern vertically
- Subtract from face

**Test output:** `output/wedge_with_grooves.step`

**Validation:**
- Groove spacing = 3.81mm (measure in CAD)
- Groove depth = 0.4mm
- Grooves extend to within 3mm of heel/toe

### Step 4.3 - Face Texture Notes
**Objective:** Document surface finish (not modeled)

**Add to fabricator specs:**
- Ra 100-120 μin surface roughness
- Achieved through bead blasting or controlled milling
- Critical for spin generation

**Note:** Face texture is too fine to model in CAD - this is a machining specification.

---

## PHASE 5: Parametric Configuration System (1-2 hours)

### Step 5.1 - Create YAML Config Structure
**File:** `configs/vokey_56_8.yaml` ✅ ALREADY CREATED

**Validation:** Ensure all parameters from geometry code are represented in YAML.

### Step 5.2 - Build Config Parser
**File:** `src/config_loader.py`

**Objectives:**
- Load YAML file
- Validate required fields
- Provide defaults for optional fields
- Return Python dict

**Code structure:**
```python
import yaml

class WedgeConfig:
    def __init__(self, config_path):
        self.config = self.load_yaml(config_path)
        self.validate()
    
    def load_yaml(self, path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def validate(self):
        # Check required fields exist
        # Validate ranges (loft 45-64°, bounce 0-16°, etc.)
        
    def get(self, key, default=None):
        # Nested dict access helper
```

### Step 5.3 - Refactor Geometry Code
**Objectives:**
- Remove hardcoded dimensions
- Accept config dict in all geometry classes
- Test: Generate same wedge from config file

**Before:**
```python
hosel = WedgeHosel(height=42, bore_dia=9.4, ...)
```

**After:**
```python
hosel = WedgeHosel(config['hosel'])
```

**Test:**
```bash
python src/wedge_generator.py --config configs/vokey_56_8.yaml
```

**Success:** Same STEP file generated as Phase 3 hardcoded version

---

## PHASE 6: Validation & Calculation Tools (1-2 hours)

### Step 6.1 - Weight Estimation
**File:** `src/utils.py`

**Objectives:**
- Calculate volume of CadQuery solid
- Apply material density (7.85 g/cm³ for 8620 steel)
- Compare to target weight (292g)
- Flag if variance >5g

**Implementation:**
```python
def calculate_weight(cq_solid, material_density=7.85):
    """
    Calculate weight of CadQuery solid.
    
    Args:
        cq_solid: CadQuery Workplane object
        material_density: g/cm³ (default 7.85 for carbon steel)
    
    Returns:
        weight_grams: float
    """
    # Get volume in mm³
    volume_mm3 = cq_solid.val().Volume()
    
    # Convert to cm³
    volume_cm3 = volume_mm3 / 1000
    
    # Calculate weight
    weight_grams = volume_cm3 * material_density
    
    return weight_grams

def validate_weight(actual, target, tolerance=5):
    """Check if weight is within tolerance."""
    variance = abs(actual - target)
    if variance > tolerance:
        print(f"⚠️  Weight variance: {variance:.1f}g (target ±{tolerance}g)")
        return False
    else:
        print(f"✓ Weight OK: {actual:.1f}g (target {target}g ±{tolerance}g)")
        return True
```

**Output:**
```
Wedge weight: 289.3g (target: 292g ±5g)
✓ Weight within tolerance
```

### Step 6.2 - Center of Gravity Approximation
**File:** `src/utils.py`

**Objectives:**
- Estimate CG location
- Compare to target (20mm from face, 37mm from heel, 19mm from sole)
- Note: This is approximate (CadQuery can calculate true CG)

**Implementation:**
```python
def calculate_center_of_gravity(cq_solid):
    """
    Calculate center of gravity of solid.
    
    Returns:
        (x, y, z): CG coordinates in mm
    """
    # CadQuery provides this via centerOfMass()
    cg = cq_solid.val().Center()
    return (cg.x, cg.y, cg.z)
```

### Step 6.3 - Dimension Validation
**File:** `src/utils.py`

**Objectives:**
- Verify critical dimensions
- Check hosel bore diameter
- Validate loft/lie angles
- Flag potential machining issues

**Validation checks:**
- Hosel bore diameter = 9.4mm ±0.025mm
- Blade length = 74mm ±0.3mm
- Weight = 292g ±5g
- All surfaces manifold (no gaps/holes)

**Output:**
```
Validating wedge geometry...
✓ Hosel bore: 9.40mm (target: 9.40mm ±0.025mm)
✓ Blade length: 74.1mm (target: 74.0mm ±0.3mm)
✓ Weight: 289.3g (target: 292g ±5g)
✓ Geometry is valid (manifold solid)

Ready for export.
```

---

## PHASE 7: Export & Documentation (1 hour)

### Step 7.1 - STEP Export Function
**File:** `src/wedge_generator.py`

**Objectives:**
- Clean STEP export
- Meaningful filename: `vokey_56_8_2024-01-15.step`
- Include metadata/comments in STEP file

**Implementation:**
```python
def export_step(wedge_solid, config, output_dir="output/step_files"):
    """Export wedge to STEP file with metadata."""
    
    # Generate filename
    name = config['name'].replace(' ', '_').lower()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{name}_{timestamp}.step"
    filepath = os.path.join(output_dir, filename)
    
    # Export
    cq.exporters.export(wedge_solid, filepath)
    
    print(f"✓ STEP file exported: {filepath}")
    return filepath
```

### Step 7.2 - Fabricator Documentation
**File:** `docs/fabricator_specs.md` ✅ ALREADY CREATED

**Ensure document includes:**
- Material specs
- Critical tolerances
- Heat treatment requirements
- Surface finish requirements
- Inspection criteria

### Step 7.3 - Usage README
**File:** `README.md` ✅ ALREADY CREATED

**Ensure includes:**
- Installation instructions
- Basic usage example
- Configuration guide
- Troubleshooting

---

## PHASE 8: Testing & Iteration (2-3 hours)

### Step 8.1 - Generate Baseline Vokey Clone
**Test:**
```bash
python src/wedge_generator.py --config configs/vokey_56_8.yaml
```

**Validation checklist:**
1. STEP file generates without errors
2. Opens cleanly in FreeCAD/Fusion 360
3. All dimensions measure correctly
4. Weight estimation close to target
5. No gaps or non-manifold geometry
6. Grooves appear correct
7. Sole relief visible and smooth

### Step 8.2 - Test Parameter Variations
**Create additional configs:**

**High-bounce bunker wedge:**
```yaml
# configs/bunker_60_12.yaml
loft: 60
bounce: 12
sole_width_center: 24  # Wider sole
```

**Low-bounce versatile wedge:**
```yaml
# configs/versatile_54_6.yaml
loft: 54
bounce: 6
sole_width_center: 18  # Narrower sole
```

**Test all configs:**
```bash
for config in configs/*.yaml; do
    python src/wedge_generator.py --config $config
done
```

**Validation:**
- All generate successfully
- Loft/bounce angles correct for each
- Weight varies appropriately (wider sole = heavier)

### Step 8.3 - Create Alternative Grind Profiles
**Add grind presets:**

**S Grind (more heel relief):**
- Heel relief: 3° (vs. 1.5° baseline)
- Narrower sole: 19mm (vs. 21mm)
- For players who open face frequently

**K Grind (wide sole, bunker specialist):**
- Wider sole: 24mm
- Higher bounce: 12°
- Full width heel-to-toe

**Test:** Generate S and K grinds, verify sole profiles differ visually

---

## PHASE 9: Polish & Delivery (1 hour)

### Step 9.1 - Code Cleanup
**Tasks:**
- Add docstrings to all functions
- Comment complex geometry sections
- Remove debug print statements
- Run code formatter (black)
- Check for unused imports

**Quality check:**
```bash
# Format code
black src/

# Check style
flake8 src/

# Type checking (optional)
mypy src/
```

### Step 9.2 - Create Example Gallery
**Generate showcase wedges:**
1. Vokey 56/8 (baseline)
2. High-bounce 60/12
3. Low-bounce 54/6
4. Custom grind variation

**Save in:** `examples/`

**For each:**
- STEP file
- Config YAML
- Screenshot from STEP viewer
- Brief description

### Step 9.3 - Final Documentation
**Update README.md:**
- Add screenshots
- Troubleshooting section
- Known limitations
- Future enhancements

**Create CHANGELOG.md:**
- Version 1.0 features
- Known issues
- Roadmap

**Create CONTRIBUTING.md:**
- How to add new grind profiles
- Code standards
- Testing requirements

---

## Success Criteria Checklist

At completion, verify all of these:

**Functionality:**
- [ ] Generates valid STEP files
- [ ] All critical dimensions within tolerance
- [ ] Weight estimation within ±10g
- [ ] Grooves USGA-compliant
- [ ] Hosel bore correct for 0.370" shaft
- [ ] No modeling errors (gaps, non-manifold)

**Usability:**
- [ ] Can modify parameters via YAML (no code changes)
- [ ] Regenerate in <30 seconds
- [ ] Clear validation output
- [ ] Fabricator can quote from STEP file alone

**Code Quality:**
- [ ] Well-documented (docstrings, comments)
- [ ] Modular (easy to modify grind algorithms)
- [ ] No hardcoded dimensions
- [ ] Passes basic tests

**Documentation:**
- [ ] README explains installation and usage
- [ ] Fabricator specs complete
- [ ] Example configs provided
- [ ] Troubleshooting guide included

---

## Post-Launch Enhancements (Future)

Once core tool is working, consider:

1. **Additional Grind Profiles**
   - L Grind (low bounce, sweeper)
   - D Grind (full sole, digger-friendly)
   - T Grind (touring pro, minimal relief)

2. **Advanced Features**
   - STL export for 3D printing
   - Visual preview (render to PNG)
   - Swingweight calculator
   - Custom logo/stamp placement
   - Multi-wedge set generator

3. **UI Improvements**
   - Web interface (Flask/Streamlit)
   - Interactive parameter sliders
   - Real-time 3D preview
   - Preset library browser

4. **Manufacturing Integration**
   - Tool path generation for CNC
   - Cost estimation
   - Material optimization
   - Batch production support

---

## Timeline Estimate

**By Session:**
- **Session 1 (4 hours):** Phase 1-2 (setup + core geometry)
- **Session 2 (4 hours):** Phase 3 (advanced sole/grinds)
- **Session 3 (3 hours):** Phase 4-5 (grooves + config system)
- **Session 4 (3 hours):** Phase 6-7 (validation + export)
- **Session 5 (3 hours):** Phase 8-9 (testing + polish)

**Total: ~17 hours** (can compress to 3 sessions if focused)

---

## Getting Started

**Right now:**
1. Install dependencies (`pip install -r requirements.txt`)
2. Run basic test (`python tests/test_basic.py`)
3. Start Phase 2.1 (hosel geometry)

**First goal:** Generate hosel-only STEP file that you can inspect.

**End goal:** Complete parametric wedge designer generating production-ready files.

---

**Remember:** This is iterative. Build incrementally, test frequently, validate dimensions early. The grind profiles (Phase 3) are the hardest part - take your time there.

Good luck, and enjoy building your wedge designer! 🏌️
