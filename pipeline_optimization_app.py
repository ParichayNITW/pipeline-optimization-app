import streamlit as st
import pyomo.environ as pyo
from pyomo.opt import SolverManagerFactory
from math import log10
import os
from pipeline_model import solve_model  # Imported from external file

# Set environment for NEOS
os.environ['NEOS_EMAIL'] = 'parichay.nitwarangal@gmail.com'

# Streamlit UI
st.set_page_config(page_title="Pipeline Optimization", layout="wide")

st.title("Pipeline Operations Optimization")

with st.sidebar:
    st.header("Input Parameters")

    FLOW = st.number_input("Flow Rate (KL/Hr)", value=5700.0)
    KV = st.number_input("Kinematic Viscosity (cSt)", value=6.45)
    rho = st.number_input("Density (kg/m³)", value=834.0)
    SFC_J = st.number_input("SFC at Jamnagar (gm/bhp/hr)", value=155.0)
    SFC_R = st.number_input("SFC at Rajkot (gm/bhp/hr)", value=160.0)
    SFC_S = st.number_input("SFC at Surendranagar (gm/bhp/hr)", value=165.0)
    RateDRA = st.number_input("Rate of DRA (Rs/Litre)", value=300.0)
    Price_HSD = st.number_input("Price of HSD Fuel (Rs/Litre)", value=90.0)

    solve = st.button("Run Optimization")

if solve:
    with st.spinner("Running Optimization..."):
        model = solve_model(FLOW, KV, rho, SFC_J, SFC_R, SFC_S, RateDRA, Price_HSD)

        st.success("Optimization Completed!")

        st.subheader("Optimized Outputs")

        data = {
            "Station": ["Vadinar", "Jamnagar", "Rajkot", "Chotila", "Surendranagar", "Viramgam"],
            "Power & Fuel Cost (INR/day)": [model.OF_POWER_1(), model.OF_POWER_2(), model.OF_POWER_3(), "-", model.OF_POWER_4(), "-"],
            "DRA Cost (INR/day)": [model.OF_DRA_1(), model.OF_DRA_2(), model.OF_DRA_3(), "-", model.OF_DRA_4(), "-"],
            "Total Operating Cost (INR/day)": [
                model.OF_POWER_1() + model.OF_DRA_1(),
                model.OF_POWER_2() + model.OF_DRA_2(),
                model.OF_POWER_3() + model.OF_DRA_3(),
                "-",
                model.OF_POWER_4() + model.OF_DRA_4(),
                "-"],
            "Residual Head (mcl)": [model.RH1, model.RH2(), model.RH3(), model.RH4(), model.RH5(), model.RH6()],
            "SDH (mcl)": [model.SDHA_1(), model.SDHA_2(), model.SDHA_3(), model.SDHA_4, model.SDHA_5(), "-"],
            "Operating Pumps": [model.NOP1(), model.NOP2(), model.NOP3(), "-", model.NOP5(), "-"],
            "Speed of Pumps (rpm)": [model.N1(), model.N2(), model.N3(), "-", model.N5(), "-"],
            "Pump Efficiency (%)": [model.EFFP1(), model.EFFP2(), model.EFFP3(), "-", model.EFFP5(), "-"],
            "Drag Reduction (%)": [model.DR1(), model.DR2(), model.DR3(), "-", model.DR4(), "-"],
            "Head Loss (dynamic)": [model.DH1, model.DH2, model.DH3, model.DH4, model.DH5, "-"],
            "Velocity (m/sec)": [model.v1, model.v2, model.v3, model.v4, model.v5, "-"]
        }

        st.table(data)

st.markdown("---")
st.caption("Developed by Parichay Das")
