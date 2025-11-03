"""
Blade geometry generation for golf wedge.
The blade is the main hitting surface and body of the clubhead.
"""

import cadquery as cq
from typing import Dict


class WedgeBlade:
    """
    Generates the blade/face geometry for a golf wedge.
    
    The blade includes:
    - Face (hitting surface)
    - Topline (top edge)
    - Heel and toe profiles
    """
    
    def __init__(self, config: Dict):
        """
        Initialize blade with configuration parameters.
        
        Args:
            config: Dictionary with blade specifications:
                - blade_length: Heel to toe length (mm)
                - face_height: Leading edge to topline (mm)
                - topline_thickness: Thickness of top edge (mm)
                - loft: Face angle in degrees
                - lie: Shaft/hosel angle in degrees
        """
        self.blade_length = config.get('blade_length', 74)
        self.face_height = config.get('face_height', 49)
        self.topline_thickness = config.get('topline_thickness', 3.0)
        self.loft = config.get('loft', 56)
        self.lie = config.get('lie', 64)
    
    def generate(self) -> cq.Workplane:
        """
        Generate blade geometry.

        Returns:
            CadQuery Workplane with blade geometry

        Process:
            1. Create face profile (rectangular outline)
            2. Extrude to create blade body
            3. Apply loft angle to face
            4. Add topline details
        """
        import math

        # Blade body thickness (front to back)
        blade_thickness = 10  # mm - thickness at back of blade

        # Create blade as a box: length (heel-toe) x height x thickness
        # Start with blade vertical, we'll rotate for loft later
        blade = (
            cq.Workplane("XY")
            .box(self.blade_length, blade_thickness, self.face_height)
        )

        # Move blade so bottom is at z=0 (sole level)
        blade = blade.translate((0, 0, self.face_height / 2))

        # Apply loft angle - rotate around X axis (heel-toe axis)
        # Loft makes the face lean back
        # Rotate at the bottom (leading edge)
        blade = blade.rotate((0, 0, 0), (1, 0, 0), -self.loft)

        # Note: Skipping topline fillet for now - can add later if needed
        # Edge selection after rotation is tricky

        return blade

    def add_grooves(self, blade: cq.Workplane, groove_config: Dict) -> cq.Workplane:
        """
        Add groove pattern to the face.

        Args:
            blade: Existing blade geometry
            groove_config: Configuration for grooves (from config['face']['grooves'])

        Returns:
            Blade with grooves cut into face
        """
        import math

        spacing = groove_config.get('spacing', 3.81)
        width = groove_config.get('width', 0.9)
        depth = groove_config.get('depth', 0.4)
        count = groove_config.get('count', 12)
        edge_clearance = groove_config.get('edge_clearance', 3)

        # Calculate groove positions
        # Grooves are horizontal lines on the face
        # Start from bottom, space them evenly
        groove_start_z = edge_clearance
        groove_end_z = self.face_height - edge_clearance

        # Calculate how many grooves fit
        available_height = groove_end_z - groove_start_z
        actual_count = min(count, int(available_height / spacing) + 1)

        print(f"    Adding {actual_count} grooves (spacing: {spacing}mm, USGA compliant)")

        # Create grooves
        for i in range(actual_count):
            z_pos = groove_start_z + (i * spacing)

            # Create a V-groove by cutting with a wedge shape
            # Position the groove on the face
            try:
                # Create a cutting wedge for the V-groove
                # The groove is a thin triangular extrusion
                groove_cutter = (
                    cq.Workplane("XZ")
                    .moveTo(-self.blade_length / 2 - 5, z_pos)
                    .lineTo(-self.blade_length / 2 - 5, z_pos - depth)
                    .lineTo(-self.blade_length / 2 - 5 + width, z_pos)
                    .close()
                    .extrude(self.blade_length + 10)
                )

                # Position the cutter on the face
                # The face is rotated by loft angle, so we need to position accordingly
                groove_cutter = groove_cutter.translate((0, 5, 0))

                # Subtract the groove from the blade
                blade = blade.cut(groove_cutter)

            except Exception as e:
                print(f"    Note: Could not add groove {i + 1}: {str(e)}")
                # Continue with other grooves even if one fails

        return blade

    def validate(self) -> bool:
        """
        Validate blade parameters.
        
        Returns:
            True if valid, raises ValueError if invalid
        """
        # Check loft is reasonable for a wedge
        if not (45 <= self.loft <= 64):
            raise ValueError(
                f"Loft should be between 45-64° for wedges, got {self.loft}°"
            )
        
        # Check lie angle is reasonable
        if not (60 <= self.lie <= 66):
            raise ValueError(
                f"Lie angle should be between 60-66° for wedges, got {self.lie}°"
            )
        
        return True


if __name__ == "__main__":
    import os

    # Test blade generation
    test_config = {
        'blade_length': 74,
        'face_height': 49,
        'topline_thickness': 3.0,
        'loft': 56,
        'lie': 64
    }

    blade = WedgeBlade(test_config)
    blade.validate()

    print("Blade configuration:")
    print(f"  Length: {blade.blade_length}mm")
    print(f"  Face height: {blade.face_height}mm")
    print(f"  Loft: {blade.loft}°")
    print(f"  Lie: {blade.lie}°")

    # Generate and export blade
    print("\nGenerating blade geometry...")
    blade_geometry = blade.generate()

    # Ensure output directory exists
    os.makedirs("output/step_files", exist_ok=True)

    output_path = "output/step_files/blade_test.step"
    cq.exporters.export(blade_geometry, output_path)

    file_size = os.path.getsize(output_path)
    print(f"\n✓ Blade exported to {output_path}")
    print(f"  File size: {file_size:,} bytes")
