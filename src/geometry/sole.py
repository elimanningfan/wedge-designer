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
        Generate a basic flat sole with bounce angle.
        This is Phase 2.4 - simple sole before adding grinds.
        
        Args:
            blade_length: Length of blade (heel to toe) in mm
        
        Returns:
            CadQuery Workplane with flat sole geometry
        """
        # TODO: Implement flat sole
        # 
        # Steps:
        # 1. Create rectangular sole surface:
        #    sole = cq.Workplane("XY").rect(blade_length, self.width_center)
        # 
        # 2. Extrude to thickness (~8mm)
        # 
        # 3. Rotate by bounce angle:
        #    sole = sole.rotate((0,0,0), (1,0,0), self.bounce)
        # 
        # Return the sole geometry
        
        raise NotImplementedError("Flat sole generation not yet implemented")
    
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
        # TODO: Implement ground sole (Phase 3)
        # This is the complex part - the art of wedge making
        # 
        # Key insight: Use loft/spline operations to create smooth transitions
        # between different bounce angles along the sole
        
        raise NotImplementedError("Ground sole generation not yet implemented")
    
    def add_leading_edge_radius(self, sole: cq.Workplane) -> cq.Workplane:
        """
        Add subtle radius to leading edge.
        
        Args:
            sole: Existing sole geometry
        
        Returns:
            Sole with leading edge radius applied
        """
        # TODO: Implement leading edge treatment
        # Use fillet operation: sole.edges("|Z").fillet(self.leading_edge_radius)
        raise NotImplementedError()
    
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
        # TODO: Implement grind relief
        # This is complex - need to create variable camber across sole width
        raise NotImplementedError()
    
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
