"""
Integration test for complete wedge generation.
Tests all geometry components and full wedge assembly.
"""

import sys
import os

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import cadquery as cq
from geometry.hosel import WedgeHosel
from geometry.blade import WedgeBlade
from geometry.sole import WedgeSole
from config_loader import load_config


def test_hosel():
    """Test hosel generation."""
    print("\n" + "="*60)
    print("Testing Hosel Generation")
    print("="*60)

    config = {
        'height': 42,
        'outer_diameter': 14.5,
        'bore_diameter': 9.4,
        'bore_depth': 38
    }

    hosel = WedgeHosel(config)
    hosel.validate()
    geometry = hosel.generate()

    # Check it's a valid solid
    assert geometry.val().isValid(), "Hosel geometry is not valid"

    print("✓ Hosel generation successful")
    return True


def test_blade():
    """Test blade generation."""
    print("\n" + "="*60)
    print("Testing Blade Generation")
    print("="*60)

    config = {
        'blade_length': 74,
        'face_height': 49,
        'topline_thickness': 3.0,
        'loft': 56,
        'lie': 64
    }

    blade = WedgeBlade(config)
    blade.validate()
    geometry = blade.generate()

    # Check it's a valid solid
    assert geometry.val().isValid(), "Blade geometry is not valid"

    print("✓ Blade generation successful")
    return True


def test_sole():
    """Test sole generation."""
    print("\n" + "="*60)
    print("Testing Sole Generation")
    print("="*60)

    config = {
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

    sole = WedgeSole(config)
    sole.validate()
    geometry = sole.generate_flat_sole(74)

    # Check it's a valid solid
    assert geometry.val().isValid(), "Sole geometry is not valid"

    print("✓ Sole generation successful")
    return True


def test_full_wedge_generation():
    """Test complete wedge generation from config."""
    print("\n" + "="*60)
    print("Testing Full Wedge Generation")
    print("="*60)

    # Load the Vokey config
    config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'vokey_56_8.yaml')
    config = load_config(config_path)

    wedge_specs = config.get('wedge_specs', {})

    # Generate all components
    hosel = WedgeHosel(wedge_specs.get('hosel', {}))
    hosel_geo = hosel.generate()

    blade = WedgeBlade(wedge_specs)
    blade_geo = blade.generate()

    sole = WedgeSole(wedge_specs)
    sole_geo = sole.generate_flat_sole(wedge_specs.get('blade_length', 74))

    # Combine them
    wedge = blade_geo.union(sole_geo).union(hosel_geo)

    # Check it's a valid solid
    assert wedge.val().isValid(), "Combined wedge geometry is not valid"

    # Export to verify
    os.makedirs("output/step_files", exist_ok=True)
    output_path = "output/step_files/test_full_wedge.step"
    cq.exporters.export(wedge, output_path)

    file_size = os.path.getsize(output_path)
    print(f"✓ Full wedge generated and exported ({file_size:,} bytes)")
    print(f"  File: {output_path}")

    return True


def run_all_tests():
    """Run all integration tests."""
    print("="*60)
    print("WEDGE GENERATOR INTEGRATION TESTS")
    print("="*60)

    tests = [
        ("Hosel", test_hosel),
        ("Blade", test_blade),
        ("Sole", test_sole),
        ("Full Wedge", test_full_wedge_generation),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success, None))
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"✗ {name} test failed: {str(e)}")

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for name, success, error in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
        if error:
            print(f"  Error: {error}")

    print("\n" + "-"*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
