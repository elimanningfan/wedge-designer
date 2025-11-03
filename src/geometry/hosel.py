"""
Hosel geometry generation for golf wedge.
The hosel is the cylinder that connects the clubhead to the shaft.
"""

import cadquery as cq
from typing import Dict


class WedgeHosel:
    """
    Generates the hosel geometry for a golf wedge.
    
    The hosel is critical - the bore must be exactly 0.370" (9.4mm)
    for standard golf shafts to fit properly.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize hosel with configuration parameters.
        
        Args:
            config: Dictionary with hosel specifications:
                - height: Overall hosel height (mm)
                - outer_diameter: External diameter (mm)
                - bore_diameter: Internal bore diameter (mm) - CRITICAL!
                - bore_depth: How deep shaft inserts (mm)
        """
        self.height = config.get('height', 42)
        self.outer_diameter = config.get('outer_diameter', 14.5)
        self.bore_diameter = config.get('bore_diameter', 9.4)
        self.bore_depth = config.get('bore_depth', 38)
    
    def generate(self) -> cq.Workplane:
        """
        Generate hosel geometry.

        Returns:
            CadQuery Workplane with hosel geometry

        Process:
            1. Create outer cylinder
            2. Create inner bore cylinder
            3. Subtract bore from outer cylinder
        """
        # Create outer cylinder (hosel body)
        # Start at origin, build along Z axis
        hosel = (
            cq.Workplane("XY")
            .cylinder(self.height, self.outer_diameter / 2)
        )

        # Create inner bore (shaft hole)
        # Build from top down to bore_depth
        bore = (
            cq.Workplane("XY")
            .workplane(offset=self.height / 2)  # Start at top of hosel
            .cylinder(self.bore_depth, self.bore_diameter / 2)
        )

        # Subtract bore from hosel
        hosel = hosel.cut(bore)

        return hosel
    
    def validate(self) -> bool:
        """
        Validate hosel parameters are within acceptable ranges.
        
        Returns:
            True if valid, raises ValueError if invalid
        """
        # Check bore diameter is standard shaft size
        if abs(self.bore_diameter - 9.4) > 0.1:
            raise ValueError(
                f"Bore diameter should be 9.4mm for standard shaft, got {self.bore_diameter}mm"
            )
        
        # Check bore depth doesn't exceed hosel height
        if self.bore_depth >= self.height:
            raise ValueError(
                f"Bore depth ({self.bore_depth}mm) must be less than hosel height ({self.height}mm)"
            )
        
        # Check outer diameter is reasonable
        if self.outer_diameter < self.bore_diameter + 3:
            raise ValueError(
                f"Outer diameter too small - need at least 3mm wall thickness"
            )
        
        return True


if __name__ == "__main__":
    import os

    # Test hosel generation
    test_config = {
        'height': 42,
        'outer_diameter': 14.5,
        'bore_diameter': 9.4,
        'bore_depth': 38
    }

    hosel = WedgeHosel(test_config)
    hosel.validate()

    print("Hosel configuration:")
    print(f"  Height: {hosel.height}mm")
    print(f"  Outer diameter: {hosel.outer_diameter}mm")
    print(f"  Bore diameter: {hosel.bore_diameter}mm (0.370\")")
    print(f"  Bore depth: {hosel.bore_depth}mm")

    # Generate and export hosel
    print("\nGenerating hosel geometry...")
    hosel_geometry = hosel.generate()

    # Ensure output directory exists
    os.makedirs("output/step_files", exist_ok=True)

    output_path = "output/step_files/hosel_test.step"
    cq.exporters.export(hosel_geometry, output_path)

    file_size = os.path.getsize(output_path)
    print(f"\n✓ Hosel exported to {output_path}")
    print(f"  File size: {file_size:,} bytes")
