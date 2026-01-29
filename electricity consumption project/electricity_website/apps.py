import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Electricity Consumption Analyzer", layout="centered")

st.title("🔌 Electricity Consumption Analyzer (Multi-Appliance)")
st.write("Add multiple appliances and compare electricity consumption.")

# Initialize session state
if "appliances" not in st.session_state:
    st.session_state.appliances = []

# User Inputs
st.subheader("➕ Add Appliance")

appliance = st.text_input("Appliance Name")
power = st.number_input("Power Rating (Watts)", min_value=1)
hours = st.slider("Usage Hours per Day", 1, 24, 1)
days = st.number_input("Number of Days Used", min_value=1, max_value=31, value=30)
rate = st.number_input("Electricity Rate (₹ per unit)", min_value=1.0, value=8.0)

# Add Appliance Button
if st.button("Add Appliance"):
    daily_units = np.round((power * hours) / 1000, 2)
    total_units = np.round(daily_units * days, 2)
    cost = np.round(total_units * rate, 2)

    st.session_state.appliances.append({
        "Appliance": appliance,
        "Power (W)": power,
        "Hours/Day": hours,
        "Days": days,
        "Units (kWh)": total_units,
        "Cost (₹)": cost
    })

    st.success(f"{appliance} added successfully!")

# Show Appliances Table
if st.session_state.appliances:
    df = pd.DataFrame(st.session_state.appliances)

    st.subheader("📋 Appliance List")
    st.dataframe(df)

    # Calculate & Compare
    if st.button("Calculate & Compare"):
        total_units = df["Units (kWh)"].sum()
        total_cost = df["Cost (₹)"].sum()

        st.subheader("📊 Total Consumption")
        st.success(f"Total Units Consumed: {total_units} kWh")
        st.success(f"Total Estimated Cost: ₹ {total_cost}")

        # Bar Chart
        st.subheader("📈 Appliance-wise Consumption Comparison")
        fig1, ax1 = plt.subplots()
        ax1.bar(df["Appliance"], df["Units (kWh)"])
        ax1.set_xlabel("Appliance")
        ax1.set_ylabel("Units (kWh)")
        st.pyplot(fig1)

        # Pie Chart
        st.subheader("🥧 Consumption Distribution")
        fig2, ax2 = plt.subplots()
        ax2.pie(df["Units (kWh)"], labels=df["Appliance"], autopct='%1.1f%%')
        st.pyplot(fig2)

        # Energy Tips
        st.subheader("💡 Energy Saving Tips")
        st.write("""
        - Appliances with higher bars consume more electricity  
        - Reduce usage of high-consuming appliances  
        - Replace old appliances with energy-efficient ones  
        - Monitor total consumption regularly  
        """)

# Clear Button
if st.button("Clear All Data"):
    st.session_state.appliances = []
    st.warning("All appliance data cleared.")

# Footer
st.markdown("---")
st.caption("Independent Project | Streamlit + Pandas + NumPy + Matplotlib")
