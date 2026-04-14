import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Vendor Payment Decision - Pro", page_icon="💰")

st.title("Vendor Payment Decision - Advanced Financial Tool")

st.markdown("---")

# Inputs
st.subheader("📥 Input Section")

invoice_amount = st.number_input("Invoice Amount (₹)", min_value=0.0, step=1000.0)
discount_percent = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, step=0.5)
payment_days = st.number_input("Payment Due In (Days)", min_value=1, step=1)

bank_interest_rate = st.number_input("Bank Interest Rate (% p.a.)", min_value=0.0, max_value=100.0, step=0.5)

available_cash = st.number_input("Available Cash (₹)", min_value=0.0, step=1000.0)

st.markdown("---")

if invoice_amount > 0 and discount_percent > 0 and payment_days > 0:

    # Calculations
    discount_amount = invoice_amount * (discount_percent / 100)
    interest_earned = invoice_amount * (bank_interest_rate / 100) * (payment_days / 365)

    remaining_cash = available_cash - invoice_amount

    # Financial Comparison
    st.subheader("📊 Financial Comparison")

    col1, col2 = st.columns(2)
    col1.metric("Discount Earned (₹)", f"{discount_amount:,.2f}")
    col2.metric("Interest Earned if Delayed (₹)", f"{interest_earned:,.2f}")

    # Cash Flow
    st.markdown("### 💰 Cash Flow Impact")
    st.write(f"Remaining Cash After Early Payment: ₹{remaining_cash:,.2f}")

    if remaining_cash < 0:
        st.warning("⚠ Not enough cash. You may need borrowing.")

    # Decision
    st.markdown("### 🧠 Final Decision")

    if discount_amount > interest_earned:
        st.success("✔ Pay Early (Discount Benefit Higher)")
    else:
        st.error("✖ Delay Payment (Interest Benefit Higher)")

    # Break-even
    break_even_days = (discount_percent / 100 * 365) / (bank_interest_rate / 100)

    st.markdown("### 📍 Break-even Point")
    st.info(f"Break-even occurs at approximately {break_even_days:.1f} days")

    if payment_days < break_even_days:
        st.write("👉 Since actual payment days are LESS than break-even, early payment is better.")
    else:
        st.write("👉 Since actual payment days are MORE than break-even, delaying payment is better.")

    # Graph
    st.markdown("---")
    st.subheader("📈 Discount vs Interest Comparison")

    days_range = np.linspace(1, 120, 100)

    interest_curve = invoice_amount * (bank_interest_rate / 100) * (days_range / 365)
    discount_line = [discount_amount] * len(days_range)

    plt.figure()
    plt.plot(days_range, interest_curve, label="Interest Earned (Delay)")
    plt.plot(days_range, discount_line, linestyle='--', label="Discount Earned (Early)")

    plt.xlabel("Payment Days")
    plt.ylabel("Amount (₹)")
    plt.title("Early Payment vs Delayed Payment")

    plt.legend()

    st.pyplot(plt)

    # Bonus Insight (Reinvestment of Discount)
    extra_interest = discount_amount * (bank_interest_rate / 100) * (payment_days / 365)

    st.markdown("---")
    st.subheader("💡 Extra Insight (Reinvestment)")

    st.write(f"If the discount ₹{discount_amount:,.2f} is reinvested, it can earn additional ₹{extra_interest:,.2f}.")

    # Executive Summary
    st.markdown("---")
    st.subheader("📑 Executive Summary")

    decision = "Pay Early" if discount_amount > interest_earned else "Delay Payment"

    summary = f"""
    Early payment gives a discount of ₹{discount_amount:,.2f}.  
    Delayed payment allows earning ₹{interest_earned:,.2f} as interest.  

    Break-even occurs at {break_even_days:.1f} days.  

    Final decision: **{decision}**, based on higher financial benefit.
    """

    st.write(summary)