# Fabricator Specifications for Custom Golf Wedge

**Project:** Custom Golf Wedge Head Machining  
**Material:** 8620 Carbon Steel  
**Quantity:** 1 (prototype / can discuss production runs)  
**Delivery Format:** STEP file provided

---

## Material Requirements

### Primary Material
- **Steel Grade:** 8620 Carbon Steel (low-alloy steel)
- **Properties:** Good machinability, case-hardenable, excellent for golf clubs
- **Alternatives:** 1020/1025 carbon steel acceptable if 8620 unavailable
- **Stock Form:** Bar stock or billet sufficient for 75mm x 50mm x 45mm envelope

### Material Specifications
- **Density:** 7.85 g/cm³
- **Initial Hardness:** As-rolled (~150 HB / 15-20 HRC)
- **Machined Surface Finish:** Ra 63 μin (1.6 μm) or better
- **No porosity or inclusions** in final part

---

## Critical Dimensions & Tolerances

### Hosel Bore (MOST CRITICAL)
This is the most important dimension - it must be exact for proper shaft installation.

- **Bore Diameter:** 9.4mm (0.370") ±0.025mm (±0.001")
- **Bore Depth:** 38mm ±0.5mm
- **Bore Straightness:** 0.1mm maximum deviation over depth
- **Surface Finish:** Ra 32 μin (0.8 μm) or better
- **Notes:** Standard golf shaft is 0.370" tip diameter. Too tight = shaft won't insert. Too loose = poor bond and potential failure.

### Loft & Lie Angles
- **Loft Angle:** 56° ±0.5°
- **Lie Angle:** 64° ±0.5°
- **Measurement Method:** Use digital angle gauge or CMM relative to bore centerline

### Overall Dimensions
- **Blade Length (heel-to-toe):** 74mm ±0.3mm
- **Face Height:** 49mm ±0.3mm
- **Sole Width (center):** 21mm ±0.3mm
- **Head Weight:** 292g ±5g (before heat treatment)

### Bounce Angle
- **Specified Bounce:** 8° ±0.5°
- **Measurement Point:** Center of sole, with face lying flat
- **Notes:** Bounce is the angle between leading edge and trailing edge when face is flush to surface

---

## Machining Notes

### Setup & Fixturing
- Recommend 5-axis CNC or multi-operation setup
- Hosel bore should be drilled/reamed in same setup as face for accuracy
- Use soft jaws or custom fixture to avoid marring finished surfaces

### Surface Finish Requirements

**Face (hitting area):**
- **Texture:** Ra 100-120 μin (2.5-3.0 μm) - slightly textured for spin
- **Method:** Can achieve with bead blasting, hand sanding, or controlled mill finish
- **Notes:** Do NOT polish face smooth - texture is critical for spin generation

**Sole:**
- **Finish:** Ra 63 μin (1.6 μm) or better
- **Appearance:** Smooth, consistent finish
- **Method:** Mill, grind, or sand to smooth finish

**Hosel:**
- **Exterior:** Ra 63 μin (1.6 μm) - smooth finish
- **Interior bore:** Ra 32 μin (0.8 μm) - reamed or precision bored

### Grooves (If included in STEP model)
- **Width:** 0.9mm ±0.05mm
- **Depth:** 0.4mm ±0.05mm
- **Spacing:** 3.81mm (USGA maximum - cannot exceed)
- **Edge Condition:** Sharp V-groove edges preferred for spin
- **Notes:** Grooves should be milled, not stamped, for consistency

### Edge Conditions
- **Leading Edge:** 0.6mm radius - subtle, not sharp
- **Topline:** 3mm thickness, slight chamfer/radius
- **Heel/Toe:** Smooth transitions, no sharp edges
- **All external edges:** 0.2-0.5mm break/chamfer for safety and appearance

---

## Post-Machining Requirements

### Heat Treatment (REQUIRED)

**Face Area Heat Treatment:**
- **Process:** Case hardening or carburizing
- **Target Hardness:** 50-52 HRC (Rockwell C scale) on face surface
- **Depth:** 0.5-1.0mm case depth
- **Purpose:** Durability and spin performance

**Body/Hosel:**
- **Target Hardness:** 30-35 HRC (softer for feel and forgiveness)
- **Notes:** Can selectively harden face or through-harden and temper body

**Heat Treatment Process Recommendations:**
1. Machine to final dimensions
2. Case harden face (gas carburizing or similar)
3. Quench and temper
4. Verify hardness with Rockwell tester
5. Final surface finishing if needed

### Post-Heat Treatment
- Light bead blasting or tumbling to remove scale
- Verify no warpage occurred (check loft/lie angles)
- Re-check hosel bore (should not distort if done properly)

---

## Inspection Requirements

### Dimensional Inspection
- Verify hosel bore diameter with pin gauges or CMM
- Check loft/lie angles with digital gauge
- Confirm weight on precision scale (±0.1g resolution)
- Measure sole width at heel/center/toe

### Visual Inspection
- No cracks, voids, or porosity
- Smooth transitions in sole relief areas
- Consistent groove depth and spacing
- Clean bore interior (no burrs or chips)

### Functional Checks
- Test-fit with 0.370" golf shaft (should slide in smoothly but snugly)
- Verify face texture appears consistent
- Check for any sharp edges that need deburring

---

## Quantity & Timing

### Initial Order
- **Quantity:** 1 prototype
- **Lead Time:** [Your timeline - suggest 2-4 weeks for first piece]
- **Purpose:** Validation of design and manufacturing process

### Potential Follow-Up
- Additional units if prototype validates successfully
- Possible variations in loft/bounce for testing
- Open to discussing production runs (5-10+ units)

---

## Delivery Requirements

### Packaging
- Protect finished surfaces (wrap in foam/bubble wrap)
- Prevent bore contamination (cap or plug bore opening)
- Include hardness test report if heat treatment performed

### Documentation Requested
- Material certification (mill cert for 8620 steel)
- Dimensional inspection report (key dimensions)
- Hardness test results (face and body)
- Any notes on deviations or challenges encountered

---

## File Format & CAD Support

### Provided Files
- **STEP file (.step or .stp):** Primary manufacturing file
- **Configuration YAML:** Reference dimensions and specifications (for your records)
- **This specification document:** Manufacturing requirements

### CAD File Notes
- STEP file contains complete 3D geometry
- All dimensions are in millimeters
- Origin/datum: [Specify coordinate system if relevant]
- Model is final machined geometry (no stock allowances needed)

### Questions or Clarifications
If any features are unclear or seem un-manufacturable, please contact before starting:
- [Your contact information]
- Willing to modify design if needed for manufacturability

---

## Cost Estimate Request

Please provide quote including:
1. **Machining cost** (setup + runtime)
2. **Material cost** (8620 carbon steel)
3. **Heat treatment cost** (if outsourcing)
4. **Finishing cost** (bead blast, etc.)
5. **Inspection/certification** (if applicable)
6. **Lead time** from order to delivery

---

## Design Intent & Context

This is a custom golf wedge head based on proven Titleist Vokey design principles:
- **Loft:** 56° (sand wedge territory)
- **Bounce:** 8° (versatile, neutral grind)
- **Purpose:** Full-swing shots, bunkers, pitches, chips

The sole relief (camber at heel/toe) is what makes the wedge workable from various lies. The 8620 carbon steel provides soft feel and allows for heat treatment to optimize durability and spin.

### Why These Specs Matter
- **Hosel bore:** Must fit standard 0.370" golf shaft
- **Weight:** Affects swingweight and feel (292g is standard for wedges)
- **Loft/Lie:** Determines launch angle and shaft plane
- **Bounce:** Prevents digging, enables versatility
- **Face texture:** Generates backspin on shots

This is a functional golf club, not just a display piece - precision matters for performance.

---

## Alternative Approaches (If Any Issues)

### If 8620 Steel Unavailable:
- 1020/1025 carbon steel acceptable
- 304/316 stainless possible (different feel, no heat treatment needed)
- Contact for approval before substituting

### If Heat Treatment Not Available:
- Can ship machined head elsewhere for heat treatment
- Can accept without heat treatment if for testing only
- Affects durability but not dimensions

### If Tolerances Too Tight:
- Hosel bore is non-negotiable (must be ±0.001")
- Other dimensions have some flexibility - contact to discuss

---

## Final Notes

This is a precision part but not aerospace-level tolerances. Any competent machine shop with 3-axis or better CNC capability should be able to produce this. The STEP file contains all geometry - no additional drawings should be needed.

**Key Success Factors:**
1. Accurate hosel bore (0.370" / 9.4mm)
2. Proper heat treatment of face
3. Target weight achieved (292g ±5g)
4. Smooth, consistent surface finishes

Thank you for your time and quote. Looking forward to working with you on this project.

---

**Document Version:** 1.0  
**Last Updated:** [Date will be auto-generated]  
**Contact:** [Your information]
