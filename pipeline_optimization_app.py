import streamlit as st
import pyomo.environ as pyo
from pyomo.opt import SolverManagerFactory
import os
import time
import pandas as pd

# Set NEOS email for authentication
os.environ['NEOS_EMAIL'] = 'parichay.nitwarangal@gmail.com'

st.set_page_config(page_title="Pipeline Optimization App", layout="wide")
st.title("MIXED INTEGER NON LINEAR CONVEX OPTIMIZATION OF PIPELINE OPERATIONS")
st.subheader("Total Operating Cost (INR/day) = model.Objf()")

# Sidebar for inputs
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
    run_button = st.button("Run Optimization")

@st.cache_data(show_spinner=False)
def run_optimization(FLOW, KV, rho, SFC_J, SFC_R, SFC_S, RateDRA, Price_HSD):
    from pipeline_model import solve_model
    try:
        model, results = solve_model(FLOW, KV, rho, SFC_J, SFC_R, SFC_S, RateDRA, Price_HSD)
        return model, results
    except Exception as e:
        return None, str(e)

if run_button:
    with st.spinner("Running Optimization on NEOS Server... Please wait. This may take several minutes."):
        start_time = time.time()
        model, result_or_error = run_optimization(FLOW, KV, rho, SFC_J, SFC_R, SFC_S, RateDRA, Price_HSD)

        if model is None:
            st.error(f"Optimization failed: {result_or_error}")
        else:
            st.success("Optimization Completed!")
            st.subheader("Optimized Output Matrix")

            data = {
                "": ["Power and Fuel cost (INR/day)", "DRA cost (INR/day)", "Total Operating Cost (INR/day)",
                      "RH (mcl)", "SDH (mcl)", "Req. no. of Operating Pumps", "Speed of each Operating Pump (rpm)",
                      "Pump efficiency (%)", "Req. Drag reduction (%)", "Reynold's no.", "Head Loss (dynamic)", "Velocity (m/sec)"],
                "Vadinar": [model.OF_POWER_1(), model.OF_DRA_1(), model.OF_POWER_1() + model.OF_DRA_1(),
                            model.RH1, model.SDHA_1(), model.NOP1(), model.N1(), model.EFFP1(), model.DR1(), model.Re1, model.DH1, model.v1],
                "Jamnagar": [model.OF_POWER_2(), model.OF_DRA_2(), model.OF_POWER_2() + model.OF_DRA_2(),
                             model.RH2(), model.SDHA_2(), model.NOP2(), model.N2(), model.EFFP2(), model.DR2(), model.Re2, model.DH2, model.v2],
                "Rajkot": [model.OF_POWER_3(), model.OF_DRA_3(), model.OF_POWER_3() + model.OF_DRA_3(),
                           model.RH3(), model.SDHA_3(), model.NOP3(), model.N3(), model.EFFP3(), model.DR3(), model.Re3, model.DH3, model.v3],
                "Chotila": ["-", "-", "-", model.RH4(), model.SDHA_4, "-", "-", "-", "-", model.Re4, model.DH4, model.v4],
                "Surendranagar": [model.OF_POWER_4(), model.OF_DRA_4(), model.OF_POWER_4() + model.OF_DRA_4(),
                                   model.RH5(), model.SDHA_5(), model.NOP5(), model.N5(), model.EFFP5(), model.DR4(), model.Re5, model.DH5, model.v5],
                "Viramgam": ["-", "-", "-", model.RH6(), "-", "-", "-", "-", "-", model.Re6, "-", model.v6]
            }

            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            st.markdown("---")
            st.metric("Total Optimized Cost (INR/day)", f"{model.Objf():,.2f}")

st.markdown("---")
st.caption("Developed by Parichay Das")
