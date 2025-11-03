"""
Sole geometry generation for golf wedge.
The sole is where the art of wedge design lives - bounce, grinds, and relief.
"""

import cadquery as cq
from typing import Dict
import math


class WedgeSole:
    """
    Generates the sole geometry for a golf wedge.
    
    The sole includes:
    - Bounce angle (main characteristic)
    - Leading edge treatment
    - Trailing edge relief
    - Heel/toe relief (the "grind")
    - Bounce rocker (front-to-back curve)
    """
    
    def __init__(self, config: Dict):
        """
        Initialize sole with configuration parameters.
        
        Args:
            config: Dictionary with sole specifications from config['sole']:
                - width_center: Sole width at center (mm)
                - leading_edge_radius: Subtle radius on leading edge (mm)
                - trailing_edge_relief: Height of relief at back (mm)
                - heel_relief_angle: Additional camber at heel (degrees)
                - toe_relief_angle: Additional camber at toe (degrees)
                - bounce_rocker_radius: Front-to-back curve radius (mm)
        
        Plus from main config:
                - bounce: Main bounce angle (degrees)
        """
        sole_config = config.get('sole', {})
        
        self.width_center = sole_config.get('width_center', 21)
        self.leading_edge_radius = sole_config.get('leading_edge_radius', 0.6)
        self.trailing_edge_relief = sole_config.get('trailing_edge_relief', 2.0)
        self.trailing_edge_start = sole_config.get('trailing_edge_start', 15)
        
        self.heel_relief_start = sole_config.get('heel_relief_start', 12)
        self.heel_relief_angle = sole_config.get('heel_relief_angle', 1.5)
        self.toe_relief_start = sole_config.get('toe_relief_start', 18)
        self.toe_relief_angle = sole_config.get('toe_relief_angle', 2.0)
        
        self.bounce_rocker_radius = sole_config.get('bounce_rocker_radius', 180)
        self.sole_camber_radius = sole_config.get('sole_camber_radius', 200)
        
        # Main bounce angle from top-level config
        self.bounce = config.get('bounce', 8)
    
    def generate_flat_sole(self, blade_length: float) -> cq.Workplane:
        """
        Generate a sole that extends from blade bottom.
        Creates a thin sole extension with bounce angle.

        Args:
            blade_length: Length of blade (heel to toe) in mm

        Returns:
            CadQuery Workplane with flat sole geometry
        """
        # Sole is a thin bottom extension
        # Should blend with blade, not be a separate thick chunk
        sole_thickness = 3  # mm (much thinner!)

        # Create sole profile - narrow and follows bounce angle
        sole = (
            cq.Workplane("XY")
            .box(blade_length, self.width_center, sole_thickness)
        )

        # Position below the blade (z=0 is blade bottom)
        sole = sole.translate((0, 0, -sole_thickness / 2))

        # Apply bounce angle around leading edge
        # This tilts the sole/trailing edge up
        sole = sole.rotate((0, -self.width_center / 2, 0), (1, 0, 0), self.bounce)

        return sole
    
    def generate_with_grind(self, blade_length: float) -> cq.Workplane:
        """
        Generate sole with full grind profile (heel/toe relief, rockers).
        This is Phase 3 - the advanced sole geometry.

        Args:
            blade_length: Length of blade (heel to toe) in mm

        Returns:
            CadQuery Workplane with ground sole geometry

        Process:
            1. Start with flat sole at bounce angle
            2. Add leading edge radius
            3. Add trailing edge relief
            4. Add heel relief (camber)
            5. Add toe relief (camber)
            6. Add bounce rocker (front-to-back curve)
        """
        # Start with the flat sole
        sole = self.generate_flat_sole(blade_length)

        # Add leading edge radius for smooth transition
        sole = self.add_leading_edge_radius(sole)

        # Add heel and toe relief (grind)
        sole = self.add_heel_toe_relief(sole, blade_length)

        # Note: Trailing edge relief and bounce rocker are advanced features
        # that would require more complex surface modeling. For now, we have
        # a functional ground sole with heel/toe relief which is the most
        # important feature for playability.

        return sole
    
    def add_leading_edge_radius(self, sole: cq.Workplane) -> cq.Workplane:
        """
        Add subtle radius to leading edge.

        Args:
            sole: Existing sole geometry

        Returns:
            Sole with leading edge radius applied
        """
        # Apply fillet to leading edge
        # Select front edges and round them
        try:
            # This adds a small radius to soften the leading edge
            sole = sole.edges("<Y").fillet(self.leading_edge_radius)
        except:
            # If fillet fails (edge selection issues), skip it
            # Better to have a working wedge than fail on cosmetic detail
            pass

        return sole
    
    def add_heel_toe_relief(self, sole: cq.Workplane, blade_length: float) -> cq.Workplane:
        """
        Add heel and toe relief (the grind).
        This is what makes the wedge versatile.

        Args:
            sole: Existing sole geometry
            blade_length: Length of blade

        Returns:
            Sole with relief applied
        """
        # Create relief by chamfering the heel and toe edges
        # This simulates grinding away material at the extremes

        try:
            # Select edges at heel (negative X) and toe (positive X)
            # and chamfer them to create relief
            # The chamfer size is based on the relief angles
            heel_chamfer = self.heel_relief_angle * 0.5  # Convert angle to distance
            toe_chamfer = self.toe_relief_angle * 0.5

            # Chamfer heel edges (left side)
            sole = sole.faces("<X").edges("|Z").chamfer(heel_chamfer)

            # Chamfer toe edges (right side)
            sole = sole.faces(">X").edges("|Z").chamfer(toe_chamfer)

        except Exception as e:
            # If chamfer fails, skip it - better to have a working wedge
            # Edge selection can be tricky after previous operations
            print(f"  Note: Could not apply full heel/toe relief: {str(e)}")
            pass

        return sole
    
    def validate(self) -> bool:
        """
        Validate sole parameters.
        
        Returns:
            True if valid, raises ValueError if invalid
        """
        # Check bounce is reasonable
        if not (0 <= self.bounce <= 16):
            raise ValueError(
                f"Bounce should be between 0-16° for wedges, got {self.bounce}°"
            )
        
        # Check sole width is reasonable
        if not (15 <= self.width_center <= 30):
            raise ValueError(
                f"Sole width should be between 15-30mm, got {self.width_center}mm"
            )
        
        return True


def calculate_effective_bounce(
    base_bounce: float,
    relief_angle: float,
    position: str = "center"
) -> float:
    """
    Calculate effective bounce at different positions on sole.
    
    Args:
        base_bounce: Base bounce angle at center (degrees)
        relief_angle: Additional camber from grind (degrees)
        position: "heel", "center", or "toe"
    
    Returns:
        Effective bounce angle at that position
    
    Example:
        Center: 8° bounce, 0° relief = 8° effective
        Heel: 8° bounce, 1.5° relief = 9.5° effective
        Toe: 8° bounce, 2° relief = 10° effective
    """
    if position == "center":
        return base_bounce
    else:
        return base_bounce + relief_angle


if __name__ == "__main__":
    import os

    # Test sole generation
    test_config = {
        'bounce': 8,
        'sole': {
            'width_center': 21,
            'leading_edge_radius': 0.6,
            'trailing_edge_relief': 2.0,
            'heel_relief_angle': 1.5,
            'toe_relief_angle': 2.0,
            'bounce_rocker_radius': 180
        }
    }

    sole = WedgeSole(test_config)
    sole.validate()

    print("Sole configuration:")
    print(f"  Bounce: {sole.bounce}°")
    print(f"  Width: {sole.width_center}mm")
    print(f"  Heel relief: {sole.heel_relief_angle}°")
    print(f"  Toe relief: {sole.toe_relief_angle}°")

    print("\nEffective bounce angles:")
    print(f"  Heel: {calculate_effective_bounce(sole.bounce, sole.heel_relief_angle, 'heel'):.1f}°")
    print(f"  Center: {calculate_effective_bounce(sole.bounce, 0, 'center'):.1f}°")
    print(f"  Toe: {calculate_effective_bounce(sole.bounce, sole.toe_relief_angle, 'toe'):.1f}°")

    # Generate and export flat sole
    print("\nGenerating flat sole geometry...")
    blade_length = 74  # Test with standard blade length
    sole_geometry = sole.generate_flat_sole(blade_length)

    # Ensure output directory exists
    os.makedirs("output/step_files", exist_ok=True)

    output_path = "output/step_files/sole_test.step"
    cq.exporters.export(sole_geometry, output_path)

    file_size = os.path.getsize(output_path)
    print(f"\n✓ Sole exported to {output_path}")
    print(f"  File size: {file_size:,} bytes")
