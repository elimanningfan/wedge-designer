"""
Basic test to verify CadQuery installation and STEP export functionality.
Run this first to ensure environment is set up correctly.
"""

import cadquery as cq
import os

def test_cadquery_installation():
    """Test that CadQuery is installed and working."""
    print("Testing CadQuery installation...")
    print(f"CadQuery version: {cq.__version__}")
    
    # Create a simple test cylinder
    print("\nCreating test cylinder...")
    cylinder = cq.Workplane("XY").cylinder(10, 5)
    
    # Ensure output directory exists
    os.makedirs("output/step_files", exist_ok=True)
    
    # Export to STEP
    output_path = "output/step_files/test_cylinder.step"
    print(f"Exporting to: {output_path}")
    cq.exporters.export(cylinder, output_path)
    
    # Verify file was created
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"✓ Success! Test cylinder exported ({file_size} bytes)")
        print(f"\nYou can open '{output_path}' in FreeCAD or any STEP viewer to verify.")
        return True
    else:
        print("✗ Failed: STEP file was not created")
        return False

if __name__ == "__main__":
    success = test_cadquery_installation()
    
    if success:
        print("\n" + "="*60)
        print("CadQuery is properly installed and working!")
        print("You're ready to start building the wedge generator.")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("Installation test failed. Please check your environment.")
        print("="*60)
