# pipeline_optimization_app.py

import streamlit as st
import pandas as pd
from pipeline_model import solve_pipeline

st.set_page_config(page_title="Pipeline Operations Optimization", layout="wide")
st.title("Mixed Integer Non‐Linear Convex Optimization of Pipeline Operations")

# ---- Sidebar inputs ----
with st.sidebar:
    st.header("Input Parameters")
    FLOW      = st.number_input("Flow rate (KL/Hr)",                   value=5700.0, step=100.0)
    KV        = st.number_input("Kinematic Viscosity at 15 °C (cSt)",   value=6.45, step=0.01, format="%.2f")
    rho       = st.number_input("Density at 15 °C (kg/m³)",             value=834.0, step=1.0)
    SFC_J     = st.number_input("SFC at Jamnagar (gm/bhp/hr)",          value=155.0, step=1.0)
    SFC_R     = st.number_input("SFC at Rajkot (gm/bhp/hr)",            value=160.0, step=1.0)
    SFC_S     = st.number_input("SFC at Surendranagar (gm/bhp/hr)",     value=165.0, step=1.0)
    Rate_DRA  = st.number_input("DRA unit rate (Rs/Litre)",             value=300.0, step=1.0)
    Price_HSD = st.number_input("HSD unit rate (Rs/Litre)",             value=90.0,  step=1.0)

    run = st.button("Run Optimization")

if run:
    with st.spinner("Solving… this may take a minute or two"):
        results = solve_pipeline(
            FLOW, KV, rho,
            SFC_J, SFC_R, SFC_S,
            Rate_DRA, Price_HSD
        )
    st.success("Optimization complete!")

    # Build output matrix
    stations = ["Vadinar","Jamnagar","Rajkot","Chotila","Surendranagar","Viramgam"]
    data = {
        "Power Cost (INR/day)": [
            results["OF_POWER_1"], results["OF_POWER_2"], results["OF_POWER_3"],
            None,                 results["OF_POWER_4"], None
        ],
        "DRA Cost (INR/day)": [
            results["OF_DRA_1"], results["OF_DRA_2"], results["OF_DRA_3"],
            None,                results["OF_DRA_4"], None
        ],
        "Residual Head (mcl)": [
            results["RH1"], results["RH2"], results["RH3"],
            results["RH4"], results["RH5"], results["RH6"]
        ],
        "SDH (mcl)": [
            results["SDHA_1"], results["SDHA_2"], results["SDHA_3"],
            results["SDHA_4"], results["SDHA_5"], None
        ],
        "No. Pumps": [
            results["NOP1"], results["NOP2"], results["NOP3"],
            None,           results["NOP5"], None
        ],
        "Speed (rpm)": [
            results["N1"], results["N2"], results["N3"],
            None,         results["N5"], None
        ],
        "Efficiency (%)": [
            results["EFFP1"], results["EFFP2"], results["EFFP3"],
            None,             results["EFFP5"], None
        ],
        "Drag Reduction (%)": [
            results["DR1"], results["DR2"], results["DR3"],
            None,           results["DR4"], None
        ],
        "Reynolds No.": [
            results["Re1"], results["Re2"], results["Re3"],
            results["Re5"], results["Re5"], None
        ],
        "Head Loss (dynamic)": [
            results["DH1"], results["DH2"], results["DH3"],
            results["DH5"], results["DH5"], None
        ],
        "Velocity (m/s)": [
            results["v1"], results["v2"], results["v3"],
            results["v4"], results["v5"], results["v6"]
        ],
    }
    df = pd.DataFrame(data, index=stations)
    st.subheader("Optimized Station‐Wise Results")
    st.table(df.style.format("{:,.2f}").to_dict())  # format numbers to two decimals

    # Show total operating cost separately
    st.markdown(f"### Total Operating Cost (INR/day): **{results['Total_Cost']:,.0f}**")
