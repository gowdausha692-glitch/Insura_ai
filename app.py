```python
import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="InsuraAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SESSION STATE
# =========================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


# =========================================================
# THEME
# =========================================================

if st.session_state.dark_mode:

    BG = "#06171D"
    SURFACE = "#0D262F"
    TEXT = "#E6F1F0"
    MUTED = "#8CA9AF"
    LINE = "#1C4653"
    TEAL = "#4FC3C6"
    AMBER = "#F2B457"

else:

    BG = "#EDF4F3"
    SURFACE = "#FFFFFF"
    TEXT = "#0E2A33"
    MUTED = "#5A7079"
    LINE = "#D3E2E0"
    TEAL = "#0E6E78"
    AMBER = "#E19B2E"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap'
);

.stApp {{
    background:
        radial-gradient(
            circle at 8% 5%,
            rgba(103,198,192,.30),
            transparent 30%
        ),
        radial-gradient(
            circle at 92% 18%,
            rgba(240,193,105,.20),
            transparent 28%
        ),
        {BG};

    color: {TEXT};
}}

html, body, [class*="css"] {{
    font-family: 'IBM Plex Sans', sans-serif;
}}

h1, h2, h3, h4 {{
    font-family: 'Fraunces', Georgia, serif !important;
    color: {TEXT} !important;
}}

.block-container {{
    max-width: 1200px;
    padding-top: 25px;
    padding-bottom: 60px;
}}

/* ---------------- TOP BAR ---------------- */

.top-brand {{
    font-family: 'Fraunces', Georgia, serif;
    font-size: 30px;
    font-weight: 600;
    color: {TEXT};
}}

.top-sub {{
    color: {MUTED};
    font-size: 13px;
    margin-top: 3px;
}}

.theme-text {{
    color: {MUTED};
    font-size: 13px;
    text-align: right;
    padding-top: 8px;
}}

/* ---------------- HERO ---------------- */

.hero {{
    padding-top: 35px;
    padding-bottom: 20px;
}}

.hero-title {{
    font-family: 'Fraunces', Georgia, serif;
    font-size: clamp(38px, 5vw, 62px);
    font-weight: 600;
    line-height: 1.05;
    letter-spacing: -1px;
    color: {TEXT};
}}

.hero-title span {{
    color: {TEAL};
}}

.hero-text {{
    color: {MUTED};
    font-size: 18px;
    line-height: 1.6;
    max-width: 700px;
}}

/* ---------------- CARDS ---------------- */

.card {{
    background: {SURFACE};
    border: 1px solid {LINE};
    border-radius: 12px;
    padding: 22px;
    box-shadow: 0 15px 35px rgba(11,52,60,.10);
    margin-bottom: 16px;
}}

.metric-card {{
    background: {SURFACE};
    border: 1px solid {LINE};
    border-top: 4px solid {TEAL};
    border-radius: 10px;
    padding: 22px;
    min-height: 145px;
    box-shadow: 0 15px 35px rgba(11,52,60,.10);
}}

.metric-card.amber {{
    border-top-color: {AMBER};
}}

.metric-title {{
    color: {MUTED};
    font-size: 13px;
}}

.metric-value {{
    font-family: 'Fraunces', Georgia, serif;
    color: {TEXT};
    font-size: 31px;
    font-weight: 600;
    margin-top: 7px;
}}

.metric-sub {{
    color: {MUTED};
    font-size: 12px;
    margin-top: 8px;
}}

/* ---------------- SECTION ---------------- */

.section-title {{
    font-family: 'Fraunces', Georgia, serif;
    font-size: 27px;
    font-weight: 600;
    color: {TEXT};
    margin-top: 32px;
    margin-bottom: 5px;
}}

.section-note {{
    color: {MUTED};
    font-size: 14px;
    margin-bottom: 18px;
}}

/* ---------------- RESULT ---------------- */

.result-box {{
    background: linear-gradient(
        135deg,
        {TEAL},
        #123A46
    );

    color: white;
    padding: 30px;
    border-radius: 14px;
    margin-top: 25px;
    box-shadow: 0 18px 40px rgba(11,52,60,.20);
}}

.result-label {{
    font-size: 13px;
    opacity: .75;
    letter-spacing: 1px;
}}

.result-number {{
    font-family: 'Fraunces', Georgia, serif;
    font-size: 42px;
    font-weight: 600;
    margin-top: 5px;
}}

.result-line {{
    height: 1px;
    background: rgba(255,255,255,.25);
    margin: 18px 0;
}}

/* ---------------- RECOMMENDATION ---------------- */

.recommendation {{
    background: rgba(240,193,105,.16);
    border-left: 4px solid {AMBER};
    padding: 20px;
    border-radius: 8px;
    color: {TEXT};
    margin-top: 18px;
}}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {{
    background: {SURFACE};
    border-right: 1px solid {LINE};
}}

section[data-testid="stSidebar"] h2 {{
    color: {TEXT} !important;
}}

section[data-testid="stSidebar"] label {{
    color: {TEXT} !important;
}}

/* ---------------- BUTTON ---------------- */

div.stButton > button {{
    background: {TEAL};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
}}

div.stButton > button:hover {{
    background: #123A46;
    color: white;
}}

/* ---------------- FOOTER ---------------- */

.footer {{
    color: {MUTED};
    border-top: 1px solid {LINE};
    padding-top: 18px;
    margin-top: 45px;
    font-size: 13px;
    line-height: 1.7;
}}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# TOP BAR
# =========================================================

top_left, top_right = st.columns([5, 1])

with top_left:

    st.markdown(
        """
        <div class="top-brand">
            🛡️ InsuraAI
        </div>

        <div class="top-sub">
            Cover planning for Indian families
        </div>
        """,
        unsafe_allow_html=True
    )

with top_right:

    theme_label = "🌙 Midnight" if not st.session_state.dark_mode else "☀️ Daylight"

    if st.button(theme_label, key="theme_button"):

        st.session_state.dark_mode = not st.session_state.dark_mode

        st.rerun()


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            Know the bill <span>before</span><br>
            the hospital does.
        </div>

        <p class="hero-text">
            Describe your household once. See an estimated year of
            medical spending, understand your risk level, and explore
            an indicative insurance coverage range.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# SIDEBAR INPUTS
# =========================================================

st.sidebar.markdown("## 🏠 Your Household")

st.sidebar.write(
    "Enter your household information below."
)

st.sidebar.divider()


age = st.sidebar.slider(
    "Age of main member",
    min_value=18,
    max_value=90,
    value=42
)


bmi = st.sidebar.slider(
    "BMI",
    min_value=15.0,
    max_value=45.0,
    value=27.9,
    step=0.1
)


family_members = st.sidebar.number_input(
    "People covered",
    min_value=1,
    max_value=15,
    value=5
)


medical_spend = st.sidebar.number_input(
    "Medical spend last year (₹)",
    min_value=0,
    max_value=10000000,
    value=84000,
    step=5000
)


chronic_condition = st.sidebar.selectbox(
    "Chronic condition?",
    ["No", "Yes"]
)


smoking = st.sidebar.selectbox(
    "Someone smokes?",
    ["No", "Yes"]
)


income = st.sidebar.number_input(
    "Annual household income (₹)",
    min_value=100000,
    max_value=10000000,
    value=600000,
    step=25000
)


# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict_medical_expense(
    age,
    bmi,
    family_members,
    medical_spend,
    chronic_condition,
    smoking,
    income
):

    prediction = 40000

    # Age
    if age > 60:
        prediction += 25000

    elif age > 45:
        prediction += 15000

    elif age > 35:
        prediction += 7000

    # BMI
    if bmi >= 30:
        prediction += 10000

    elif bmi >= 25:
        prediction += 5000

    # Family members
    prediction += family_members * 8500

    # Previous medical spending
    prediction += medical_spend * 0.35

    # Chronic condition
    if chronic_condition == "Yes":
        prediction += 30000

    # Smoking
    if smoking == "Yes":
        prediction += 10000

    # Income
    if income < 400000:
        prediction -= 3000

    elif income > 1500000:
        prediction += 3000

    return max(prediction, 20000)


# =========================================================
# PREDICTION
# =========================================================

prediction = predict_medical_expense(
    age,
    bmi,
    family_members,
    medical_spend,
    chronic_condition,
    smoking,
    income
)


# =========================================================
# RISK LEVEL
# =========================================================

if prediction < 75000:

    risk = "Low"

elif prediction < 150000:

    risk = "Moderate"

else:

    risk = "High"


# =========================================================
# COVERAGE
# =========================================================

if prediction < 75000:

    coverage = "₹5–10 lakh"

elif prediction < 125000:

    coverage = "₹10–15 lakh"

elif prediction < 200000:

    coverage = "₹15–20 lakh"

else:

    coverage = "₹20–30 lakh"


# =========================================================
# MAIN METRICS
# =========================================================

st.markdown(
    '<div class="section-title">Your estimate</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-note">Your household information has been used to generate an estimate.</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                Estimated annual medical spend
            </div>

            <div class="metric-value">
                ₹{prediction:,.0f}
            </div>

            <div class="metric-sub">
                Estimated household expenditure
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card amber">

            <div class="metric-title">
                Risk band
            </div>

            <div class="metric-value">
                {risk}
            </div>

            <div class="metric-sub">
                Based on estimated annual spending
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                Suggested sum insured
            </div>

            <div class="metric-value">
                {coverage}
            </div>

            <div class="metric-sub">
                Indicative coverage range
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HOUSEHOLD SUMMARY
# =========================================================

st.markdown(
    '<div class="section-title">Your household</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-note">The prediction changes automatically when you change the sidebar inputs.</div>',
    unsafe_allow_html=True
)


c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(
        f"""
        <div class="card">
            <span style="color:{MUTED};font-size:13px;">
                Age of main member
            </span>

            <h2>{age}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="card">
            <span style="color:{MUTED};font-size:13px;">
                BMI
            </span>

            <h2>{bmi}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="card">
            <span style="color:{MUTED};font-size:13px;">
                People covered
            </span>

            <h2>{family_members}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FACTORS
# =========================================================

st.markdown(
    '<div class="section-title">What moved your estimate?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-note">Estimated contribution of each factor.</div>',
    unsafe_allow_html=True
)


factors = {

    "Previous medical spend":
        medical_spend * 0.35,

    "Chronic condition":
        30000 if chronic_condition == "Yes" else 0,

    "Family size":
        family_members * 8500,

    "Age":
        max(age - 30, 0) * 800,

    "BMI":
        max(bmi - 24, 0) * 1000,

    "Smoking":
        10000 if smoking == "Yes" else 0
}


factor_df = pd.DataFrame(
    {
        "Factor": list(factors.keys()),
        "Impact": list(factors.values())
    }
)

factor_df = factor_df.sort_values(
    "Impact",
    ascending=True
)

st.bar_chart(
    factor_df.set_index("Factor")
)


# =========================================================
# SCENARIOS
# =========================================================

st.markdown(
    '<div class="section-title">If something changed</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-note">Explore how individual changes affect the estimate.</div>',
    unsafe_allow_html=True
)


current = prediction


no_chronic = predict_medical_expense(
    age,
    bmi,
    family_members,
    medical_spend,
    "No",
    smoking,
    income
)


five_years_older = predict_medical_expense(
    age + 5,
    bmi,
    family_members,
    medical_spend,
    chronic_condition,
    smoking,
    income
)


one_more_person = predict_medical_expense(
    age,
    bmi,
    family_members + 1,
    medical_spend,
    chronic_condition,
    smoking,
    income
)


s1, s2, s3, s4 = st.columns(4)


with s1:

    st.metric(
        "Current",
        f"₹{current:,.0f}"
    )


with s2:

    st.metric(
        "No chronic condition",
        f"₹{no_chronic:,.0f}",
        f"₹{no_chronic-current:,.0f}"
    )


with s3:

    st.metric(
        "Five years older",
        f"₹{five_years_older:,.0f}",
        f"₹{five_years_older-current:,.0f}"
    )


with s4:

    st.metric(
        "One more person",
        f"₹{one_more_person:,.0f}",
        f"₹{one_more_person-current:,.0f}"
    )


# =========================================================
# FINAL RESULT
# =========================================================

st.markdown(
    f"""
    <div class="result-box">

        <div class="result-label">
            INSURAAI PREDICTION
        </div>

        <div class="result-number">
            ₹{prediction:,.0f}
        </div>

        <div>
            Estimated annual household medical expenditure
        </div>

        <div class="result-line"></div>

        <b>Risk band:</b> {risk}

        <br><br>

        <b>Suggested coverage:</b> {coverage}

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# EXPLANATION
# =========================================================

st.markdown(
    f"""
    <div class="recommendation">

        <b>💡 Reading your result</b>

        <br><br>

        The estimate is influenced by household size, previous medical
        expenditure, age, BMI, chronic conditions and smoking.

        <br><br>

        <b>Important:</b> This is an educational prediction/demo.
        It is not an insurance quote or financial advice.

        Actual policy coverage depends on the insurer's terms,
        waiting periods, exclusions, room-rent limits and sub-limits.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        <b>InsuraAI</b> — AI-assisted health insurance planning demo.

        <br>

        Estimates shown are illustrative and should not be treated
        as medical, insurance or financial advice.

    </div>
    """,
    unsafe_allow_html=True
)
```
