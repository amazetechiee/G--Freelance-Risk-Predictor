# """
# app.py
# The complete production-grade Streamlit Web Application Interface.
# Includes real-time ML inference, strict business guardrails, dynamic Matplotlib dial gauge,
# and SQLite database tracking localized to Indian Standard Time (IST).
# """
# #version 1

# import os
# import sqlite3
# import pickle
# from datetime import datetime, timedelta
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import streamlit as st

# # --- Page Config ---
# st.set_page_config(page_title="Freelance Project Risk Engine", layout="centered", page_icon="🔍")

# DB_PATH = "data/freelance.db"
# MODEL_PATH = "models/model.pkl"

# # --- Helper: Convert UTC string to IST Display String ---
# def convert_utc_to_ist(utc_str):
#     try:
#         # SQLite CURRENT_TIMESTAMP format: YYYY-MM-DD HH:MM:SS
#         utc_dt = datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S")
#         # Add IST offset (+5 hours, 30 minutes)
#         ist_dt = utc_dt + timedelta(hours=5, minutes=30)
#         return ist_dt.strftime("%d-%b-%Y %I:%M %p")
#     except Exception:
#         return utc_str

# # --- Helper: Draw Matplotlib Gauge Dial ---
# def draw_gauge_dial(score):
#     fig, ax = plt.subplots(figsize=(6, 1.5))
#     # Draw a thin horizontal color block mapping risk levels
#     # Red: [0.0 to 0.4], Yellow: [0.4 to 0.65], Green: [0.65 to 1.0]
#     ax.axvspan(0, 40, color="#ff4d4d", alpha=0.9, label="High Risk")
#     ax.axvspan(40, 65, color="#ffcc00", alpha=0.9, label="Caution")
#     ax.axvspan(65, 100, color="#2ecc71", alpha=0.9, label="Safe Track")
    
#     # Plot the slider position needle based on calculated certainty score
#     needle_pos = (1 - score) * 100 # Inverse because high score means high risk
#     ax.axvline(x=needle_pos, color="black", linewidth=4, linestyle="-")
#     ax.plot(needle_pos, 0.5, marker="v", color="black", markersize=12)
    
#     ax.set_xlim(0, 100)
#     ax.set_ylim(0, 1)
#     ax.set_yticks([])
#     ax.set_xticks([20, 52.5, 82.5])
#     ax.set_xticklabels(["High Risk", "Caution Zone", "Safe Track"], fontsize=9, fontweight='bold')
#     ax.set_title(f"Live Confidence Health Gauge (Pointer: {needle_pos:.1f}%)", fontsize=10, pad=8)
#     plt.tight_layout()
#     return fig

# # --- Main Core UI Layout ---
# st.title("🇮🇳 Freelance Project Budget & Delivery Risk Predictor")
# st.markdown("Auditing tech contract viability to catch mathematically doomed deliveries early.")

# # Horizontal Dual Navigation Tabs
# tab_audit, tab_logs = st.tabs(["🔍 Contract Risk Audit", "📜 System Database Logs"])

# # ==============================================================================
# # TAB 1: RISK AUDIT PANEL
# # ==============================================================================
# with tab_audit:
#     st.subheader("🛠️ Contract Parameters Configuration")
    
#     with st.form("audit_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             experience = st.number_input("Developer Experience (Years)", min_value=0, max_value=30, value=4)
#             duration = st.number_input("Project Expected Duration (Days)", min_value=1, max_value=365, value=60)
#         with col2:
#             tech_stack = st.selectbox("Tech Stack Domain", ["Fullstack Web", "Frontend React", "Backend Python", "Mobile App", "DevOps", "Data Engineering"])
#             budget = st.number_input("Total Proposed Contract Budget (₹)", min_value=1, value=45000)
            
#         submit_btn = st.form_submit_button("Run Delivery Risk Audit")
        
#     if submit_btn:
#         daily_rate = budget / duration
        
#         # --- Deep Business Logic Overrides & Guardrails ---
#         override_triggered = False
#         final_status = ""
#         alert_type = ""
#         risk_probability = 0.5 # Default fallback
        
#         # Rule 1: Exploitation Guardrail (< ₹400/day)
#         if daily_rate < 400:
#             override_triggered = True
#             final_status = "FAILED (Extreme Budget Risk)"
#             alert_type = "error"
#             risk_probability = 0.95 # Artificially spiked for the gauge map
#             st.error(f"🚨 **Exploitation Guardrail Triggered!** The daily payout rate works out to only ₹{daily_rate:.2f}/day (below standard baseline minimum threshold of ₹400). This contract is mathematically doomed to failure.")
            
#         # Rule 2: Talent Discount Exemption
#         elif experience >= 5 and budget < (duration * 600):
#             override_triggered = True
#             final_status = "PASSED WITH CAUTION"
#             alert_type = "warning"
#             risk_probability = 0.45
#             st.warning(f"⚠️ **Talent Discount Exemption Flagged:** The developer has robust seniority (>= 5 Years Exp) but is offering deep pricing optimization. Appraising project with strategic reservation.")
            
#         # --- Run ML Inference if no high priority overrides took precedence ---
#         if not override_triggered:
#             if not os.path.exists(MODEL_PATH):
#                 st.error("Missing trained model binary matrix! Please evaluate Step 3 in your notebook.")
#             else:
#                 with open(MODEL_PATH, "rb") as f:
#                     model = pickle.load(f)
                
#                 # Format raw operational arrays for Random Forest prediction
#                 features = np.array([[experience, duration, budget]])
#                 prediction = model.predict(features)[0]
#                 probabilities = model.predict_proba(features)[0]
#                 risk_probability = probabilities[1] # Chance of delivery risk
                
#                 if prediction == 1:
#                     final_status = "FAILED (High Risk Model Flag)"
#                     alert_type = "error"
#                 else:
#                     final_status = "PASSED"
#                     alert_type = "success"

#         # --- Output Scorecard Rendering ---
#         st.markdown("---")
#         st.subheader("🎯 Audit Evaluation Outcome")
        
#         if alert_type == "success":
#             st.success(f"💚 **Status: {final_status}**")
#         elif alert_type == "warning":
#             st.warning(f"🧡 **Status: {final_status}**")
#         else:
#             st.error(f"❤️ **Status: {final_status}**")
            
#         # Render horizontal dashboard gauges
#         fig = draw_gauge_dial(risk_probability)
#         st.pyplot(fig)
        
#         # Log insertion directly into localized SQLite3 Database
#         conn = sqlite3.connect(DB_PATH)
#         cursor = conn.cursor()
#         cursor.execute("""
#             INSERT INTO contract_audit_logs 
#             (developer_experience, tech_stack, duration_days, total_budget_inr, calculated_risk_score, final_prediction_status)
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, (experience, tech_stack, duration, budget, float(risk_probability), final_status))
#         conn.commit()
#         conn.close()
#         st.toast("Audit successfully cataloged in system ledger logs!")

# # ==============================================================================
# # TAB 2: SYSTEM DATABASE LOGS
# # ==============================================================================
# with tab_logs:
#     st.subheader("📜 Real-Time Audit Ledger (IST Timestamps)")
    
#     if not os.path.exists(DB_PATH):
#         st.info("Database empty or not yet populated. Perform an audit run above to initialize columns.")
#     else:
#         conn = sqlite3.connect(DB_PATH)
#         logs_df = pd.read_sql_query("SELECT * FROM contract_audit_logs ORDER BY id DESC", conn)
#         conn.close()
        
#         if logs_df.empty:
#             st.info("No logs present yet.")
#         else:
#             # Map UTC timestamps into Indian Standard Time (IST)
#             logs_df["timestamp_ist"] = logs_df["timestamp_utc"].apply(convert_utc_to_ist)
            
#             # Interactive Filter Dropdown Selection
#             filter_status = st.selectbox("Filter Ledger Distribution View", ["ALL", "PASSED", "FAILED"])
            
#             # Sub-segment rows based on criteria definitions
#             if filter_status == "PASSED":
#                 filtered_df = logs_df[logs_df["final_prediction_status"].str.contains("PASSED")]
#             elif filter_status == "FAILED":
#                 filtered_df = logs_df[logs_df["final_prediction_status"].str.contains("FAILED")]
#             else:
#                 filtered_df = logs_df
                
#             # Dynamic Matplotlib Distribution Trend Chart
#             st.markdown("#### Distribution Trend Chart")
#             if not filtered_df.empty:
#                 fig_bar, ax_bar = plt.subplots(figsize=(6, 2))
#                 status_counts = filtered_df["final_prediction_status"].value_counts()
#                 colors = ["#2ecc71" if "PASS" in idx else "#ff4d4d" for idx in status_counts.index]
#                 status_counts.plot(kind="barh", color=colors, ax=ax_bar)
#                 ax_bar.set_xlabel("Logged Transaction Frequency Count")
#                 plt.tight_layout()
#                 st.pyplot(fig_bar)
#             else:
#                 st.write("No distributions to display for selection criteria.")
                
#             # Clean Presentation Data Frame Table Ledger
#             st.markdown("#### Database Ledger Records")
#             display_cols = ["id", "timestamp_ist", "developer_experience", "tech_stack", "duration_days", "total_budget_inr", "calculated_risk_score", "final_prediction_status"]
#             st.dataframe(filtered_df[display_cols], use_container_width=True)

#             # version2


# """
# app.py (Upgraded Edition)
# Includes real-time ML feature engineering inference, complex guardrails,
# custom horizontal gauge dials, and database metrics monitoring Capital at Risk.
# """

# import os
# import sqlite3
# import pickle
# from datetime import datetime, timedelta
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import streamlit as st

# # --- Page Configuration ---
# st.set_page_config(page_title="Freelance Risk Engine Engine", layout="centered", page_icon="🔍")

# DB_PATH = "data/freelance.db"
# MODEL_PATH = "models/model.pkl"

# # --- Helper: Convert UTC string to IST Display String ---
# def convert_utc_to_ist(utc_str):
#     try:
#         utc_dt = datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S")
#         ist_dt = utc_dt + timedelta(hours=5, minutes=30)
#         return ist_dt.strftime("%d-%b-%Y %I:%M %p")
#     except Exception:
#         return utc_str

# # --- Helper: Draw Matplotlib Gauge Dial ---
# def draw_gauge_dial(score):
#     fig, ax = plt.subplots(figsize=(6, 1.3))
#     ax.axvspan(0, 40, color="#ff4d4d", alpha=0.9)   # Red: High Risk
#     ax.axvspan(40, 65, color="#ffcc00", alpha=0.9)  # Yellow: Caution
#     ax.axvspan(65, 100, color="#2ecc71", alpha=0.9) # Green: Safe Track
    
#     needle_pos = (1 - score) * 100
#     ax.axvline(x=needle_pos, color="black", linewidth=4)
#     ax.plot(needle_pos, 0.5, marker="v", color="black", markersize=12)
    
#     ax.set_xlim(0, 100)
#     ax.set_ylim(0, 1)
#     ax.set_yticks([])
#     ax.set_xticks([20, 52.5, 82.5])
#     ax.set_xticklabels(["High Risk", "Caution Zone", "Safe Track"], fontsize=9, fontweight='bold')
#     plt.tight_layout()
#     return fig

# # --- Main Core UI Layout ---
# st.title("🇮🇳 Advanced Freelance Contract Predictor & Auditor")
# st.markdown("Equipped with automated feature ratios and predictive data intelligence.")

# tab_audit, tab_logs = st.tabs(["🔍 Contract Risk Audit", "📜 System Database Logs"])

# # ==============================================================================
# # TAB 1: ADVANCED RISK AUDIT PANEL
# # ==============================================================================
# with tab_audit:
#     st.subheader("🛠️ Configure Contract Parameters")
    
#     with st.form("audit_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             experience = st.number_input("Developer Experience (Years)", min_value=0, max_value=30, value=4)
#             duration = st.number_input("Project Expected Duration (Days)", min_value=1, max_value=365, value=60)
#         with col2:
#             tech_stack = st.selectbox("Tech Stack Domain", ["Fullstack Web", "Frontend React", "Backend Python", "Mobile App", "DevOps", "Data Engineering"])
#             budget = st.number_input("Total Proposed Contract Budget (₹)", min_value=1, value=45000)
            
#         submit_btn = st.form_submit_button("Run Upgraded Risk Audit")
        
#     if submit_btn:
#         daily_rate = budget / duration
        
#         # 1. Compute Live Inference Ratios for the ML Brain
#         live_burn_rate = budget / duration
#         expected_market_rate = duration * (500 + (experience * 400))
#         live_buffer_ratio = budget / expected_market_rate
#         live_exp_density = experience / duration
        
#         override_triggered = False
#         final_status = ""
#         alert_type = ""
#         risk_probability = 0.5
        
#         # Enforcing Strict Business Rules & Guardrails
#         if daily_rate < 400:
#             override_triggered = True
#             final_status = "FAILED (Extreme Budget Risk)"
#             alert_type = "error"
#             risk_probability = 0.98
#             st.error(f"🚨 **Exploitation Guardrail Triggered!** Budget averages out to ₹{daily_rate:.2f}/day. Overriding ML prediction array.")
            
#         elif experience >= 5 and budget < (duration * 600):
#             override_triggered = True
#             final_status = "PASSED WITH CAUTION"
#             alert_type = "warning"
#             risk_probability = 0.42
#             st.warning(f"⚠️ **Talent Discount Exemption Flagged:** Experienced professional operating at optimized rates.")
            
#         # Run ML inference using the newly engineered columns
#         if not override_triggered:
#             if not os.path.exists(MODEL_PATH):
#                 st.error("Model array missing! Please run Phase A in your notebook cell.")
#             else:
#                 with open(MODEL_PATH, "rb") as f:
#                     model = pickle.load(f)
                
#                 # Input vector shape must match training shape exactly:
#                 # [experience, duration, budget, burn_rate, buffer_ratio, density]
#                 features = np.array([[experience, duration, budget, live_burn_rate, live_buffer_ratio, live_exp_density]])
#                 prediction = model.predict(features)[0]
#                 risk_probability = model.predict_proba(features)[0][1]
                
#                 if prediction == 1 or risk_probability > 0.5:
#                     final_status = "FAILED (High Risk Model Flag)"
#                     alert_type = "error"
#                 else:
#                     final_status = "PASSED"
#                     alert_type = "success"

#         # Output Rendering Panels
#         st.markdown("---")
#         st.subheader("🎯 Audit Evaluation Outcome")
        
#         if alert_type == "success":
#             st.success(f"💚 **Status: {final_status}**")
#         elif alert_type == "warning":
#             st.warning(f"🧡 **Status: {final_status}**")
#         else:
#             st.error(f"❤️ **Status: {final_status}**")
            
#         st.pyplot(draw_gauge_dial(risk_probability))
        
#         # Log metrics to DB
#         conn = sqlite3.connect(DB_PATH)
#         cursor = conn.cursor()
#         cursor.execute("""
#             INSERT INTO contract_audit_logs 
#             (developer_experience, tech_stack, duration_days, total_budget_inr, calculated_risk_score, final_prediction_status)
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, (experience, tech_stack, duration, budget, float(risk_probability), final_status))
#         conn.commit()
#         conn.close()
#         st.toast("Audit records written to system ledger.")

# # ==============================================================================
# # TAB 2: SYSTEM DATABASE LOGS WITH EXECUTIVE METRICS
# # ==============================================================================
# with tab_logs:
#     st.subheader("📊 Executive Portfolio Ledger Insights")
    
#     if not os.path.exists(DB_PATH):
#         st.info("Perform an initial audit to activate database metrics reporting features.")
#     else:
#         conn = sqlite3.connect(DB_PATH)
#         logs_df = pd.read_sql_query("SELECT * FROM contract_audit_logs ORDER BY id DESC", conn)
#         conn.close()
        
#         if logs_df.empty:
#             st.info("No transaction logs present.")
#         else:
#             logs_df["timestamp_ist"] = logs_df["timestamp_utc"].apply(convert_utc_to_ist)
            
#             # --- Executive Insight Scorecard Widgets ---
#             failed_mask = logs_df["final_prediction_status"].str.contains("FAILED")
#             capital_at_risk = logs_df[failed_mask]["total_budget_inr"].sum()
#             avg_duration = logs_df["duration_days"].mean()
#             total_audits = len(logs_df)
            
#             m1, m2, m3 = st.columns(3)
#             with m1:
#                 st.metric(label="Total Capital at Risk", value=f"₹{capital_at_risk:,.2f}", delta=f"{failed_mask.sum()} Projects", delta_color="inverse")
#             with m2:
#                 st.metric(label="Avg Project Run-rate", value=f"{avg_duration:.1f} Days")
#             with m3:
#                 st.metric(label="Total Audits Logged", value=total_audits)
                
#             st.markdown("---")
            
#             # Interactive Filters
#             filter_status = st.selectbox("Filter Ledger Distribution View", ["ALL", "PASSED", "FAILED"])
#             if filter_status == "PASSED":
#                 filtered_df = logs_df[logs_df["final_prediction_status"].str.contains("PASSED")]
#             elif filter_status == "FAILED":
#                 filtered_df = logs_df[failed_mask]
#             else:
#                 filtered_df = logs_df
                
#             # Distribution Trend Graph
#             st.markdown("#### Distribution Trend Chart")
#             if not filtered_df.empty:
#                 fig_bar, ax_bar = plt.subplots(figsize=(6, 2))
#                 status_counts = filtered_df["final_prediction_status"].value_counts()
#                 colors = ["#2ecc71" if "PASS" in idx else "#ff4d4d" for idx in status_counts.index]
#                 status_counts.plot(kind="barh", color=colors, ax=ax_bar)
#                 ax_bar.set_xlabel("Logged Transaction Frequency Count")
#                 plt.tight_layout()
#                 st.pyplot(fig_bar)
                
#             # Ledger Data Grid
#             st.markdown("#### Database Ledger Records")
#             display_cols = ["id", "timestamp_ist", "developer_experience", "tech_stack", "duration_days", "total_budget_inr", "calculated_risk_score", "final_prediction_status"]
#             st.dataframe(filtered_df[display_cols], use_container_width=True)

#version3


#streamlit code for website live



"""
app.py (Upgraded Frontend Edition)
Brings real-time feature engineering data breakdowns and analytical insights
directly onto the main Contract Risk Audit panel.
"""

import os
import sqlite3
import pickle
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# #streamlit
# import os
# import subprocess

# # 1. Cloud Database Guardrail: Initialize DB if missing
# if not os.path.exists("data/freelance.db"):
#     print("Cloud database missing. Initializing system ledger...")
#     subprocess.run(["python", "init_db.py"])

# # 2. Cloud Model Guardrail: Train ML Model if binary is missing
# if not os.path.exists("models/model.pkl"):
#     print("Cloud ML model binary missing. Training Random Forest ensemble...")
#     # Adjust this path if your script is inside src/
#     if os.path.exists("src/train_model.py"):
#         subprocess.run(["python", "src/train_model.py"])
#     elif os.path.exists("train_model.py"):
#         subprocess.run(["python", "train_model.py"])
#streamlit code 2
import os
import subprocess

# 🛑 SAFETY GUARDRAIL: Create folders if they don't exist in the cloud
if not os.path.exists("data"):
    os.makedirs("data")
    print("Created missing 'data' folder.")

if not os.path.exists("models"):
    os.makedirs("models")
    print("Created missing 'models' folder.")

# 1. Cloud Database Guardrail: Initialize DB if missing
if not os.path.exists("data/freelance.db"):
    print("Cloud database missing. Initializing system ledger...")
    subprocess.run(["python", "init_db.py"])

# 2. Cloud Model Guardrail: Train ML Model if binary is missing
if not os.path.exists("models/model.pkl"):
    print("Cloud ML model binary missing. Training Random Forest ensemble...")
    if os.path.exists("src/train_model.py"):
        subprocess.run(["python", "src/train_model.py"])
    elif os.path.exists("train_model.py"):
        subprocess.run(["python", "train_model.py"])

# --- Page Configuration ---
st.set_page_config(page_title="Freelance Risk Engine", layout="centered", page_icon="🔍")

DB_PATH = "data/freelance.db"
MODEL_PATH = "models/model.pkl"

def convert_utc_to_ist(utc_str):
    try:
        utc_dt = datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S")
        ist_dt = utc_dt + timedelta(hours=5, minutes=30)
        return ist_dt.strftime("%d-%b-%Y %I:%M %p")
    except Exception:
        return utc_str

def draw_gauge_dial(score):
    fig, ax = plt.subplots(figsize=(6, 1.1))
    ax.axvspan(0, 40, color="#ff4d4d", alpha=0.9)   # Red
    ax.axvspan(40, 65, color="#ffcc00", alpha=0.9)  # Yellow
    ax.axvspan(65, 100, color="#2ecc71", alpha=0.9) # Green
    
    needle_pos = (1 - score) * 100
    ax.axvline(x=needle_pos, color="black", linewidth=4)
    ax.plot(needle_pos, 0.5, marker="v", color="black", markersize=12)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xticks([20, 52.5, 82.5])
    ax.set_xticklabels(["High Risk", "Caution Zone", "Safe Track"], fontsize=9, fontweight='bold')
    plt.tight_layout()
    return fig

# --- Main Core UI Layout ---
st.title("🇮🇳 Advanced Freelance Contract Predictor & Auditor")
st.markdown("Equipped with automated feature ratios and predictive data intelligence.")

tab_audit, tab_logs = st.tabs(["🔍 Contract Risk Audit", "📜 System Database Logs"])

# ==============================================================================
# TAB 1: ADVANCED RISK AUDIT PANEL (WITH DIRECT FRONTEND INSIGHTS)
# ==============================================================================
with tab_audit:
    st.subheader("🛠️ Configure Contract Parameters")
    
    with st.form("audit_form"):
        col1, col2 = st.columns(2)
        with col1:
            experience = st.number_input("Developer Experience (Years)", min_value=0, max_value=30, value=4)
            duration = st.number_input("Project Expected Duration (Days)", min_value=1, max_value=365, value=60)
        with col2:
            tech_stack = st.selectbox("Tech Stack Domain", ["Fullstack Web", "Frontend React", "Backend Python", "Mobile App", "DevOps", "Data Engineering"])
            budget = st.number_input("Total Proposed Contract Budget (₹)", min_value=1, value=45000)
            
        submit_btn = st.form_submit_button("Run Upgraded Risk Audit")
        
    if submit_btn:
        daily_rate = budget / duration
        
        # Compute Live Inference Ratios
        live_burn_rate = budget / duration
        expected_market_rate = duration * (500 + (experience * 400))
        live_buffer_ratio = budget / expected_market_rate
        live_exp_density = experience / duration
        
        override_triggered = False
        final_status = ""
        alert_type = ""
        risk_probability = 0.5
        
        # Enforcing Guardrails
        if daily_rate < 400:
            override_triggered = True
            final_status = "FAILED (Extreme Budget Risk)"
            alert_type = "error"
            risk_probability = 0.98
            st.error(f"🚨 **Exploitation Guardrail Triggered!** Budget averages out to ₹{daily_rate:.2f}/day. Overriding ML prediction array.")
            
        elif experience >= 5 and budget < (duration * 600):
            override_triggered = True
            final_status = "PASSED WITH CAUTION"
            alert_type = "warning"
            risk_probability = 0.42
            st.warning(f"⚠️ **Talent Discount Exemption Flagged:** Experienced professional operating at optimized rates.")
            
        if not override_triggered:
            if not os.path.exists(MODEL_PATH):
                st.error("Model array missing! Please run Phase A in your notebook cell.")
            else:
                with open(MODEL_PATH, "rb") as f:
                    model = pickle.load(f)
                
                features = np.array([[experience, duration, budget, live_burn_rate, live_buffer_ratio, live_exp_density]])
                prediction = model.predict(features)[0]
                risk_probability = model.predict_proba(features)[0][1]
                
                if prediction == 1 or risk_probability > 0.5:
                    final_status = "FAILED (High Risk Model Flag)"
                    alert_type = "error"
                else:
                    final_status = "PASSED"
                    alert_type = "success"

        # --- Output Rendering & Dynamic Insights Right Here ---
        st.markdown("---")
        st.subheader("🎯 Audit Evaluation Outcome")
        
        if alert_type == "success":
            st.success(f"💚 **Status: {final_status}**")
        elif alert_type == "warning":
            st.warning(f"🧡 **Status: {final_status}**")
        else:
            st.error(f"❤️ **Status: {final_status}**")
            
        st.pyplot(draw_gauge_dial(risk_probability))
        
        # 🌟 NEW VISUAL INSIGHTS COLUMN SPLIT FOR THE AUDIT TAB 🌟
        st.markdown("#### 📊 Real-Time Parameter Analysis")
        ins_col1, ins_col2 = st.columns(2)
        
        with ins_col1:
            # Gauge calculation for budget health vs market expectations
            st.metric(
                label="Cost Efficiency Index (CEI)", 
                value=f"{live_buffer_ratio:.2f}x", 
                delta="Underpriced (Risky)" if live_buffer_ratio < 0.8 else "Healthy Budgeting" if live_buffer_ratio <= 1.3 else "Overpriced"
            )
            st.caption("Ratio of proposed budget against estimated standard market rates.")
            
        with ins_col2:
            st.metric(
                label="Daily Project Burn Velocity", 
                value=f"₹{live_burn_rate:,.2f}/day"
            )
            st.caption("Financial intensity requirement needed to hit this timeline.")
            
        # Contextual Interpretation
        st.markdown("##### 📝 Core Data Breakdown")
        st.info(
            f"Given a developer with **{experience} years** of experience working over **{duration} days**, "
            f"the ideal standard market allocation is approximately **₹{expected_market_rate:,.2f}**. "
            f"Your current proposal of **₹{budget:,.2f}** yields a timeline experience density score of **{live_exp_density:.3f}**. "
            f"The AI model maps these parameters to an overall delivery failure probability of **{risk_probability * 100:.1f}%**."
        )
        
        # Log metrics to DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contract_audit_logs 
            (developer_experience, tech_stack, duration_days, total_budget_inr, calculated_risk_score, final_prediction_status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (experience, tech_stack, duration, budget, float(risk_probability), final_status))
        conn.commit()
        conn.close()
        st.toast("Audit records written to system ledger.")

# ==============================================================================
# TAB 2: SYSTEM DATABASE LOGS
# ==============================================================================
with tab_logs:
    st.subheader("📊 Executive Portfolio Ledger Insights")
    if not os.path.exists(DB_PATH):
        st.info("Perform an initial audit to activate database metrics reporting features.")
    else:
        conn = sqlite3.connect(DB_PATH)
        logs_df = pd.read_sql_query("SELECT * FROM contract_audit_logs ORDER BY id DESC", conn)
        conn.close()
        
        if not logs_df.empty:
            logs_df["timestamp_ist"] = logs_df["timestamp_utc"].apply(convert_utc_to_ist)
            
            failed_mask = logs_df["final_prediction_status"].str.contains("FAILED")
            capital_at_risk = logs_df[failed_mask]["total_budget_inr"].sum()
            avg_duration = logs_df["duration_days"].mean()
            total_audits = len(logs_df)
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="Total Capital at Risk", value=f"₹{capital_at_risk:,.2f}", delta=f"{failed_mask.sum()} Projects", delta_color="inverse")
            with m2:
                st.metric(label="Avg Project Run-rate", value=f"{avg_duration:.1f} Days")
            with m3:
                st.metric(label="Total Audits Logged", value=total_audits)
                
            st.markdown("---")
            filter_status = st.selectbox("Filter Ledger Distribution View", ["ALL", "PASSED", "FAILED"])
            if filter_status == "PASSED":
                filtered_df = logs_df[logs_df["final_prediction_status"].str.contains("PASSED")]
            elif filter_status == "FAILED":
                filtered_df = logs_df[failed_mask]
            else:
                filtered_df = logs_df
                
            if not filtered_df.empty:
                fig_bar, ax_bar = plt.subplots(figsize=(6, 2))
                status_counts = filtered_df["final_prediction_status"].value_counts()
                colors = ["#2ecc71" if "PASS" in idx else "#ff4d4d" for idx in status_counts.index]
                status_counts.plot(kind="barh", color=colors, ax=ax_bar)
                plt.tight_layout()
                st.pyplot(fig_bar)
                
            st.dataframe(filtered_df[["id", "timestamp_ist", "developer_experience", "tech_stack", "duration_days", "total_budget_inr", "calculated_risk_score", "final_prediction_status"]], use_container_width=True)