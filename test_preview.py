"""
Test 3D preview generation to debug visualization issues
"""

import sys
sys.path.insert(0, 'src')

from geometry.hosel import WedgeHosel
from geometry.blade import WedgeBlade
from geometry.sole import WedgeSole
from utils import create_3d_preview
import cadquery as cq

# Build test wedge
print("Building test wedge for preview...")

hosel = WedgeHosel({
    'height': 42,
    'outer_diameter': 14.5,
    'bore_diameter': 9.4,
    'bore_depth': 38
})
hosel_geo = hosel.generate()
print(f"Hosel created - BBox: {hosel_geo.val().BoundingBox()}")

blade = WedgeBlade({
    'blade_length': 74,
    'face_height': 49,
    'topline_thickness': 3.0,
    'loft': 56,
    'lie': 64
})
blade_geo = blade.generate()
print(f"Blade created - BBox: {blade_geo.val().BoundingBox()}")

sole = WedgeSole({
    'bounce': 8,
    'sole': {
        'width_center': 21,
        'heel_relief_angle': 1.5,
        'toe_relief_angle': 2.0
    }
})
sole_geo = sole.generate_flat_sole(74)
print(f"Sole created - BBox: {sole_geo.val().BoundingBox()}")

# Position hosel
hosel_positioned = hosel_geo.translate((-74/2 + 10, 0, 45))
hosel_positioned = hosel_positioned.rotate((-74/2 + 10, 0, 45), (1, 0, 0), -(90 - 64))

# Combine
print("\nAssembling components...")
wedge = blade_geo.union(sole_geo).union(hosel_positioned)
bbox = wedge.val().BoundingBox()

print(f"\nComplete wedge BBox:")
print(f"  X: [{bbox.xmin:.1f}, {bbox.xmax:.1f}] (length: {bbox.xlen:.1f}mm)")
print(f"  Y: [{bbox.ymin:.1f}, {bbox.ymax:.1f}] (depth: {bbox.ylen:.1f}mm)")
print(f"  Z: [{bbox.zmin:.1f}, {bbox.zmax:.1f}] (height: {bbox.zlen:.1f}mm)")

# Test STL export
print("\nTesting STL export...")
try:
    cq.exporters.export(wedge, "output/step_files/test_preview.stl", exportType='STL')
    import os
    size = os.path.getsize("output/step_files/test_preview.stl")
    print(f"✓ STL exported: {size:,} bytes")

    # Count triangles
    with open("output/step_files/test_preview.stl", 'r') as f:
        content = f.read()
        triangle_count = content.count('endfacet')
    print(f"  Triangles: {triangle_count}")

except Exception as e:
    print(f"✗ STL export failed: {str(e)}")

# Try the preview function
print("\nTesting preview generation...")
try:
    fig = create_3d_preview(wedge)
    print(f"✓ Preview created: {type(fig)}")
    print(f"  Data traces: {len(fig.data)}")
    if len(fig.data) > 0:
        print(f"  Vertices: {len(fig.data[0].x)}")
        print(f"  Triangles: {len(fig.data[0].i)}")
except Exception as e:
    print(f"✗ Preview failed: {str(e)}")
    import traceback
    traceback.print_exc()
