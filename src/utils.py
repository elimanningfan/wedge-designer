"""
Utility functions for wedge design calculations and validations.
Includes weight estimation, center of gravity, and dimension validation.
"""

import cadquery as cq
from typing import Tuple, Dict


# Material densities (g/cm³)
MATERIAL_DENSITIES = {
    '8620_steel': 7.85,
    '1020_steel': 7.87,
    '304_stainless': 8.00,
    '431_stainless': 7.75,
    'carbon_steel': 7.85,  # Generic carbon steel
}


def calculate_weight(cq_solid: cq.Workplane, material: str = '8620_steel') -> float:
    """
    Calculate weight of CadQuery solid based on material density.
    
    Args:
        cq_solid: CadQuery Workplane containing solid geometry
        material: Material type (key from MATERIAL_DENSITIES)
    
    Returns:
        Weight in grams
    
    Example:
        wedge = create_wedge()
        weight = calculate_weight(wedge, '8620_steel')
        print(f"Wedge weight: {weight:.1f}g")
    """
    # Get volume in mm³ from CadQuery solid
    volume_mm3 = cq_solid.val().Volume()
    
    # Convert mm³ to cm³
    volume_cm3 = volume_mm3 / 1000.0
    
    # Get material density
    density = MATERIAL_DENSITIES.get(material, 7.85)
    
    # Calculate weight
    weight_grams = volume_cm3 * density
    
    return weight_grams


def validate_weight(actual: float, target: float, tolerance: float = 5.0) -> bool:
    """
    Validate that actual weight is within tolerance of target.
    
    Args:
        actual: Actual calculated weight (grams)
        target: Target weight (grams)
        tolerance: Acceptable variance (grams)
    
    Returns:
        True if within tolerance, False otherwise
    """
    variance = abs(actual - target)
    
    if variance <= tolerance:
        print(f"✓ Weight OK: {actual:.1f}g (target: {target}g ±{tolerance}g)")
        return True
    else:
        print(f"⚠️  Weight variance: {variance:.1f}g exceeds tolerance of ±{tolerance}g")
        print(f"   Actual: {actual:.1f}g, Target: {target}g")
        return False


def calculate_center_of_gravity(cq_solid: cq.Workplane) -> Tuple[float, float, float]:
    """
    Calculate center of gravity (centroid) of solid.

    Args:
        cq_solid: CadQuery Workplane containing solid geometry

    Returns:
        (x, y, z) coordinates of center of gravity in mm

    Note:
        CadQuery provides geometric centroid. For true CG with
        variable density, more complex calculation needed.
    """
    # Get the shape from the workplane
    shape = cq_solid.val()

    # Get center of mass - works for both Solid and Compound
    try:
        cg = shape.CenterOfMass()
    except AttributeError:
        # If CenterOfMass doesn't exist, try Center() as fallback
        cg = shape.Center()

    return (cg.x, cg.y, cg.z)


def validate_center_of_gravity(
    actual_cg: Tuple[float, float, float],
    target_cg: Tuple[float, float, float],
    tolerance: float = 2.0
) -> bool:
    """
    Validate that actual CG is within tolerance of target.
    
    Args:
        actual_cg: (x, y, z) actual center of gravity
        target_cg: (x, y, z) target center of gravity
        tolerance: Acceptable variance in mm
    
    Returns:
        True if all dimensions within tolerance
    """
    labels = ['X (from face)', 'Y (from heel)', 'Z (from sole)']
    all_ok = True
    
    for i, label in enumerate(labels):
        variance = abs(actual_cg[i] - target_cg[i])
        if variance <= tolerance:
            print(f"✓ CG {label}: {actual_cg[i]:.1f}mm (target: {target_cg[i]:.1f}mm)")
        else:
            print(f"⚠️  CG {label}: {variance:.1f}mm variance (tolerance: ±{tolerance}mm)")
            all_ok = False
    
    return all_ok


def validate_dimension(
    name: str,
    actual: float,
    target: float,
    tolerance: float,
    unit: str = "mm"
) -> bool:
    """
    Generic dimension validation with output.
    
    Args:
        name: Dimension name for display
        actual: Measured/calculated value
        target: Target value
        tolerance: Acceptable variance
        unit: Unit of measurement
    
    Returns:
        True if within tolerance
    """
    variance = abs(actual - target)
    
    if variance <= tolerance:
        print(f"✓ {name}: {actual:.2f}{unit} (target: {target:.2f}{unit} ±{tolerance:.2f}{unit})")
        return True
    else:
        print(f"⚠️  {name}: {variance:.2f}{unit} variance exceeds tolerance")
        print(f"   Actual: {actual:.2f}{unit}, Target: {target:.2f}{unit}")
        return False


def validate_wedge_geometry(wedge_solid: cq.Workplane, config: Dict) -> Dict[str, bool]:
    """
    Run complete validation suite on wedge geometry.
    
    Args:
        wedge_solid: CadQuery Workplane with wedge geometry
        config: Configuration dictionary with target values
    
    Returns:
        Dictionary of validation results
    """
    print("\n" + "="*60)
    print("WEDGE GEOMETRY VALIDATION")
    print("="*60 + "\n")
    
    results = {}
    
    # Weight validation
    print("Weight Analysis:")
    target_weight = config.get('wedge_specs', {}).get('weight', {}).get('target_head_weight', 292)
    material = config.get('wedge_specs', {}).get('material', {}).get('type', '8620_steel')
    actual_weight = calculate_weight(wedge_solid, material.replace(' ', '_'))
    results['weight'] = validate_weight(actual_weight, target_weight)
    
    print()
    
    # Center of gravity
    print("Center of Gravity:")
    cg_target = config.get('wedge_specs', {}).get('weight', {}).get('center_of_gravity', {})
    target_cg = (
        cg_target.get('from_face', 20),
        cg_target.get('from_heel', 37),
        cg_target.get('from_sole', 19)
    )
    actual_cg = calculate_center_of_gravity(wedge_solid)
    results['cg'] = validate_center_of_gravity(actual_cg, target_cg)
    
    print()
    
    # TODO: Add more validations:
    # - Hosel bore diameter (critical!)
    # - Blade length
    # - Face height
    # - Loft/lie angles (requires measurement technique)
    
    # Check if geometry is valid (manifold)
    print("Geometry Check:")
    is_valid = wedge_solid.val().isValid()
    if is_valid:
        print("✓ Geometry is valid (manifold solid)")
        results['geometry'] = True
    else:
        print("✗ Geometry has errors (non-manifold)")
        results['geometry'] = False
    
    print("\n" + "="*60)
    if all(results.values()):
        print("✓ ALL VALIDATIONS PASSED")
    else:
        print("⚠️  SOME VALIDATIONS FAILED")
    print("="*60 + "\n")
    
    return results


# Helper function for converting degrees to radians
def deg_to_rad(degrees: float) -> float:
    """Convert degrees to radians."""
    import math
    return degrees * math.pi / 180.0


def rad_to_deg(radians: float) -> float:
    """Convert radians to degrees."""
    import math
    return radians * 180.0 / math.pi


if __name__ == "__main__":
    # Example usage
    print("Wedge Design Utilities")
    print("="*60)
    
    # Test material density lookup
    print("\nAvailable materials:")
    for material, density in MATERIAL_DENSITIES.items():
        print(f"  {material}: {density} g/cm³")
    
    # Example volume calculation
    print("\nExample: 50cm³ wedge head in 8620 steel")
    volume_cm3 = 50
    density = MATERIAL_DENSITIES['8620_steel']
    weight = volume_cm3 * density
    print(f"  Weight: {weight:.1f}g")
