"""
Loan Risk Calculator
---------------------
Finance class project. Calculates standard credit ratios (current ratio,
DSCR, debt-to-assets, etc.) from basic company financials and outputs a
risk rating. Not a real underwriting tool.
"""

import streamlit as st

st.set_page_config(page_title="Loan Risk Calculator", layout="centered")

st.title("Loan Risk Calculator")
st.write("Enter company financials. Outputs standard credit ratios and a risk rating.")


def use_example_numbers():
    st.session_state.revenue = 500000.0
    st.session_state.net_income = 60000.0
    st.session_state.cash = 40000.0
    st.session_state.ar = 30000.0
    st.session_state.inventory = 20000.0
    st.session_state.current_liab = 50000.0
    st.session_state.total_assets = 400000.0
    st.session_state.total_liab = 180000.0
    st.session_state.op_cash_flow = 90000.0
    st.session_state.debt_payments = 60000.0
    st.session_state.loan_amount = 100000.0


st.button("Use example company", on_click=use_example_numbers)

st.write("---")

# --- inputs ---
st.write("**Company info**")

col1, col2 = st.columns(2)

with col1:
    annual_revenue = st.number_input("Annual revenue", min_value=0.0, key="revenue")
    net_income = st.number_input("Net income", key="net_income")
    annual_operating_cash_flow = st.number_input("Operating cash flow", key="op_cash_flow")
    annual_debt_payments = st.number_input("Annual debt payments", min_value=0.0, key="debt_payments")
    requested_loan_amount = st.number_input("Loan amount requested", min_value=0.0, key="loan_amount")

with col2:
    cash = st.number_input("Cash", min_value=0.0, key="cash")
    accounts_receivable = st.number_input("Accounts receivable", min_value=0.0, key="ar")
    inventory = st.number_input("Inventory", min_value=0.0, key="inventory")
    current_liabilities = st.number_input("Current liabilities", min_value=0.0, key="current_liab")
    total_assets = st.number_input("Total assets", min_value=0.0, key="total_assets")
    total_liabilities = st.number_input("Total liabilities", min_value=0.0, key="total_liab")

analyze_clicked = st.button("Run the numbers")

st.write("---")

# --- runs after the button is clicked ---
if analyze_clicked:

    # basic checks to avoid divide by zero
    errors = []
    if total_assets == 0:
        errors.append("Total assets can't be 0.")
    if current_liabilities == 0:
        errors.append("Current liabilities can't be 0.")
    if annual_debt_payments == 0:
        errors.append("Annual debt payments can't be 0.")
    if requested_loan_amount == 0:
        errors.append("Enter a loan amount.")

    if errors:
        st.write("Fix these first:")
        for e in errors:
            st.write("- " + e)
        st.stop()

    if annual_revenue == 0:
        st.write("Note: revenue is $0. Ratios below may not be meaningful.")

    # --- ratio calculations ---
    current_assets = cash + accounts_receivable + inventory

    net_working_capital = current_assets - current_liabilities
    current_ratio = current_assets / current_liabilities
    debt_to_assets_ratio = total_liabilities / total_assets
    dscr = annual_operating_cash_flow / annual_debt_payments
    loan_to_assets_pct = (requested_loan_amount / total_assets) * 100

    # --- risk scoring ---
    # simple point system: worse ratio, more points, higher risk
    points = 0
    good_signs = []
    concerns = []

    if current_ratio >= 1.5:
        good_signs.append("Current ratio above 1.5. Short-term assets cover current liabilities.")
    elif current_ratio >= 1.0:
        points += 1
        good_signs.append("Current ratio above 1.0. Current assets cover current liabilities.")
    else:
        points += 2
        concerns.append("Current ratio below 1.0. Current assets do not cover current liabilities.")

    if debt_to_assets_ratio <= 0.4:
        good_signs.append("Debt-to-assets under 40%. Low leverage.")
    elif debt_to_assets_ratio <= 0.6:
        points += 1
        concerns.append("Debt-to-assets between 40% and 60%. Moderate leverage.")
    else:
        points += 2
        concerns.append("Debt-to-assets above 60%. High leverage.")

    if dscr >= 1.25:
        good_signs.append("DSCR above 1.25. Cash flow comfortably covers debt payments.")
    elif dscr >= 1.0:
        points += 1
        good_signs.append("DSCR between 1.0 and 1.25. Debt payments covered, low margin.")
    else:
        points += 2
        concerns.append("DSCR below 1.0. Cash flow does not cover debt payments.")

    if loan_to_assets_pct <= 25:
        good_signs.append("Loan under 25% of total assets.")
    elif loan_to_assets_pct <= 50:
        points += 1
        concerns.append("Loan between 25% and 50% of total assets.")
    else:
        points += 2
        concerns.append("Loan exceeds 50% of total assets.")

    if net_working_capital < 0:
        points += 2
        concerns.append("Net working capital is negative.")
    else:
        good_signs.append("Net working capital is positive.")

    # convert score to a rating
 if points <= 2:
    risk_rating = "Low"
    risk_summary = "The company shows solid liquidity, manageable leverage, and enough cash flow to cover debt payments."
elif points <= 5:
    risk_rating = "Moderate"
    risk_summary = "The company has some positive signs, but one or more ratios need a closer look."
else:
    risk_rating = "High"
    risk_summary = "Several ratios suggest the company may have difficulty supporting additional debt."
    # --- output ---
    st.write(f"**Risk rating: {risk_rating}**")
    st.write(risk_summary)

    st.write("---")

    st.write("**Method**")
    st.write("Four factors: liquidity, leverage, debt coverage, and loan size relative to assets.")

    st.write("---")

    c1, c2 = st.columns(2)
    with c1:
        st.write("**Strengths**")
        if good_signs:
            for g in good_signs:
                st.write("- " + g)
        else:
            st.write("- None identified.")
    with c2:
        st.write("**Concerns**")
        if concerns:
            for c in concerns:
                st.write("- " + c)
        else:
            st.write("- None identified.")

    st.write("---")

    st.write("**Ratios**")

    st.write(f"Net working capital: ${net_working_capital:,.0f}")
    st.caption("Current assets minus current liabilities.")

    st.write(f"Current ratio: {current_ratio:.2f}")
    st.caption("Current assets divided by current liabilities.")

    st.write(f"Debt-to-assets: {debt_to_assets_ratio:.0%}")
    st.caption("Total liabilities divided by total assets.")

    st.write(f"DSCR: {dscr:.2f}")
    st.caption("Operating cash flow divided by annual debt payments.")

    st.write(f"Loan as % of assets: {loan_to_assets_pct:.1f}%")
    st.caption("Requested loan divided by total assets.")
