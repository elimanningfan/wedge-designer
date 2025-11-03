"""
Streamlit web interface for Parametric Golf Wedge Designer
Run with: streamlit run app.py --server.port 8000
"""

import streamlit as st
import sys
import os
from datetime import datetime
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import cadquery as cq
from config_loader import WedgeConfig
from wedge_generator import generate_wedge
from geometry.hosel import WedgeHosel
from geometry.blade import WedgeBlade
from geometry.sole import WedgeSole
from utils import calculate_weight, calculate_center_of_gravity

# Page config
st.set_page_config(
    page_title="Wedge Designer",
    page_icon="🏌️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🏌️ Parametric Golf Wedge Designer")
st.markdown("**Design custom golf wedges with real-time parameter control**")
st.markdown("---")

# Sidebar for parameters
with st.sidebar:
    st.header("⚙️ Wedge Parameters")

    st.subheader("📐 Primary Angles")
    loft = st.slider("Loft (°)", 45, 64, 56, 1,
                     help="Club face angle - affects trajectory and distance")
    lie = st.slider("Lie (°)", 60, 66, 64, 1,
                    help="Shaft angle to ground - affects strike pattern")
    bounce = st.slider("Bounce (°)", 0, 16, 8, 1,
                       help="Sole angle - prevents digging into turf")

    st.subheader("📏 Blade Dimensions")
    blade_length = st.slider("Blade Length (mm)", 65, 80, 74, 1,
                              help="Heel to toe length")
    face_height = st.slider("Face Height (mm)", 40, 55, 49, 1,
                             help="Leading edge to topline")
    topline_thickness = st.slider("Topline (mm)", 2.0, 4.0, 3.0, 0.1,
                                   help="Thickness of top edge")

    st.subheader("👟 Sole Design")
    sole_width = st.slider("Sole Width (mm)", 15, 30, 21, 1,
                            help="Width at center - wider = more forgiveness")
    heel_relief = st.slider("Heel Relief (°)", 0.0, 4.0, 1.5, 0.1,
                             help="Camber at heel - allows opening face")
    toe_relief = st.slider("Toe Relief (°)", 0.0, 4.0, 2.0, 0.1,
                            help="Camber at toe - versatility")

    st.subheader("🔧 Hosel")
    hosel_height = st.slider("Hosel Height (mm)", 35, 50, 42, 1)
    hosel_outer = st.slider("Outer Diameter (mm)", 12.0, 17.0, 14.5, 0.1)
    hosel_bore = st.number_input("Bore Diameter (mm)", 9.2, 9.6, 9.4, 0.01,
                                  help="⚠️ Critical: 9.4mm for standard shaft")
    hosel_bore_depth = st.slider("Bore Depth (mm)", 30, 45, 38, 1)

    st.subheader("🎯 Grooves")
    groove_count = st.slider("Number of Grooves", 8, 14, 12, 1)
    groove_spacing = st.slider("Groove Spacing (mm)", 3.0, 3.81, 3.81, 0.01,
                                help="⚠️ USGA Max: 3.81mm")
    groove_width = st.slider("Groove Width (mm)", 0.7, 1.0, 0.9, 0.05)
    groove_depth = st.slider("Groove Depth (mm)", 0.3, 0.5, 0.4, 0.05)

    st.subheader("🏋️ Target Specs")
    target_weight = st.number_input("Target Weight (g)", 280, 310, 292, 1)

    st.markdown("---")
    wedge_name = st.text_input("Wedge Name", f"Custom_{loft}_{bounce}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Design Summary")

    # Show current configuration
    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        st.metric("Loft", f"{loft}°")
        st.metric("Lie", f"{lie}°")
        st.metric("Bounce", f"{bounce}°")

    with summary_col2:
        st.metric("Blade Length", f"{blade_length}mm")
        st.metric("Face Height", f"{face_height}mm")
        st.metric("Sole Width", f"{sole_width}mm")

    with summary_col3:
        st.metric("Grooves", groove_count)
        st.metric("Spacing", f"{groove_spacing}mm")
        st.metric("Target Weight", f"{target_weight}g")

    # Grind profile description
    st.subheader("🎨 Grind Profile")

    if heel_relief > 2.5 or toe_relief > 2.5:
        grind_type = "High Relief (S-Grind style)"
        grind_desc = "Versatile grind for opening/closing face. Good for varied lies."
    elif sole_width > 23:
        grind_type = "Wide Sole (K-Grind style)"
        grind_desc = "Bunker specialist. High forgiveness, prevents digging."
    elif bounce < 6:
        grind_type = "Low Bounce (L-Grind style)"
        grind_desc = "For firm conditions and sweepers. Less forgiveness."
    else:
        grind_type = "Standard (F/M-Grind style)"
        grind_desc = "Versatile all-around grind. Works from most lies."

    st.info(f"**{grind_type}**\n\n{grind_desc}")

    # USGA Compliance
    if groove_spacing <= 3.81:
        st.success("✓ USGA Compliant - Groove spacing meets regulations")
    else:
        st.error("⚠️ Non-Conforming - Groove spacing exceeds USGA limit (3.81mm)")

    if hosel_bore != 9.4:
        st.warning(f"⚠️ Non-standard bore diameter ({hosel_bore}mm). Standard is 9.4mm (0.370\")")

with col2:
    st.header("🚀 Generate Wedge")

    # Generate button
    if st.button("Generate STEP File", type="primary", use_container_width=True):
        with st.spinner("Generating wedge geometry..."):
            try:
                # Build configuration dict
                config_dict = {
                    'wedge_specs': {
                        'name': wedge_name,
                        'loft': loft,
                        'lie': lie,
                        'bounce': bounce,
                        'face_progression': 2.5,
                        'blade_length': blade_length,
                        'face_height': face_height,
                        'topline_thickness': topline_thickness,
                        'hosel': {
                            'height': hosel_height,
                            'outer_diameter': hosel_outer,
                            'bore_diameter': hosel_bore,
                            'bore_depth': hosel_bore_depth,
                            'bore_taper': 0
                        },
                        'sole': {
                            'width_center': sole_width,
                            'width_heel': sole_width - 3,
                            'width_toe': sole_width - 4,
                            'leading_edge_radius': 0.6,
                            'trailing_edge_relief': 2.0,
                            'trailing_edge_start': 15,
                            'heel_relief_start': 12,
                            'heel_relief_angle': heel_relief,
                            'toe_relief_start': 18,
                            'toe_relief_angle': toe_relief,
                            'bounce_rocker_radius': 180,
                            'sole_camber_radius': 200
                        },
                        'face': {
                            'surface_roughness': 110,
                            'grooves': {
                                'spacing': groove_spacing,
                                'width': groove_width,
                                'depth': groove_depth,
                                'count': groove_count,
                                'edge_clearance': 3,
                                'groove_type': 'V'
                            }
                        },
                        'weight': {
                            'target_head_weight': target_weight,
                            'tolerance': 5,
                            'center_of_gravity': {
                                'from_face': 20,
                                'from_heel': 37,
                                'from_sole': 19
                            }
                        },
                        'material': {
                            'type': '8620 carbon steel',
                            'density': 7.85
                        }
                    }
                }

                # Generate geometry
                st.write("Creating hosel...")
                hosel = WedgeHosel(config_dict['wedge_specs']['hosel'])
                hosel_geo = hosel.generate()

                st.write("Creating blade...")
                blade = WedgeBlade(config_dict['wedge_specs'])
                blade_geo = blade.generate()

                st.write("Adding grooves...")
                if 'face' in config_dict['wedge_specs'] and 'grooves' in config_dict['wedge_specs']['face']:
                    groove_config = config_dict['wedge_specs']['face']['grooves']
                    blade_geo = blade.add_grooves(blade_geo, groove_config)

                st.write("Creating sole with grind...")
                sole = WedgeSole(config_dict['wedge_specs'])
                sole_geo = sole.generate_with_grind(blade_length)

                st.write("Assembling components...")
                # Position hosel
                hosel_positioned = hosel_geo.translate((
                    -blade_length / 2 + 10,
                    0,
                    45
                ))
                hosel_positioned = hosel_positioned.rotate(
                    (-blade_length / 2 + 10, 0, 45),
                    (1, 0, 0),
                    -(90 - lie)
                )

                # Combine
                wedge = blade_geo.union(sole_geo).union(hosel_positioned)

                # Calculate metrics
                st.write("Calculating metrics...")
                actual_weight = calculate_weight(wedge, '8620_steel')
                cg = calculate_center_of_gravity(wedge)

                # Export
                st.write("Exporting STEP file...")
                os.makedirs("output/step_files", exist_ok=True)

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{wedge_name.replace(' ', '_')}_{loft}_{bounce}_{timestamp}.step"
                filepath = os.path.join("output/step_files", filename)

                cq.exporters.export(wedge, filepath)
                file_size = os.path.getsize(filepath)

                # Store in session state for download
                st.session_state['last_file'] = filepath
                st.session_state['last_filename'] = filename
                st.session_state['last_weight'] = actual_weight
                st.session_state['last_cg'] = cg
                st.session_state['last_size'] = file_size

                st.success("✓ Wedge generated successfully!")

            except Exception as e:
                st.error(f"Error generating wedge: {str(e)}")
                st.exception(e)

    # Download section
    if 'last_file' in st.session_state and os.path.exists(st.session_state['last_file']):
        st.markdown("---")
        st.subheader("📥 Download")

        with open(st.session_state['last_file'], 'rb') as f:
            st.download_button(
                label="⬇️ Download STEP File",
                data=f,
                file_name=st.session_state['last_filename'],
                mime="application/step",
                use_container_width=True
            )

        st.caption(f"File size: {st.session_state['last_size']:,} bytes")

        # Show metrics
        st.markdown("---")
        st.subheader("📊 Validation")

        weight_variance = abs(st.session_state['last_weight'] - target_weight)
        if weight_variance <= 5:
            st.success(f"✓ Weight: {st.session_state['last_weight']:.1f}g")
        else:
            st.warning(f"⚠️ Weight: {st.session_state['last_weight']:.1f}g (target: {target_weight}g)")

        cg_x, cg_y, cg_z = st.session_state['last_cg']
        st.info(f"Center of Gravity:\n- X: {cg_x:.1f}mm\n- Y: {cg_y:.1f}mm\n- Z: {cg_z:.1f}mm")

# Footer
st.markdown("---")
st.markdown("""
### 📖 Next Steps

1. **Download** the STEP file above
2. **Open** in FreeCAD or Fusion 360 to inspect
3. **Verify** dimensions and geometry
4. **Send** to fabricator with `docs/fabricator_specs.md`

### 🔧 CAD Software (Free)
- [FreeCAD](https://www.freecad.org/) - Free, cross-platform
- [Fusion 360](https://www.autodesk.com/products/fusion-360) - Free for hobbyists

### 🏌️ Wedge Design Tips
- **Higher loft** (58-60°) = More height, less distance (lob wedge)
- **Higher bounce** (10-14°) = More forgiveness, better for bunkers
- **More relief** (3-4°) = More versatility, can open/close face
- **Wider sole** (24-28mm) = More forgiveness, prevents digging
""")

st.caption("Built with CadQuery & Streamlit | GitHub: elimanningfan/wedge-designer")
