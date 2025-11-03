"""
Main wedge generator - orchestrates geometry creation and export.
This is the entry point for generating wedge STEP files from configuration.
"""

import cadquery as cq
import os
import argparse
import math
from datetime import datetime
from typing import Optional

from config_loader import load_config
from utils import validate_wedge_geometry
from geometry.hosel import WedgeHosel
from geometry.blade import WedgeBlade
from geometry.sole import WedgeSole


def generate_wedge(config_path: str, output_dir: str = "output/step_files") -> str:
    """
    Generate wedge geometry from configuration and export to STEP file.
    
    Args:
        config_path: Path to YAML configuration file
        output_dir: Directory to save STEP file
    
    Returns:
        Path to generated STEP file
    """
    print(f"\nLoading configuration: {config_path}")
    config = load_config(config_path)
    
    print("\nGenerating wedge geometry...")

    # Extract configuration sections
    wedge_specs = config.get('wedge_specs', {})
    hosel_config = wedge_specs.get('hosel', {})
    sole_config = wedge_specs.get('sole', {})
    blade_length = wedge_specs.get('blade_length', 74)

    # 1. Generate hosel
    print("  Creating hosel...")
    hosel = WedgeHosel(hosel_config)
    hosel.validate()
    hosel_geometry = hosel.generate()

    # 2. Generate blade
    print("  Creating blade...")
    blade = WedgeBlade(wedge_specs)
    blade.validate()
    blade_geometry = blade.generate()

    # Add grooves to face
    if 'face' in wedge_specs and 'grooves' in wedge_specs['face']:
        print("  Adding grooves to face...")
        groove_config = wedge_specs['face']['grooves']
        blade_geometry = blade.add_grooves(blade_geometry, groove_config)

    # 3. Generate sole (with advanced grind features)
    print("  Creating sole with grind...")
    sole = WedgeSole(wedge_specs)
    sole.validate()
    sole_geometry = sole.generate_with_grind(blade_length)

    # 4. Position and combine components
    print("  Assembling components...")

    # Get key dimensions
    face_height = wedge_specs.get('face_height', 49)
    lie_angle = wedge_specs.get('lie', 64)

    # Position hosel at heel
    # The hosel should emerge from the TOP of the blade at the heel
    # After loft is applied, the top is tilted back
    heel_x = -blade_length / 2 + 8  # 8mm from heel edge

    # Hosel starts at top of blade
    # After 56° loft, the top of face is pushed back and up
    # Need to calculate where top-of-blade is after rotation
    loft_rad = math.radians(wedge_specs.get('loft', 56))
    top_offset_y = face_height * math.sin(loft_rad)  # How far back top moved
    top_offset_z = face_height * math.cos(loft_rad)  # How high top is

    hosel_positioned = hosel_geometry.translate((
        heel_x,           # At heel
        top_offset_y,     # Offset back due to loft
        top_offset_z      # At top of blade
    ))

    # Apply lie angle to hosel (tilt it toward player)
    hosel_positioned = hosel_positioned.rotate(
        (heel_x, top_offset_y, top_offset_z),  # Rotate around hosel base
        (1, 0, 0),                              # Around X axis (heel-toe)
        -(90 - lie_angle)                       # Tilt angle
    )

    # Combine all components using union
    wedge = blade_geometry.union(sole_geometry).union(hosel_positioned)
    
    # Validate geometry
    print("\nValidating geometry...")
    validation_results = validate_wedge_geometry(wedge, config.get_all())
    
    # Export to STEP
    print("\nExporting to STEP file...")
    step_path = export_step(wedge, config, output_dir)
    
    return step_path


def export_step(
    wedge_solid: cq.Workplane,
    config,
    output_dir: str = "output/step_files"
) -> str:
    """
    Export wedge geometry to STEP file with meaningful filename.
    
    Args:
        wedge_solid: CadQuery Workplane with wedge geometry
        config: WedgeConfig object
        output_dir: Directory to save file
    
    Returns:
        Path to exported STEP file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    name = config.get('wedge_specs.name', 'wedge')
    # Sanitize filename: replace spaces and slashes
    name = name.replace(' ', '_').replace('/', '-').lower()

    loft = config.get('wedge_specs.loft', '')
    bounce = config.get('wedge_specs.bounce', '')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    filename = f"{name}_{loft}_{bounce}_{timestamp}.step"
    filepath = os.path.join(output_dir, filename)
    
    # Export to STEP format
    cq.exporters.export(wedge_solid, filepath)
    
    file_size = os.path.getsize(filepath)
    print(f"✓ STEP file exported: {filepath}")
    print(f"  File size: {file_size:,} bytes")
    
    return filepath


def main():
    """Main entry point with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description='Generate custom golf wedge STEP files from YAML configuration'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to YAML configuration file (e.g., configs/vokey_56_8.yaml)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='output/step_files',
        help='Output directory for STEP files (default: output/step_files)'
    )
    
    args = parser.parse_args()
    
    # Generate wedge
    print("="*60)
    print("PARAMETRIC WEDGE GENERATOR")
    print("="*60)
    
    try:
        step_path = generate_wedge(args.config, args.output)
        
        print("\n" + "="*60)
        print("✓ SUCCESS!")
        print("="*60)
        print(f"\nYour wedge STEP file is ready:")
        print(f"  {step_path}")
        print(f"\nNext steps:")
        print(f"  1. Open in FreeCAD or Fusion 360 to inspect")
        print(f"  2. Verify dimensions and geometry")
        print(f"  3. Send to fabricator with docs/fabricator_specs.md")
        print()
        
    except Exception as e:
        print("\n" + "="*60)
        print("✗ ERROR")
        print("="*60)
        print(f"\n{str(e)}")
        print()
        raise


if __name__ == "__main__":
    main()
