import streamlit as st
import requests
import pandas as pd

API_URL = "http://backend:8000"

st.title("Loan and Salary Calculator")
st.sidebar.header("Select Calculator")
calculator_type = st.sidebar.selectbox(
    "Choose a calculator",
    ("Loan Calculator", "Salary Advance Calculator", "Compound Interest Calculator", "Salary Calculator")
)

if calculator_type == "Loan Calculator":
    st.subheader("Loan Payment Calculator")
    principal = st.number_input("Principal Amount", min_value=0, value=10000, step=1000)
    monthly_rate = st.number_input("Monthly Interest Rate (%)", min_value=0.0, value=1.0, step=0.1)
    months = st.number_input("Loan Term (Months)", min_value=1, value=12, step=1)
    
    if st.button("Calculate Loan Payment"):
        try:
            response = requests.get(
                f"{API_URL}/loan/",
                params={"principal": principal, "monthly_rate": monthly_rate, "months": months}
            )
            if response.status_code == 200:
                result = response.json()
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Monthly Payment", f"${result['monthly_payment']}")
                with col2:
                    st.metric("Total Payment", f"${result['total_payment']}")
                
                st.info(f"Total Interest: ${round(result['total_payment'] - principal, 2)}")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")

elif calculator_type == "Salary Advance Calculator":
    st.subheader("Salary Advance Eligibility")
    gross_salary = st.number_input("Gross Salary", min_value=0, value=5000, step=500)
    pay_frequency = st.selectbox(
        "Pay Frequency", 
        options=["weekly", "semi-monthly", "monthly"],
        format_func=lambda x: x.capitalize()
    )
    requested_amount = st.number_input("Requested Advance Amount", min_value=0, value=1000, step=100)
    
    if st.button("Check Eligibility"):
        try:
            response = requests.get(
                f"{API_URL}/advance/",
                params={
                    "gross_salary": gross_salary, 
                    "pay_frequency": pay_frequency,
                    "requested_amount": requested_amount
                }
            )
            if response.status_code == 200:
                result = response.json()
                if result["is_eligible"]:
                    st.success("You are eligible for this advance!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Monthly Salary", f"${result['monthly_salary']}")
                    with col2:
                        st.metric("Maximum Advance", f"${result['max_advance']}")

                    st.subheader("Advance Details")
                    st.info(f"Requested Amount: ${requested_amount}")
                    st.info(f"Total to Repay: ${result['total_repayment']}")
                else:
                    st.error("Not eligible for advance")
                    st.info(f"Reason: {result['reason']}")
                    st.info(f"Maximum allowed advance: ${result['max_advance']}")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")

if calculator_type == "Compound Interest Calculator":
    st.subheader("Compound Interest Calculator")
    principal = st.number_input("Principal Amount", min_value=0.0, value=1000.0, step=100.0)
    annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0, step=0.1)
    years = st.number_input("Loan Term (Years)", min_value=0.1, value=5.0, step=0.5)
    compounds_per_year = st.selectbox("Compounding Frequency", 
                                      options=[1, 2, 4, 12, 365],
                                      format_func=lambda x: {1: "Annually", 2: "Semi-annually", 
                                                           4: "Quarterly", 12: "Monthly", 
                                                           365: "Daily"}[x])

    if st.button("Calculate Compound Interest"):
        try:
            response = requests.get(
                f"{API_URL}/compound-interest/",
                params={"principal": principal, "annual_rate": annual_rate, "years": years, "compounds_per_year": compounds_per_year}
            )
            if response.status_code == 200:
                result = response.json()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Payment per Period", f"${result['payment_per_period']}")
                with col2:
                    st.metric("Total Payment", f"${result['total_payment']}")
                with col3:
                    st.metric("Total Interest", f"${result['total_interest']}")

                with st.expander("View Completion Schedule"):
                    schedule = pd.DataFrame(result['completion_schedule'])
                    display_schedule = schedule.copy()
                    for col in ['start_balance', 'payment', 'principal_payment', 
                               'interest_payment', 'end_balance']:
                        display_schedule[col] = display_schedule[col].apply(lambda x: f"${x:,.2f}")
                    
                    st.dataframe(display_schedule)

                    chart_data = schedule[['principal_payment', 'interest_payment']].cumsum()
                    st.line_chart(chart_data)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif calculator_type == "Salary Calculator":
    st.subheader("Salary Calculator")
    gross_salary = st.number_input("Gross Salary", step=100, min_value=1)
    st.info("Note: Gross Salary should be the total salary before tax deductions.")
    if st.button("Calculate Net Salary"):
        response = requests.get(
            f"{API_URL}/salary/",
            params={"gross_salary": gross_salary}
        )
        if response.status_code == 200:
            result = response.json()
            st.success(f"Net Salary: {result['net_salary']}")
            st.info(f"Tax Deducted: {result['tax']}")
        else:
            st.error("Failed to calculate salary")