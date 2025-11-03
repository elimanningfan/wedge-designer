"""
Main wedge generator - orchestrates geometry creation and export.
This is the entry point for generating wedge STEP files from configuration.
"""

import cadquery as cq
import os
import argparse
from datetime import datetime
from typing import Optional

from config_loader import load_config
from utils import validate_wedge_geometry


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
    
    # TODO: Implement geometry generation
    # This is where you'll orchestrate the creation of:
    # 1. Hosel (from geometry.hosel import WedgeHosel)
    # 2. Blade (from geometry.blade import WedgeBlade)
    # 3. Sole (from geometry.sole import WedgeSole)
    # 4. Grooves (face details)
    # Then combine them all together
    
    # For now, create a placeholder cylinder to test the pipeline
    print("  [Placeholder: Creating test cylinder - implement actual geometry!]")
    wedge = cq.Workplane("XY").cylinder(40, 15)
    
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
    name = name.replace(' ', '_').lower()
    
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
