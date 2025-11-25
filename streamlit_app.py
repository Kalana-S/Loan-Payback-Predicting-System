import streamlit as st
import pickle

st.set_page_config(
    page_title="Loan Payback Prediction",
    layout="centered",
    page_icon="💰"
)

@st.cache_resource
def load_model():
    with open("model/catboost_credit_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

st.markdown(
    """
    <h1 style='text-align:center; color:#4CAF50;'>Loan Payback Prediction System</h1>
    <p style='text-align:center; font-size:16px; color:gray;'>
        Enter borrower details and get the predicted probability of full loan repayment.
    </p>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown("### 📝 Borrower Information")
    st.markdown(
        "<div style='padding:2px; border-radius:10px; background-color:#F7F7F7;'>",
        unsafe_allow_html=True
    )

    debt_to_income_ratio = st.number_input(
        "📊 Debt to Income Ratio",
        min_value=0.0, max_value=200.0, step=0.1
    )

    credit_score = st.number_input(
        "💳 Credit Score",
        min_value=300, max_value=850, step=1
    )

    employment_status = st.selectbox(
        "💼 Employment Status",
        ["Employed", "Unemployed", "Self-Employed", "Student", "Other"]
    )

    st.markdown("</div>", unsafe_allow_html=True)

credit_dti_interaction = credit_score / (debt_to_income_ratio + 1e-6)

if st.button("🔍 Predict Risk Score", use_container_width=True):

    features = [[
        debt_to_income_ratio,
        credit_score,
        employment_status,
        credit_dti_interaction
    ]]

    with st.spinner("Calculating probability..."):
        probability = model.predict_proba(features)[0][1]

    st.markdown("### 🎯 Prediction Result")

    st.progress(float(probability))

    st.subheader(f"Default Probability: **{probability:.4f}**")

    if probability > 0.5:
        st.success("✔ Borrower is likely to **repay the loan in full**.")
    else:
        st.error("⚠ Borrower may **struggle to repay the loan fully**.")
