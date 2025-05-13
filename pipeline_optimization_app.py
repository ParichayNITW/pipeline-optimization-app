# pipeline_optimization_app.py

import re
import streamlit as st
import builtins, sys, importlib, io
import pandas as pd

st.set_page_config(
    page_title="Pipeline Operations Optimization",
    layout="wide",
)
st.title("MIXED INTEGER NON LINEAR CONVEX OPTIMIZATION OF PIPELINE OPERATIONS")

# Sidebar inputs
with st.sidebar:
    st.header("Input Parameters")
    FLOW      = st.number_input("Flow rate (KL/Hr)",                   value=5700.0, step=100.0, format="%.1f")
    KV        = st.number_input("Kinematic Viscosity at 15 °C (cSt)",   value=6.45,  step=0.01, format="%.2f")
    rho       = st.number_input("Density at 15 °C (kg/m³)",             value=834.0,  step=1.0, format="%.1f")
    SFC_J     = st.number_input("SFC at Jamnagar (gm/bhp/hr)",          value=155.0, step=1.0, format="%.1f")
    SFC_R     = st.number_input("SFC at Rajkot (gm/bhp/hr)",            value=160.0, step=1.0, format="%.1f")
    SFC_S     = st.number_input("SFC at Surendranagar (gm/bhp/hr)",     value=165.0, step=1.0, format="%.1f")
    Rate_DRA  = st.number_input("DRA unit rate (₹/Litre)",             value=300.0, step=1.0, format="%.1f")
    Price_HSD = st.number_input("HSD unit rate (₹/Litre)",             value=90.0,  step=1.0, format="%.1f")
    go        = st.button("Run Optimization")

def _normalize_key(raw: str) -> str:
    """
    Turn:
       'Optimum Power Cost at Vadinar'
    into:
       'power_cost_at_vadinar'
    """
    s = raw.strip().lower()
    # drop leading 'the '
    if s.startswith("the "):
        s = s[4:]
    # drop 'optimum ' prefix
    if s.startswith("optimum "):
        s = s[len("optimum "):]
    # drop 'value of ' prefix
    if s.startswith("value of "):
        s = s[len("value of "):]
    # drop 'percentage ' prefix
    if s.startswith("percentage "):
        s = s[len("percentage "):]
    # drop 'no. of ' or 'no of '
    s = re.sub(r"^no\.?\s+of\s+", "no_of_", s)
    # punctuation
    s = s.replace("%", "pct")
    s = s.replace("(", "").replace(")", "")
    s = s.replace("/", "_")
    s = s.replace(",", "")
    # turn ' at ' → '_at_'
    s = re.sub(r"\s+at\s+", "_at_", s)
    # any other non-alnum → underscore
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    return s

def solve_pipeline(flow, kv, rho, sfc_j, sfc_r, sfc_s, rate_dra, price_hsd):
    """
    Monkey-patch input(), capture print() from pipeline_model.py,
    and return a dict of normalized keys → floats.
    """
    # Prepare the 8 inputs
    inputs = list(map(str, [flow, kv, rho, sfc_j, sfc_r, sfc_s, rate_dra, price_hsd]))
    it = iter(inputs)

    # Patch input()
    orig_input = builtins.input
    builtins.input = lambda prompt="": next(it)

    # Capture stdout
    buf = io.StringIO()
    orig_stdout = sys.stdout
    sys.stdout    = buf

    try:
        import pipeline_model
        importlib.reload(pipeline_model)
    finally:
        # Restore
        builtins.input = orig_input
        sys.stdout    = orig_stdout

    # Parse lines like "Optimum Power Cost at Vadinar =  12345.67"
    res = {}
    for line in buf.getvalue().splitlines():
        if "=" not in line:
            continue
        key_part, val_part = line.split("=", 1)
        key_norm = _normalize_key(key_part)
        # try to pull a float
        m = re.search(r"([-+]?\d*\.?\d+)", val_part)
        if not m:
            continue
        try:
            res[key_norm] = float(m.group(1))
        except:
            pass
    return res

if go:
    with st.spinner("Solving… this can take a minute or two"):
        r = solve_pipeline(FLOW, KV, rho,
                           SFC_J, SFC_R, SFC_S,
                           Rate_DRA, Price_HSD)
    st.success("Done!")

    # Build DataFrame exactly as per your layout
    stations = ["Vadinar","Jamnagar","Rajkot","Chotila","Surendranagar","Viramgam"]
    df = pd.DataFrame({
        "Power Cost (INR/day)": [
            r.get("power_cost_at_vadinar"),
            r.get("power_cost_at_jamnagar"),
            r.get("power_cost_at_rajkot"),
            None,
            r.get("power_cost_at_surendranagar"),
            None
        ],
        "DRA Cost (INR/day)": [
            r.get("dra_cost_at_vadinar"),
            r.get("dra_cost_at_jamnagar"),
            r.get("dra_cost_at_rajkot"),
            None,
            r.get("dra_cost_at_surendranagar"),
            None
        ],
        "Residual Head (mcl)": [
            r.get("residual_head_at_vadinar"),       # will be None (model doesn’t print RH1)
            r.get("residual_head_at_jamnagar"),
            r.get("residual_head_at_rajkot"),
            r.get("residual_head_at_chotila"),
            r.get("residual_head_at_surendranagar"),
            r.get("residual_head_at_viramgam")
        ],
        "SDH (mcl)": [
            r.get("sdh_at_vadinar"),
            r.get("sdh_at_jamnagar"),
            r.get("sdh_at_rajkot"),
            r.get("sdh_at_chotila"),
            r.get("sdh_at_surendranagar"),
            None
        ],
        "No. Pumps": [
            r.get("no_of_operating_pumps_at_vadinar"),
            r.get("no_of_operating_pumps_at_jamnagar"),
            r.get("no_of_operating_pumps_at_rajkot"),
            None,
            r.get("no_of_operating_pumps_at_surendranagar"),
            None
        ],
        "Speed (rpm)": [
            r.get("operating_speed_of_each_pump_at_vadinar"),
            r.get("operating_speed_of_each_pump_at_jamnagar"),
            r.get("operating_speed_of_each_pump_at_rajkot"),
            None,
            r.get("operating_speed_of_each_pump_at_surendranagar"),
            None
        ],
        "Efficiency (%)": [
            r.get("pump_efficiency_at_vadinar"),
            r.get("pump_efficiency_at_jamnagar"),
            r.get("pump_efficiency_at_rajkot"),
            None,
            r.get("pump_efficiency_at_surendranagar"),
            None
        ],
        "Drag Reduction (%)": [
            r.get("drag_reduction_at_vadinar"),
            r.get("drag_reduction_at_jamnagar"),
            r.get("drag_reduction_at_rajkot"),
            None,
            r.get("drag_reduction_at_surendranagar"),
            None
        ],
        # Reynolds, Head Loss, Velocity never get printed by your model,
        # so these will remain blank (None).
        "Reynold's No.":    [None]*6,
        "Head Loss (dynamic)": [None]*6,
        "Velocity (m/s)":    [None]*6,
    }, index=stations)

    st.subheader("Optimized Station-Wise Results")
    st.table(df.round(2))

    # Total cost
    total = r.get("total_optimum_cost")
    if total is not None:
        st.markdown(f"### Total Optimum Cost (INR/day): **{total:,.0f}**")
    else:
        st.markdown("### Total Optimum Cost (INR/day): **N/A**")
