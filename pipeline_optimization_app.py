# pipeline_optimization_app.py

import streamlit as st
import builtins, sys, importlib, io
import pandas as pd
import os

st.set_page_config(
    page_title="Pipeline Operations Optimization",
    layout="wide",
)
st.title("MIXED INTEGER NON LINEAR CONVEX OPTIMIZATION OF PIPELINE OPERATIONS")

# Sidebar inputs
with st.sidebar:
    st.header("Input Parameters")
    FLOW      = st.number_input("Flow rate (KL/Hr)",                 value=5700.0, step=100.0, format="%.1f")
    KV        = st.number_input("Kinematic Viscosity at 15 °C (cSt)", value=6.45,  step=0.01, format="%.2f")
    rho       = st.number_input("Density at 15 °C (kg/m³)",           value=834.0,  step=1.0, format="%.1f")
    SFC_J     = st.number_input("SFC at Jamnagar (gm/bhp/hr)",        value=155.0, step=1.0, format="%.1f")
    SFC_R     = st.number_input("SFC at Rajkot (gm/bhp/hr)",          value=160.0, step=1.0, format="%.1f")
    SFC_S     = st.number_input("SFC at Surendranagar (gm/bhp/hr)",   value=165.0, step=1.0, format="%.1f")
    Rate_DRA  = st.number_input("DRA unit rate (₹/Litre)",           value=300.0, step=1.0, format="%.1f")
    Price_HSD = st.number_input("HSD unit rate (₹/Litre)",           value=90.0,  step=1.0, format="%.1f")
    go        = st.button("Run Optimization")

def solve_pipeline(flow, kv, rho, sfc_j, sfc_r, sfc_s, rate_dra, price_hsd):
    """
    Monkey-patch input(), capture print(), reload pipeline_model.py,
    and parse its outputs into a dict (stripping out parentheses).
    """
    vals = list(map(str, [flow, kv, rho, sfc_j, sfc_r, sfc_s, rate_dra, price_hsd]))
    it   = iter(vals)

    # patch input()
    orig_input = builtins.input
    builtins.input = lambda prompt="": next(it)

    # capture stdout
    buf = io.StringIO()
    orig_stdout = sys.stdout
    sys.stdout    = buf

    try:
        import pipeline_model
        importlib.reload(pipeline_model)
    finally:
        builtins.input = orig_input
        sys.stdout    = orig_stdout

    # parse “key = value” lines, stripping spaces, slashes, % and () 
    results = {}
    for line in buf.getvalue().splitlines():
        if "=" in line:
            key, val = line.split("=", 1)
            k = (key.strip().lower()
                 .replace("the value of ", "")
                 .replace("optimum ", "")
                 .replace(" at ", "_")
                 .replace(" ", "_")
                 .replace("%", "pct")
                 .replace("/", "_")
                 .replace("(", "")
                 .replace(")", "")
            )
            try:
                results[k] = float(val.strip())
            except:
                pass
    return results

if go:
    with st.spinner("Solving… this can take a minute or two"):
        res = solve_pipeline(FLOW, KV, rho,
                             SFC_J, SFC_R, SFC_S,
                             Rate_DRA, Price_HSD)
    st.success("Done!")

    # Build DataFrame
    stations = ["Vadinar","Jamnagar","Rajkot","Chotila","Surendranagar","Viramgam"]
    df = pd.DataFrame({
        "Power Cost (INR/day)": [
            res.get("power_cost_at_vadinar"),
            res.get("power_cost_at_jamnagar"),
            res.get("power_cost_at_rajkot"),
            None,
            res.get("power_cost_at_surendranagar"),
            None
        ],
        "DRA Cost (INR/day)": [
            res.get("dra_cost_at_vadinar"),
            res.get("dra_cost_at_jamnagar"),
            res.get("dra_cost_at_rajkot"),
            None,
            res.get("dra_cost_at_surendranagar"),
            None
        ],
        "Residual Head (mcl)": [
            res.get("residual_head_at_vadinar"),
            res.get("residual_head_at_jamnagar"),
            res.get("residual_head_at_rajkot"),
            res.get("residual_head_at_chotila"),
            res.get("residual_head_at_surendranagar"),
            res.get("residual_head_at_viramgam")
        ],
        "SDH (mcl)": [
            res.get("sdh_at_vadinar"),
            res.get("sdh_at_jamnagar"),
            res.get("sdh_at_rajkot"),
            res.get("sdh_at_chotila"),
            res.get("sdh_at_surendranagar"),
            None
        ],
        "No. Pumps": [
            res.get("no_of_operating_pumps_at_vadinar"),
            res.get("no_of_operating_pumps_at_jamnagar"),
            res.get("no_of_operating_pumps_at_rajkot"),
            None,
            res.get("no_of_operating_pumps_at_surendranagar"),
            None
        ],
        "Speed (rpm)": [
            res.get("the_operating_speed_of_each_pump_at_vadinar"),
            res.get("the_operating_speed_of_each_pump_at_jamnagar"),
            res.get("the_operating_speed_of_each_pump_at_rajkot"),
            None,
            res.get("the_operating_speed_of_each_pump_at_surendranagar"),
            None
        ],
        "Efficiency (%)": [
            res.get("value_of_pump_efficiency_at_vadinar"),
            res.get("value_of_pump_efficiency_at_jamnagar"),
            res.get("value_of_pump_efficiency_at_rajkot"),
            None,
            res.get("value_of_pump_efficiency_at_surendranagar"),
            None
        ],
        "Drag Reduction (%)": [
            res.get("percentage_drag_reduction_at_vadinar"),
            res.get("percentage_drag_reduction_at_jamnagar"),
            res.get("percentage_drag_reduction_at_rajkot"),
            None,
            res.get("percentage_drag_reduction_at_surendranagar"),
            None
        ],
        "Reynold's No.": [
            res.get("reynolds_no_at_vadinar"),
            res.get("reynolds_no_at_jamnagar"),
            res.get("reynolds_no_at_rajkot"),
            res.get("reynolds_no_at_chotila"),
            res.get("reynolds_no_at_surendranagar"),
            None
        ],
        "Head Loss (dynamic)": [
            res.get("head_loss_dynamic_at_vadinar"),
            res.get("head_loss_dynamic_at_jamnagar"),
            res.get("head_loss_dynamic_at_rajkot"),
            res.get("head_loss_dynamic_at_chotila"),
            res.get("head_loss_dynamic_at_surendranagar"),
            None
        ],
        "Velocity (m/s)": [
            res.get("velocity_at_vadinar"),
            res.get("velocity_at_jamnagar"),
            res.get("velocity_at_rajkot"),
            res.get("velocity_at_chotila"),
            res.get("velocity_at_surendranagar"),
            res.get("velocity_at_viramgam")
        ],
    }, index=stations)

    st.subheader("Optimized Station-Wise Results")
    st.table(df.round(2))

    # Safely format total even if it's missing
    total = res.get("total_operating_cost_inr_day")
    if total is not None:
        st.markdown(f"### **Total Operating Cost (INR/day): {total:,.0f}**")
    else:
        st.markdown("### **Total Operating Cost (INR/day): N/A**")
