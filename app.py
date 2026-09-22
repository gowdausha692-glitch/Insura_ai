import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="InsuraAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

THEMES = {
    "light": {
        "bg": "#EDF4F3",
        "surface": "rgba(255,255,255,0.86)",
        "surface_solid": "#FFFFFF",
        "line": "#D3E2E0",
        "text": "#0E2A33",
        "muted": "#5A7079",
        "ink": "#0E2A33",
        "teal": "#0E6E78",
        "teal_soft": "#6FB3B4",
        "amber": "#E19B2E",
        "clay": "#C4572F",
        "glow_a": "#67C6C0",
        "glow_b": "#F0C169",
        "glow_c": "#9FD8E8",
        "grid": "rgba(14,110,120,.10)",
        "pulse": "rgba(14,110,120,.30)",
        "shadow": "0 18px 40px -26px rgba(11,52,60,.55)",
        "grain": ".16",
        "sidebar": "#0E2A33",
        "sidebar_text": "#E7EFEE",
        "plot_grid": "rgba(14,110,120,.14)",
    },
    "dark": {
        "bg": "#06171D",
        "surface": "rgba(13,38,47,0.74)",
        "surface_solid": "#0D262F",
        "line": "#1C4653",
        "text": "#E6F1F0",
        "muted": "#8CA9AF",
        "ink": "#E8F2F1",
        "teal": "#4FC3C6",
        "teal_soft": "#2C7F87",
        "amber": "#F2B457",
        "clay": "#E57A4D",
        "glow_a": "#0E6E78",
        "glow_b": "#8A5E14",
        "glow_c": "#123C52",
        "grid": "rgba(120,220,224,.10)",
        "pulse": "rgba(79,195,198,.38)",
        "shadow": "0 22px 50px -30px rgba(0,0,0,.9)",
        "grain": ".10",
        "sidebar": "#041217",
        "sidebar_text": "#D6E7E6",
        "plot_grid": "rgba(120,220,224,.12)",
    },
}

if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("### 🛡️ InsuraAI")
    st.caption("Cover planning for Indian families")

    st.markdown("**☀ Daylight  /  ☾ Midnight**")
    if hasattr(st, "segmented_control"):
        # Streamlit >= 1.36
        choice = st.segmented_control(
            "Theme",
            ["☀ Daylight", "☾ Midnight"],
            default="☾ Midnight" if st.session_state.theme == "dark" else "☀ Daylight",
            label_visibility="collapsed",
        )
        st.session_state.theme = "dark" if choice == "☾ Midnight" else "light"
    elif hasattr(st, "toggle"):
        # Streamlit >= 1.26
        dark = st.toggle(
            "Switch to midnight mode",
            value=st.session_state.theme == "dark",
        )
        st.session_state.theme = "dark" if dark else "light"
    else:
        # Older Streamlit: no toggle widget, fall back to a checkbox
        dark = st.checkbox(
            "Switch to midnight mode",
            value=st.session_state.theme == "dark",
        )
        st.session_state.theme = "dark" if dark else "light"

T = THEMES[st.session_state.theme]

# Names used throughout the charts below.
INK = T["ink"]
TEAL = T["teal"]
TEAL_SOFT = T["teal_soft"]
AMBER = T["amber"]
CLAY = T["clay"]
MUTED = T["muted"]

RISK_COLORS = {"Low": T["teal_soft"], "Moderate": T["amber"], "High": T["clay"]}

# A shield made of contour lines, drawn once behind everything.
SHIELD_SVG = (
    "<svg class='contour' viewBox='0 0 1200 700' preserveAspectRatio='xMidYMin slice'>"
    "<path d='M600 40 L980 170 V420 Q980 600 600 690 Q220 600 220 420 V170 Z'/>"
    "<path d='M600 90 L930 200 V415 Q930 565 600 640 Q270 565 270 415 V200 Z'/>"
    "<path d='M600 140 L880 232 V410 Q880 530 600 592 Q320 530 320 410 V232 Z'/>"
    "<path d='M600 190 L830 264 V405 Q830 495 600 544 Q370 495 370 405 V264 Z'/>"
    "<path d='M600 240 L780 296 V400 Q780 460 600 496 Q420 460 420 400 V296 Z'/>"
    "</svg>"
)

PULSE_SVG = (
    "<svg class='pulse' viewBox='0 0 2800 220' preserveAspectRatio='none'>"
    "<path d='M0 110 H300 l26 -64 22 128 24 -110 26 60 H800 l30 -78 24 150 26 -128 28 74 "
    "H1500 l26 -64 22 128 24 -110 26 60 H2000 l30 -78 24 150 26 -128 28 74 H2800'/></svg>"
)

GRAIN = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' "
    "height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' "
    "baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='160' height='160' "
    "filter='url(%23n)' opacity='.55'/%3E%3C/svg%3E\")"
)

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap');

html, body, [class*="css"] {{ font-family:'IBM Plex Sans', system-ui, sans-serif; }}

.stApp {{ background:{T['bg']}; color:{T['text']}; }}
.block-container {{ padding-top:2rem; padding-bottom:4rem; max-width:1180px; position:relative; z-index:1; }}

h1,h2,h3,h4 {{ font-family:'Fraunces', Georgia, serif; color:{T['ink']}; }}
p, li, label, .stMarkdown {{ color:{T['text']}; }}

/* ---------------- background ---------------- */
.ia-bg {{ position:fixed; inset:0; z-index:0; overflow:hidden; pointer-events:none; }}
.ia-bg .bloom {{ position:absolute; border-radius:50%; filter:blur(90px); opacity:.5; }}
.ia-bg .a {{ width:60vw; height:60vw; left:-18vw; top:-22vw; background:{T['glow_a']};
             animation:iaDriftA 34s ease-in-out infinite alternate; }}
.ia-bg .b {{ width:46vw; height:46vw; right:-14vw; top:8vh; background:{T['glow_b']}; opacity:.34;
             animation:iaDriftB 42s ease-in-out infinite alternate; }}
.ia-bg .c {{ width:52vw; height:52vw; left:22vw; bottom:-28vw; background:{T['glow_c']}; opacity:.38;
             animation:iaDriftA 50s ease-in-out infinite alternate-reverse; }}
@keyframes iaDriftA {{ to {{ transform:translate3d(6vw,4vh,0) scale(1.12); }} }}
@keyframes iaDriftB {{ to {{ transform:translate3d(-5vw,6vh,0) scale(1.08); }} }}

.ia-bg .grid {{ position:absolute; inset:0;
  background-image:linear-gradient({T['grid']} 1px,transparent 1px),
                   linear-gradient(90deg,{T['grid']} 1px,transparent 1px);
  background-size:46px 46px;
  -webkit-mask-image:radial-gradient(ellipse 120% 70% at 50% 0%,#000 30%,transparent 78%);
          mask-image:radial-gradient(ellipse 120% 70% at 50% 0%,#000 30%,transparent 78%); }}

.ia-bg .contour {{ position:absolute; top:-6vh; left:50%; transform:translateX(-50%);
  width:min(1500px,150vw); opacity:.5; }}
.ia-bg .contour path {{ fill:none; stroke:{T['teal']}; stroke-width:1; opacity:.16; }}

.ia-bg .pulse {{ position:absolute; left:0; right:0; top:44vh; width:200%; height:220px; }}
.ia-bg .pulse path {{ fill:none; stroke:{T['pulse']}; stroke-width:2; stroke-linecap:round;
  stroke-dasharray:1400; stroke-dashoffset:1400; animation:iaTrace 9s linear infinite; }}
@keyframes iaTrace {{ to {{ stroke-dashoffset:-1400; }} }}

.ia-bg .grain {{ position:absolute; inset:-50%; opacity:{T['grain']}; mix-blend-mode:overlay;
  background-image:{GRAIN}; }}

@media (prefers-reduced-motion:reduce) {{
  .ia-bg .bloom, .ia-bg .pulse path {{ animation:none !important; }}
  .ia-bg .pulse path {{ stroke-dashoffset:0; stroke-dasharray:none; }}
}}

/* ---------------- masthead ---------------- */
.masthead {{display:flex;align-items:center;gap:16px;margin-bottom:26px;}}
.masthead .crest {{flex:none;}}
.masthead .name {{
    font-family:'Fraunces',Georgia,serif;
    font-size:58px;font-weight:800;
    color:{T['ink']};line-height:1;letter-spacing:-1.5px;
}}
.masthead .tag {{
    color:{T['muted']};font-size:19px;font-weight:600;
    margin-top:10px;max-width:65ch;line-height:1.5;
}}
.hero {{margin-top:45px;margin-bottom:35px;}}
.hero h1 {{font-family:'Fraunces',Georgia,serif;font-size:64px;font-weight:800;line-height:1.05;letter-spacing:-2px;color:{T['ink']};margin:0;}}
.hero h1 span {{color:{T['teal']};}}
.hero p {{color:{T['muted']};font-size:21px;font-weight:500;line-height:1.6;max-width:720px;margin-top:22px;}}

/* ---------------- surfaces ---------------- */
.section {{ font-family:'Fraunces',Georgia,serif; font-size:26px; font-weight:600;
  color:{T['ink']}; margin:34px 0 4px 0; }}
.section-note {{ color:{T['muted']}; font-size:14px; margin-bottom:14px; }}

.panel {{ background:{T['surface']}; backdrop-filter:blur(14px) saturate(1.2);
  border:1px solid {T['line']}; border-radius:6px; padding:20px 22px; height:100%;
  box-shadow:{T['shadow']}; }}
.panel .k {{ color:{T['muted']}; font-size:13px; }}
.panel .v {{ font-family:'Fraunces',Georgia,serif; font-size:30px; font-weight:600;
  color:{T['ink']}; margin-top:5px; line-height:1.1; }}
.panel .s {{ color:{T['muted']}; font-size:13px; margin-top:7px; }}
.panel-accent {{ border-top:3px solid {T['amber']}; }}
.panel-teal {{ border-top:3px solid {T['teal']}; }}

.note {{ background:{T['surface']}; backdrop-filter:blur(14px); border:1px solid {T['line']};
  border-left:3px solid {T['amber']}; border-radius:6px; padding:20px 22px;
  color:{T['text']}; line-height:1.65; box-shadow:{T['shadow']}; }}
.note .small {{ color:{T['muted']}; font-size:13px; margin-top:10px; }}

.steps .step {{ display:flex; gap:14px; padding:12px 0; border-bottom:1px solid {T['line']}; }}
.steps .step:last-child {{ border-bottom:none; }}
.steps .n {{ color:{T['teal']}; font-weight:600; min-width:22px; font-family:'IBM Plex Mono',monospace; }}
.steps .t {{ color:{T['ink']}; font-weight:600; }}
.steps .d {{ color:{T['muted']}; font-size:14px; }}

/* ---------------- widgets ---------------- */
div.stButton > button {{ background:{T['teal']}; color:{T['surface_solid']}; border:none;
  border-radius:3px; padding:10px 18px; font-weight:600; }}
div.stButton > button:hover {{ background:{T['ink']}; color:{T['bg']}; }}
div.stButton > button:focus-visible {{ outline:3px solid {T['amber']}; outline-offset:2px; }}

div[data-testid="stMetricValue"], .stSlider label, .stSelectbox label,
.stMultiSelect label, .stTextInput label, .stRadio label {{ color:{T['text']} !important; }}

div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input {{
  background:{T['surface_solid']} !important; border-color:{T['line']} !important;
  color:{T['text']} !important; }}

.stTabs [data-baseweb="tab-list"] {{ gap:22px; border-bottom:1px solid {T['line']}; }}
.stTabs [data-baseweb="tab"] {{ color:{T['muted']}; }}
.stTabs [aria-selected="true"] {{ color:{T['teal']}; }}

section[data-testid="stSidebar"] {{ background:{T['sidebar']}; }}
section[data-testid="stSidebar"] * {{ color:{T['sidebar_text']}; }}

/* Theme switch: force visible contrast no matter what wildcard rules apply above */
section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] label {{
  background:{T['surface_solid']} !important; border:1px solid {T['line']} !important; }}
section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] label p {{
  color:{T['ink']} !important; font-weight:600; }}
section[data-testid="stSidebar"] [aria-checked="true"][data-testid="stSegmentedControl"] label,
section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] label[data-checked="true"] {{
  background:{T['teal']} !important; }}
section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {{
  color:{T['sidebar_text']} !important; }}
section[data-testid="stSidebar"] div[data-baseweb="checkbox"] > div:first-child {{
  border-color:{T['amber']} !important; background:{T['surface_solid']} !important; }}
section[data-testid="stSidebar"] div[data-baseweb="checkbox"] svg {{ fill:{T['teal']} !important; }}

hr {{ border-color:{T['line']}; }}
.footer {{ color:{T['muted']}; font-size:13px; line-height:1.7; padding-top:14px; }}
</style>

<div class="ia-bg" aria-hidden="true">
  <div class="bloom a"></div><div class="bloom b"></div><div class="bloom c"></div>
  <div class="grid"></div>
  {SHIELD_SVG}
  {PULSE_SVG}
  <div class="grain"></div>
</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

FEATURES = ["Age", "BMI", "Family_Size", "Chronic", "Smoker", "Previous_Expense"]

LABELS = {
    "Age": "Age of main member",
    "BMI": "BMI",
    "Family_Size": "People covered",
    "Chronic": "Chronic condition",
    "Smoker": "Smoking",
    "Previous_Expense": "Past medical spend",
}


@st.cache_data
def build_dataset(n: int = 2000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    age = rng.integers(18, 75, n)
    bmi = np.round(rng.uniform(18, 38, n), 1)
    family_size = rng.integers(1, 7, n)
    chronic = rng.integers(0, 2, n)
    smoker = rng.integers(0, 2, n)
    previous_expense = rng.integers(5000, 120000, n)

    expense = (
        9000
        + age * 650
        + bmi * 450
        + family_size * 5000
        + chronic * 30000
        + smoker * 22000
        + previous_expense * 0.30
        + rng.normal(0, 9000, n)
    )
    expense = np.maximum(expense, 5000)

    score = (
        age * 0.04
        + bmi * 0.5
        + family_size * 1.2
        + chronic * 5
        + smoker * 4
        + previous_expense / 20000
    )
    risk = np.where(score < 12, "Low", np.where(score < 18, "Moderate", "High"))

    return pd.DataFrame(
        {
            "Age": age,
            "BMI": bmi,
            "Family_Size": family_size,
            "Chronic": chronic,
            "Smoker": smoker,
            "Previous_Expense": previous_expense,
            "Medical_Expense": expense,
            "Risk": risk,
        }
    )


@st.cache_resource(show_spinner="Training models…")
def train_models(df: pd.DataFrame):
    X = df[FEATURES]

    Xtr, Xte, ytr, yte = train_test_split(
        X, df["Medical_Expense"], test_size=0.2, random_state=42
    )
    reg = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    reg.fit(Xtr, ytr)
    reg_pred = reg.predict(Xte)

    encoder = LabelEncoder()
    y_cls = encoder.fit_transform(df["Risk"])
    Xtr2, Xte2, ytr2, yte2 = train_test_split(
        X, y_cls, test_size=0.2, random_state=42
    )
    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(Xtr2, ytr2)

    scores = {
        "mae": mean_absolute_error(yte, reg_pred),
        "r2": r2_score(yte, reg_pred),
        "accuracy": accuracy_score(yte2, clf.predict(Xte2)),
        "n_train": len(Xtr),
        "n_test": len(Xte),
    }
    return reg, clf, encoder, scores


df = build_dataset()
expense_model, risk_model, encoder, scores = train_models(df)

MEDIANS = df[FEATURES].median()


# ---------------------------------------------------------------------------
# Prediction helpers
# ---------------------------------------------------------------------------


def to_frame(age, bmi, family_size, chronic, smoker, previous_expense) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Age": age,
                "BMI": bmi,
                "Family_Size": family_size,
                "Chronic": int(chronic),
                "Smoker": int(smoker),
                "Previous_Expense": previous_expense,
            }
        ]
    )[FEATURES]


def predict_expense(row: pd.DataFrame) -> float:
    return float(expense_model.predict(row)[0])


def expense_range(row: pd.DataFrame, lo: int = 10, hi: int = 90):
    """Spread across the individual trees, used as a plain-English range."""
    tree_preds = np.array([t.predict(row.values)[0] for t in expense_model.estimators_])
    return float(np.percentile(tree_preds, lo)), float(np.percentile(tree_preds, hi))


def predict_risk(row: pd.DataFrame):
    probs = risk_model.predict_proba(row)[0]
    classes = encoder.inverse_transform(risk_model.classes_)
    band = classes[int(np.argmax(probs))]
    return band, dict(zip(classes, probs))


def factor_contributions(row: pd.DataFrame) -> pd.DataFrame:
   
    base = predict_expense(row)
    out = []

    for f in FEATURES:
        # Convert to float so Pandas can safely assign median values
        swapped = row.copy().astype(float)

        # Replace one factor with its median value
        swapped.loc[:, f] = float(MEDIANS[f])

        # Calculate effect
        new_prediction = predict_expense(swapped)

        out.append({
            "Factor": LABELS[f],
            "Effect": base - new_prediction
        })

    return pd.DataFrame(out).sort_values("Effect")

def coverage_for(expense: float) -> str:
    if expense < 50_000:
        return "₹5–10 lakh"
    if expense < 100_000:
        return "₹10–15 lakh"
    if expense < 150_000:
        return "₹15–20 lakh"
    return "₹20–25 lakh"


def rupees(x: float) -> str:
    return f"₹{x:,.0f}"


# ---------------------------------------------------------------------------
# Chart defaults
# ---------------------------------------------------------------------------


def style_chart(fig, height: int = 360):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=44, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans, sans-serif", color=T["text"], size=13),
        title=dict(font=dict(family="Fraunces, Georgia, serif", size=17, color=T["ink"])),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        hoverlabel=dict(
            bgcolor=T["surface_solid"],
            bordercolor=T["line"],
            font=dict(color=T["text"], family="IBM Plex Sans, sans-serif"),
        ),
    )
    fig.update_xaxes(gridcolor=T["plot_grid"], zeroline=False, linecolor=T["line"])
    fig.update_yaxes(gridcolor=T["plot_grid"], zeroline=False, linecolor=T["line"])
    return fig


# ---------------------------------------------------------------------------
# Shared assessment block (used by Overview and Plan your cover)
# ---------------------------------------------------------------------------


def render_assessment(prefix: str, defaults: dict, note_intro: str = ""):
    """
    Renders the live household controls, the three result panels, the
    contribution chart, the percentile histogram, and the scenario
    comparison. Returns the current inputs and prediction so the caller
    (e.g. the save-profile UI) can reuse them.
    """
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.slider("Age of main member", 18, 90, defaults["age"], key=f"{prefix}_age")
        chronic = st.toggle(
            "Diagnosed chronic condition", defaults["chronic"], key=f"{prefix}_chronic"
        )
    with c2:
        bmi = st.slider("BMI", 14.0, 50.0, defaults["bmi"], 0.1, key=f"{prefix}_bmi")
        smoker = st.toggle(
            "Someone covered smokes", defaults["smoker"], key=f"{prefix}_smoker"
        )
    with c3:
        family_size = st.slider(
            "People covered", 1, 10, defaults["family_size"], key=f"{prefix}_family"
        )
        previous_expense = st.slider(
            "Medical spend last year (₹)", 0, 300_000, defaults["previous_expense"],
            5_000, key=f"{prefix}_prev",
        )

    row = to_frame(age, bmi, family_size, chronic, smoker, previous_expense)
    expense = predict_expense(row)
    lo, hi = expense_range(row)
    band, band_probs = predict_risk(row)
    coverage = coverage_for(expense)

    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""<div class="panel panel-teal"><div class="k">Estimated annual spend</div>
            <div class="v">{rupees(expense)}</div>
            <div class="s">Most trees land between {rupees(lo)} and {rupees(hi)}</div></div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="panel panel-accent"><div class="k">Risk band</div>
            <div class="v">{band}</div>
            <div class="s">{band_probs[band]*100:.0f}% of trees agree</div></div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="panel panel-teal"><div class="k">Suggested sum insured</div>
            <div class="v">{coverage}</div>
            <div class="s">Rule of thumb from the estimate</div></div>""",
            unsafe_allow_html=True,
        )

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown(
            '<div class="section">What moved your estimate</div>', unsafe_allow_html=True
        )
        contrib = factor_contributions(row)
        fig = px.bar(
            contrib,
            x="Effect",
            y="Factor",
            orientation="h",
            color=np.where(contrib["Effect"] >= 0, "Raises", "Lowers"),
            color_discrete_map={"Raises": "#C4572F", "Lowers": TEAL},
            title="Rupees added or removed vs. a typical household",
        )
        fig.update_layout(legend_title_text="")
        st.plotly_chart(style_chart(fig, 330), use_container_width=True)

    with right:
        st.markdown('<div class="section">Where you sit</div>', unsafe_allow_html=True)
        pct = (df["Medical_Expense"] < expense).mean() * 100
        fig = px.histogram(
            df,
            x="Medical_Expense",
            nbins=45,
            title=f"Higher than {pct:.0f}% of households in the data",
            color_discrete_sequence=[TEAL_SOFT],
        )
        fig.add_vline(
            x=expense, line_color=AMBER, line_width=3,
            annotation_text="You", annotation_position="top",
        )
        fig.update_layout(yaxis_title="Households", xaxis_title="Annual spend (₹)")
        st.plotly_chart(style_chart(fig, 330), use_container_width=True)

    # --- Scenarios -----------------------------------------------------
    st.markdown('<div class="section">If something changed</div>', unsafe_allow_html=True)

    scenarios = {}
    if smoker:
        scenarios["No one smokes"] = to_frame(age, bmi, family_size, chronic, 0, previous_expense)
    if bmi > 25:
        scenarios["BMI at 24"] = to_frame(age, 24.0, family_size, chronic, smoker, previous_expense)
    if previous_expense > 20_000:
        scenarios["Quiet year, ₹10,000 spent"] = to_frame(
            age, bmi, family_size, chronic, smoker, 10_000
        )
    scenarios["Five years older"] = to_frame(
        min(age + 5, 90), bmi, family_size, chronic, smoker, previous_expense
    )
    scenarios["One more person covered"] = to_frame(
        age, bmi, min(family_size + 1, 10), chronic, smoker, previous_expense
    )

    rows = [{"Scenario": "Your answers now", "Estimate": expense, "Change": 0.0}]
    for name, scen_row in scenarios.items():
        value = predict_expense(scen_row)
        rows.append({"Scenario": name, "Estimate": value, "Change": value - expense})
    scen_df = pd.DataFrame(rows)

    fig = px.bar(
        scen_df,
        x="Estimate",
        y="Scenario",
        orientation="h",
        text=scen_df["Estimate"].map(rupees),
        color_discrete_sequence=[TEAL],
        title="Estimated annual spend under each scenario",
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="")
    st.plotly_chart(style_chart(fig, 300), use_container_width=True)

    # --- Plain explanation ---------------------------------------------
    drivers = []
    if age >= 50:
        drivers.append("the main member's age")
    if chronic:
        drivers.append("a chronic condition in the household")
    if smoker:
        drivers.append("smoking")
    if family_size >= 5:
        drivers.append("the number of people covered")
    if previous_expense >= 50_000:
        drivers.append("last year's medical spend")
    if bmi >= 30:
        drivers.append("BMI")

    if drivers:
        sentence = "The estimate is pushed up mainly by " + ", ".join(drivers[:-1])
        sentence += f" and {drivers[-1]}." if len(drivers) > 1 else f"{drivers[0]}."
        sentence = sentence.replace("by and", "by")
    else:
        sentence = (
            "Nothing in your answers stands out as a cost driver, so the estimate "
            "sits close to a typical household."
        )

    st.markdown(
        f"""<div class="note">{note_intro}<b>Reading your result.</b> {sentence}
        The suggested sum insured is a rule of thumb applied to the estimate, not a quote.
        What a policy actually pays depends on its terms, waiting periods, room-rent limits,
        sub-limits and exclusions.</div>""",
        unsafe_allow_html=True,
    )

    return {
        "age": age, "bmi": bmi, "family_size": family_size, "chronic": chronic,
        "smoker": smoker, "previous_expense": previous_expense,
        "expense": expense, "band": band, "coverage": coverage,
    }


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "saved" not in st.session_state:
    st.session_state.saved = []
if "chat" not in st.session_state:
    st.session_state.chat = []


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.divider()
    page = st.radio(
        "Go to",
        ["Overview", "Plan your cover", "Explore the data", "Ask a question"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(
        f"{len(df):,} synthetic households · "
        f"{scores['n_train']:,} used for training"
    )
    st.caption("Prototype. Estimates only, not financial advice.")


st.markdown(
    f"""
<div class="masthead">
  <svg class="crest" width="54" height="62" viewBox="0 0 42 48" fill="none">
    <path d="M21 2 L39 9 v18 c0 11-8 17-18 21C11 44 3 38 3 27V9Z"
          stroke="{TEAL}" stroke-width="2"/>
    <path d="M21 9 L33 13.5 v13c0 8-5.5 12.5-12 15.5-6.5-3-12-7.5-12-15.5v-13Z"
          fill="{TEAL}" opacity=".14"/>
    <path d="M9 26 h6 l3 -8 4 16 3 -10 2 4 h6" stroke="{AMBER}" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  <div>
    <div class="name">InsuraAI</div>
    <div class="tag">Know what a year of medical care could cost your family, and how much
    cover pays for it.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("""
<div class="hero">
<h1>Know the bill <span>before</span> the<br>hospital does.</h1>
<p>Describe your household once. See a year of likely medical spend, the sum insured that covers it, and exactly which answer moved the number.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

if page == "Overview":
    st.markdown(
        '<div class="section-note">Everything below updates the moment you move one of '
        'these — this is the same live estimate shown in the design preview.</div>',
        unsafe_allow_html=True,
    )

    render_assessment(
        "ov",
        defaults={
            "age": 42, "bmi": 27.9, "family_size": 5,
            "chronic": True, "smoker": False, "previous_expense": 84_000,
        },
    )

    st.markdown('<div class="section">How reliable is this</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""<div class="panel panel-teal"><div class="k">Typical error on unseen households</div>
            <div class="v">{rupees(scores['mae'])}</div>
            <div class="s">Average gap between estimate and actual</div></div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="panel panel-teal"><div class="k">Variation explained</div>
            <div class="v">{scores['r2']:.2f}</div>
            <div class="s">R² of the expense model</div></div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="panel panel-accent"><div class="k">Risk band agreement</div>
            <div class="v">{scores['accuracy']*100:.1f}%</div>
            <div class="s">Classifier vs. the rule-based band</div></div>""",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section">Where the numbers come from</div>', unsafe_allow_html=True)
    st.markdown(
        """<div class="note">
        The dataset here is generated, not collected. Ages, BMI and past spend are drawn
        independently at random, and expense is built from a fixed formula plus noise. That makes
        the app safe to demo and the model easy to check — but the relationships you see are the
        ones that were written in, so treat the charts as a demonstration of method rather than
        evidence about real households.
        <div class="small" style="margin-top:10px;">Swap in a real dataset with the same eight
        columns and everything downstream keeps working.</div></div>""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Plan your cover
# ---------------------------------------------------------------------------

elif page == "Plan your cover":
    st.markdown('<div class="section">Plan your cover</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-note">Everything updates as you change an answer. '
        'Nothing is stored unless you save it.</div>',
        unsafe_allow_html=True,
    )

    result = render_assessment(
        "plan",
        defaults={
            "age": 35, "bmi": 24.0, "family_size": 4,
            "chronic": False, "smoker": False, "previous_expense": 25_000,
        },
    )

    # --- Save and compare ----------------------------------------------
    st.markdown('<div class="section">Saved profiles</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        label = st.text_input(
            "Name this profile", value=f"Profile {len(st.session_state.saved) + 1}"
        )
    with c2:
        st.write("")
        if st.button("Save profile", use_container_width=True):
            st.session_state.saved.append(
                {
                    "Profile": label,
                    "Age": result["age"],
                    "BMI": result["bmi"],
                    "People": result["family_size"],
                    "Chronic": "Yes" if result["chronic"] else "No",
                    "Smoker": "Yes" if result["smoker"] else "No",
                    "Past spend": result["previous_expense"],
                    "Estimate": round(result["expense"]),
                    "Risk": result["band"],
                    "Cover": result["coverage"],
                }
            )
    with c3:
        st.write("")
        if st.button("Clear all", use_container_width=True):
            st.session_state.saved = []

    if st.session_state.saved:
        saved_df = pd.DataFrame(st.session_state.saved)
        st.dataframe(saved_df, use_container_width=True, hide_index=True)

        buffer = io.StringIO()
        saved_df.to_csv(buffer, index=False)
        st.download_button(
            "Download as CSV",
            buffer.getvalue(),
            file_name="insuraai_profiles.csv",
            mime="text/csv",
        )
    else:
        st.markdown(
            '<div class="note">No profiles saved yet. Save one, change an answer, '
            'then save again to compare them side by side.</div>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Explore the data
# ---------------------------------------------------------------------------

elif page == "Explore the data":
    st.markdown('<div class="section">Explore the data</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-note">Filter the households, then read the charts below.</div>',
        unsafe_allow_html=True,
    )

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        age_range = st.slider("Age", 18, 75, (18, 75))
    with f2:
        bands = st.multiselect(
            "Risk band", ["Low", "Moderate", "High"], default=["Low", "Moderate", "High"]
        )
    with f3:
        smoker_filter = st.selectbox("Smoking", ["All", "Smokers", "Non-smokers"])
    with f4:
        chronic_filter = st.selectbox("Chronic condition", ["All", "Yes", "No"])

    view = df[
        df["Age"].between(*age_range) & df["Risk"].isin(bands if bands else ["Low", "Moderate", "High"])
    ]
    if smoker_filter != "All":
        view = view[view["Smoker"] == (1 if smoker_filter == "Smokers" else 0)]
    if chronic_filter != "All":
        view = view[view["Chronic"] == (1 if chronic_filter == "Yes" else 0)]

    if view.empty:
        st.markdown(
            '<div class="note">No households match these filters. Widen the age range '
            'or add a risk band.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    m1, m2, m3, m4 = st.columns(4)
    for col, (k, v) in zip(
        [m1, m2, m3, m4],
        [
            ("Households shown", f"{len(view):,}"),
            ("Median spend", rupees(view["Medical_Expense"].median())),
            ("Top 10% spend above", rupees(view["Medical_Expense"].quantile(0.9))),
            ("High-risk share", f"{(view['Risk'] == 'High').mean()*100:.0f}%"),
        ],
    ):
        with col:
            st.markdown(
                f'<div class="panel"><div class="k">{k}</div><div class="v">{v}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("")
    tab1, tab2, tab3 = st.tabs(["Relationships", "Distributions", "Model"])

    with tab1:
        c1, c2 = st.columns([1, 1])
        with c1:
            x_var = st.selectbox(
                "Horizontal axis", ["Age", "BMI", "Family_Size", "Previous_Expense"]
            )
        with c2:
            color_var = st.selectbox("Colour by", ["Risk", "Smoker", "Chronic"])

        plot_df = view.copy()
        plot_df["Smoker"] = plot_df["Smoker"].map({1: "Smoker", 0: "Non-smoker"})
        plot_df["Chronic"] = plot_df["Chronic"].map({1: "Chronic", 0: "None"})

        fig = px.scatter(
            plot_df,
            x=x_var,
            y="Medical_Expense",
            color=color_var,
            opacity=0.55,
            color_discrete_map=RISK_COLORS if color_var == "Risk" else None,
            color_discrete_sequence=[TEAL, AMBER],
            title=f"{LABELS.get(x_var, x_var)} against annual spend",
            labels={"Medical_Expense": "Annual spend (₹)"},
        )

        # Overall trend line, computed with numpy so no extra dependency is needed.
        x_vals = plot_df[x_var].to_numpy(dtype=float)
        y_vals = plot_df["Medical_Expense"].to_numpy(dtype=float)
        slope, intercept = np.polyfit(x_vals, y_vals, 1)
        x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
        fig.add_trace(
            go.Scatter(
                x=x_line,
                y=slope * x_line + intercept,
                mode="lines",
                name="Overall trend",
                line=dict(color=INK, width=2.5, dash="dash"),
            )
        )
        st.plotly_chart(style_chart(fig, 430), use_container_width=True)

        corr = view[FEATURES + ["Medical_Expense"]].corr()
        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale=["#FFFFFF", TEAL_SOFT, TEAL],
            title="Correlation between the numeric columns",
        )
        st.plotly_chart(style_chart(fig, 430), use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.box(
                view,
                x="Risk",
                y="Medical_Expense",
                color="Risk",
                category_orders={"Risk": ["Low", "Moderate", "High"]},
                color_discrete_map=RISK_COLORS,
                points="outliers",
                title="Annual spend by risk band",
                labels={"Medical_Expense": "Annual spend (₹)"},
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(style_chart(fig), use_container_width=True)
        with c2:
            var = st.selectbox("Column", FEATURES + ["Medical_Expense"], index=6)
            fig = px.histogram(
                view, x=var, nbins=40, color_discrete_sequence=[TEAL_SOFT],
                title=f"Distribution of {LABELS.get(var, 'annual spend').lower()}",
            )
            fig.update_layout(yaxis_title="Households")
            st.plotly_chart(style_chart(fig), use_container_width=True)

        counts = view["Risk"].value_counts().reindex(["Low", "Moderate", "High"]).fillna(0)
        fig = px.bar(
            x=counts.index,
            y=counts.values,
            color=counts.index,
            color_discrete_map=RISK_COLORS,
            title="How many households fall in each band",
            labels={"x": "", "y": "Households"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_chart(fig, 300), use_container_width=True)

    with tab3:
        imp = (
            pd.DataFrame(
                {
                    "Factor": [LABELS[f] for f in FEATURES],
                    "Importance": expense_model.feature_importances_,
                }
            )
            .sort_values("Importance")
        )
        fig = px.bar(
            imp,
            x="Importance",
            y="Factor",
            orientation="h",
            color_discrete_sequence=[TEAL],
            title="What the expense model relies on across all households",
        )
        st.plotly_chart(style_chart(fig, 360), use_container_width=True)

        sample = df.sample(400, random_state=7)
        actual = sample["Medical_Expense"]
        predicted = expense_model.predict(sample[FEATURES])
        fig = px.scatter(
            x=actual,
            y=predicted,
            opacity=0.6,
            color_discrete_sequence=[TEAL_SOFT],
            labels={"x": "Actual spend (₹)", "y": "Predicted spend (₹)"},
            title="Predicted against actual, on 400 sampled households",
        )
        line = [min(actual.min(), predicted.min()), max(actual.max(), predicted.max())]
        fig.add_trace(
            go.Scatter(x=line, y=line, mode="lines", name="Perfect prediction",
                       line=dict(color=INK, dash="dash"))
        )
        st.plotly_chart(style_chart(fig, 400), use_container_width=True)

        st.markdown(
            f"""<div class="note">On households it never saw during training, the model is off by
            {rupees(scores['mae'])} on average and explains {scores['r2']:.0%} of the variation in
            spend. Points below the dashed line are households the model under-estimated.</div>""",
            unsafe_allow_html=True,
        )

    with st.expander("See the underlying rows"):
        st.dataframe(view.head(300), use_container_width=True, hide_index=True)
        buf = io.StringIO()
        view.to_csv(buf, index=False)
        st.download_button("Download filtered rows", buf.getvalue(), "insuraai_data.csv", "text/csv")


# ---------------------------------------------------------------------------
# Ask a question
# ---------------------------------------------------------------------------

elif page == "Ask a question":
    st.markdown('<div class="section">Ask a question</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-note">Plain-language explanations of common health '
        'insurance terms. Answers come from a fixed glossary, not a language model.</div>',
        unsafe_allow_html=True,
    )

    GLOSSARY = {
        ("family floater", "floater"): (
            "A family floater covers several members under one shared sum insured. If one member "
            "claims heavily in a year, that reduces what is left for everyone else. It is usually "
            "cheaper than separate policies for a young family, and less suitable once one member "
            "is much older or higher risk than the rest."
        ),
        ("waiting period", "waiting"): (
            "A waiting period is the stretch of time after buying a policy during which certain "
            "claims are not payable. Most policies have a short initial waiting period, a longer "
            "one for named conditions, and a separate one for pre-existing conditions. Check the "
            "length for anything already diagnosed in your household."
        ),
        ("sum insured", "cover amount", "coverage amount"): (
            "The sum insured is the maximum the insurer will pay for covered claims in a policy "
            "year. Costs above it come out of your pocket, so it is worth checking against what "
            "treatment actually costs at hospitals near you rather than against a round number."
        ),
        ("premium", "cost of policy"): (
            "The premium is what you pay to keep the policy running. It moves with age, sum "
            "insured, the number of people covered, the city you live in, declared conditions and "
            "any add-ons. A low premium often signals tighter limits elsewhere in the policy."
        ),
        ("room rent", "sub-limit", "sublimit"): (
            "Room-rent caps and sub-limits put a ceiling on specific parts of a claim, such as the "
            "daily room charge or a named procedure. Exceeding them can reduce the whole claim "
            "proportionally, not just the capped item."
        ),
        ("deductible", "co-pay", "copay"): (
            "A deductible is the amount you pay before the insurer starts paying. A co-pay is a "
            "fixed share of every claim that stays with you. Both lower the premium and raise "
            "what you pay when you actually claim."
        ),
        ("exclusion", "not covered"): (
            "Exclusions are the things a policy will never pay for. They vary by insurer and are "
            "listed in the policy wording, which is the document worth reading before the brochure."
        ),
        ("pre-existing", "preexisting"): (
            "A pre-existing condition is one diagnosed or treated before the policy started. "
            "These are usually covered only after a specified waiting period, and only if they "
            "were declared honestly at the time of buying."
        ),
        ("claim", "cashless", "reimbursement"): (
            "Cashless claims are settled directly with a network hospital. Reimbursement means you "
            "pay first and claim later with bills and discharge papers. Keeping originals and "
            "informing the insurer early makes either route smoother."
        ),
    }

    suggestions = [
        "What is a family floater?",
        "How do waiting periods work?",
        "What is a room rent sub-limit?",
        "Cashless or reimbursement?",
    ]
    cols = st.columns(len(suggestions))
    clicked = None
    for col, s in zip(cols, suggestions):
        with col:
            if st.button(s, use_container_width=True):
                clicked = s

    for turn in st.session_state.chat:
        with st.chat_message(turn["role"], avatar="🛡️" if turn["role"] == "assistant" else "🧑"):
            st.write(turn["content"])

    question = st.chat_input("Type a question about health insurance")
    question = question or clicked

    if question:
        st.session_state.chat.append({"role": "user", "content": question})
        q = question.lower()
        answer = next(
            (text for keys, text in GLOSSARY.items() if any(k in q for k in keys)),
            "That one is outside the glossary. Try asking about family floater policies, "
            "waiting periods, sum insured, premiums, room-rent sub-limits, deductibles and "
            "co-pays, exclusions, pre-existing conditions, or how claims are settled.",
        )
        st.session_state.chat.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat and st.button("Clear conversation"):
        st.session_state.chat = []
        st.rerun()


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.divider()
st.markdown(
    """<div class="footer">
    <b>InsuraAI</b> — a data science portfolio project.<br>
    Estimates come from a random forest trained on synthetic data. They are not medical,
    insurance or financial advice, and they are not a quote.
    </div>""",
    unsafe_allow_html=True,
)
