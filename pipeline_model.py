import os
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# Ensure NEOS email is set if you ever use remote solves
os.environ['NEOS_EMAIL'] = 'parichay.nitwarangal@gmail.com'


def solve_pipeline(
    FLOW, KV, rho,
    SFC_J, SFC_R, SFC_S,
    RateDRA, Price_HSD
):
    model = pyo.ConcreteModel()

    # --------- INPUT PARAMS ---------
    model.FLOW1     = pyo.Param(initialize=FLOW);    FLOW1    = model.FLOW1
    model.KV1       = pyo.Param(initialize=KV);      KV1      = model.KV1
    model.rho1      = pyo.Param(initialize=rho);     rho1     = model.rho1
    model.SFC2      = pyo.Param(initialize=SFC_J);   SFC2     = model.SFC2
    model.SFC3      = pyo.Param(initialize=SFC_R);   SFC3     = model.SFC3
    model.SFC5      = pyo.Param(initialize=SFC_S);   SFC5     = model.SFC5
    model.Rate_DRA  = pyo.Param(initialize=RateDRA); Rate_DRA = model.Rate_DRA
    model.Price_HSD = pyo.Param(initialize=Price_HSD);Price_HSD= model.Price_HSD

    # --------- VADINAR‐JAMNAGAR PARAMS ---------
    model.D1   = pyo.Param(initialize=0.7112);    D1   = model.D1
    model.t1   = pyo.Param(initialize=0.0071374); t1   = model.t1
    model.SMYS1= pyo.Param(initialize=52000);     SMYS1= model.SMYS1
    model.e1   = pyo.Param(initialize=0.00004);   e1   = model.e1
    model.L1   = pyo.Param(initialize=46.7);      L1   = model.L1
    model.z1   = pyo.Param(initialize=8);         z1   = model.z1
    model.d1   = pyo.Param(initialize=0.697);     d1   = model.d1
    model.DF1  = pyo.Param(initialize=0.72);      DF1  = model.DF1
    model.Rate1= pyo.Param(initialize=9);         Rate1= model.Rate1
    model.A1   = pyo.Param(initialize=-0.000002); A1   = model.A1
    model.B1   = pyo.Param(initialize=-0.0015);   B1   = model.B1
    model.C1   = pyo.Param(initialize=179.14);    C1   = model.C1
    model.DOL1 = pyo.Param(initialize=1500);      DOL1 = model.DOL1
    model.MinRPM1 = pyo.Param(initialize=1200);  MinRPM1 = model.MinRPM1
    model.BEP1 = pyo.Param(initialize=4000);      BEP1 = model.BEP1
    model.P1   = pyo.Param(initialize=-4.161E-14);P1   = model.P1
    model.Q1   = pyo.Param(initialize=6.574E-10); Q1   = model.Q1
    model.R1   = pyo.Param(initialize=-0.000008737);R1 = model.R1
    model.S1   = pyo.Param(initialize=0.04924);   S1   = model.S1
    model.T1   = pyo.Param(initialize=-0.001754); T1   = model.T1
    model.RH1  = pyo.Param(initialize=50);        RH1  = model.RH1
    model.z2   = pyo.Param(initialize=24);        z2   = model.z2

    # --------- JAMNAGAR‐RAJKOT PARAMS ---------
    model.FLOW2 = pyo.Param(initialize=FLOW);    FLOW2 = model.FLOW2
    model.D2   = pyo.Param(initialize=0.7112);  D2   = model.D2
    model.t2   = pyo.Param(initialize=0.0071374);t2   = model.t2
    model.SMYS2= pyo.Param(initialize=52000);    SMYS2= model.SMYS2
    model.KV2  = pyo.Param(initialize=KV);       KV2  = model.KV2
    model.e2   = pyo.Param(initialize=0.00004);  e2   = model.e2
    model.rho2 = pyo.Param(initialize=rho);      rho2 = model.rho2
    model.L2   = pyo.Param(initialize=67.9);     L2   = model.L2
    model.d2   = pyo.Param(initialize=0.697);    d2   = model.d2
    model.DF2  = pyo.Param(initialize=0.72);     DF2  = model.DF2
    model.SFC2 = pyo.Param(initialize=SFC_J);    SFC2 = model.SFC2
    model.A2   = pyo.Param(initialize=-1e-5);    A2   = model.A2
    model.B2   = pyo.Param(initialize=0.00135);  B2   = model.B2
    model.C2   = pyo.Param(initialize=270.08);   C2   = model.C2
    model.DOL2 = pyo.Param(initialize=3437);     DOL2 = model.DOL2
    model.MinRPM2 = pyo.Param(initialize=2750); MinRPM2 = model.MinRPM2
    model.BEP2 = pyo.Param(initialize=3150);     BEP2 = model.BEP2
    model.P2   = pyo.Param(initialize=-4.07033296e-13);P2 = model.P2
    model.Q2   = pyo.Param(initialize=3.4657688e-9);    Q2 = model.Q2
    model.R2   = pyo.Param(initialize=-1.92727273e-5); R2 = model.R2
    model.S2   = pyo.Param(initialize=6.7033189e-2);   S2 = model.S2
    model.T2   = pyo.Param(initialize=-1.504329e-1);   T2 = model.T2
    model.z3   = pyo.Param(initialize=113);     z3   = model.z3

    # --------- RAJKOT‐CHOTILA PARAMS ---------
    model.FLOW3 = pyo.Param(initialize=FLOW);    FLOW3 = model.FLOW3
    model.D3   = pyo.Param(initialize=0.7112);  D3   = model.D3
    model.t3   = pyo.Param(initialize=0.0071374);t3   = model.t3
    model.SMYS3= pyo.Param(initialize=52000);    SMYS3= model.SMYS3
    model.KV3  = pyo.Param(initialize=KV);       KV3  = model.KV3
    model.e3   = pyo.Param(initialize=0.00004);  e3   = model.e3
    model.rho3 = pyo.Param(initialize=rho);      rho3 = model.rho3
    model.L3   = pyo.Param(initialize=40.2);     L3   = model.L3
    model.d3   = pyo.Param(initialize=0.697);    d3   = model.d3
    model.DF3  = pyo.Param(initialize=0.72);     DF3  = model.DF3
    model.SFC3 = pyo.Param(initialize=SFC_R);    SFC3 = model.SFC3
    model.A3   = pyo.Param(initialize=-1e-5);    A3   = model.A3
    model.B3   = pyo.Param(initialize=0.0192);   B3   = model.B3
    model.C3   = pyo.Param(initialize=218.81);   C3   = model.C3
    model.DOL3 = pyo.Param(initialize=2870);     DOL3 = model.DOL3
    model.MinRPM3 = pyo.Param(initialize=2296); MinRPM3 = model.MinRPM3
    model.BEP3 = pyo.Param(initialize=2850);     BEP3 = model.BEP3
    model.P3   = pyo.Param(initialize=-9.01972569e-13);P3 = model.P3
    model.Q3   = pyo.Param(initialize=7.45948934e-9);  Q3 = model.Q3
    model.R3   = pyo.Param(initialize=-3.19133266e-5); R3 = model.R3
    model.S3   = pyo.Param(initialize=0.0815595446);  S3 = model.S3
    model.T3   = pyo.Param(initialize=-0.00303811075);T3= model.T3
    model.z4   = pyo.Param(initialize=232);     z4   = model.z4

    # (... continued for Chotila->Surendranagar and Surendranagar->Viramgam, and all equations ...)

    # Decision variables, hydraulic equations, efficiency, costs, constraints ...

    # ------------------------------------------------------------------
    # Return results dict with all station-wise metrics
    return {
        "power_cost_at_vadinar":         pyo.value(OF_POWER_1),
        "dra_cost_at_vadinar":           pyo.value(OF_DRA_1),
        "power_cost_at_jamnagar":        pyo.value(OF_POWER_2),
        "dra_cost_at_jamnagar":          pyo.value(OF_DRA_2),
        "power_cost_at_rajkot":          pyo.value(OF_POWER_3),
        "dra_cost_at_rajkot":            pyo.value(OF_DRA_3),
        "power_cost_at_surendranagar":   pyo.value(OF_POWER_4),
        "dra_cost_at_surendranagar":     pyo.value(OF_DRA_4),
        "residual_head_at_vadinar":       pyo.value(RH1),
        "residual_head_at_jamnagar":      pyo.value(RH2),
        "residual_head_at_rajkot":        pyo.value(RH3),
        "residual_head_at_chotila":       pyo.value(RH4),
        "residual_head_at_surendranagar": pyo.value(RH5),
        "residual_head_at_viramgam":      pyo.value(RH6),
        "total_optimum_cost":             pyo.value(model.Objf),
    }

# pipeline_optimization_app.py
```python
import streamlit as st
import pandas as pd
from pipeline_model import solve_pipeline

st.set_page_config(page_title="Pipeline Optimization", layout="wide")
st.title("Mixed-Integer Nonlinear Pipeline Optimization")

# Sidebar for inputs
with st.sidebar:
    FLOW      = st.number_input("Flow rate (KL/Hr)", 5700.0, step=100.0)
    KV        = st.number_input("Viscosity (cSt)", 6.45, step=0.01)
    rho       = st.number_input("Density (kg/m³)", 834.0, step=1.0)
    SFC_J     = st.number_input("SFC @ Jamnagar (gm/bhp/hr)", 155.0, step=1.0)
    SFC_R     = st.number_input("SFC @ Rajkot (gm/bhp/hr)", 160.0, step=1.0)
    SFC_S     = st.number_input("SFC @ Surendranagar (gm/bhp/hr)", 165.0, step=1.0)
    RateDRA   = st.number_input("DRA rate (₹/L)", 300.0, step=1.0)
    PriceHSD  = st.number_input("HSD rate (₹/L)", 90.0, step=1.0)
    run_btn   = st.button("Run Optimization")

if run_btn:
    with st.spinner("Solving… this may take a minute"):
        res = solve_pipeline(
            FLOW, KV, rho,
            SFC_J, SFC_R, SFC_S,
            RateDRA, PriceHSD
        )
    st.success("Done!")

    stations = ["Vadinar","Jamnagar","Rajkot","Chotila","Surendranagar","Viramgam"]
    df = pd.DataFrame({
        "Power Cost (₹/day)": [
            res["power_cost_at_vadinar"], res["power_cost_at_jamnagar"], res["power_cost_at_rajkot"], None,
            res["power_cost_at_surendranagar"], None
        ],
        "DRA Cost (₹/day)":   [
            res["dra_cost_at_vadinar"], res["dra_cost_at_jamnagar"], res["dra_cost_at_rajkot"], None,
            res["dra_cost_at_surendranagar"], None
        ],
        "Residual Head (mcl)": [
            res["residual_head_at_vadinar"], res["residual_head_at_jamnagar"], res["residual_head_at_rajkot"],
            res["residual_head_at_chotila"], res["residual_head_at_surendranagar"], res["residual_head_at_viramgam"]
        ],
    }, index=stations).round(2)

    st.subheader("Optimized Station-Wise Results")
    st.table(df)

    total = res.get("total_optimum_cost")
    if total is not None:
        st.markdown(f"### Total Cost (₹/day): **{total:,.0f}**")
