import streamlit as st
import pandas as pd


# 1. PAGE SETUP & STYLING


st.set_page_config(
    page_title="SafeX Solutions | Market Basket Analysis",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 26px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 2px;
    }

    .sub-title {
        font-size: 14px;
        color: #64748B;
        margin-bottom: 18px;
    }

    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🛒 SafeX Solutions — Market Basket Analysis Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Retail Cross-Sell Recommendations using Apriori Association Rules & Out-of-Sample Validation</div>',
    unsafe_allow_html=True
)


# 2. DATA LOADING



@st.cache_data
def load_data():
    try:
        df = pd.read_csv("safex_market_basket_recommendations.csv")
        return df

    except FileNotFoundError:
        st.error(
            "File 'safex_market_basket_recommendations.csv' was not found. "
            "Make sure it is in the same folder as app.py."
        )
        return pd.DataFrame()


df_rules = load_data()

if df_rules.empty:
    st.stop()

# Ensure numeric columns are numeric
numeric_columns = [
    "support",
    "confidence",
    "lift",
    "validation_confidence"
]

for col in numeric_columns:
    df_rules[col] = pd.to_numeric(df_rules[col], errors="coerce")

df_rules = df_rules.dropna(subset=numeric_columns)


# 3. SIDEBAR FILTERING


st.sidebar.header("Filter & Tuning Controls")

min_conf = st.sidebar.slider(
    "Minimum Training Confidence",
    min_value=0.1,
    max_value=1.0,
    value=0.3,
    step=0.05
)

min_lift = st.sidebar.slider(
    "Minimum Lift",
    min_value=1.0,
    max_value=20.0,
    value=5.0,
    step=0.5
)

filtered_rules = df_rules[
    (df_rules["confidence"] >= min_conf) &
    (df_rules["lift"] >= min_lift)
].sort_values(
    "lift",
    ascending=False
)


# 4. SUMMARY METRIC CARDS


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Active Rules",
    f"{len(filtered_rules)}"
)

col2.metric(
    "Peak Lift",
    f"{df_rules['lift'].max():.2f}x"
)

col3.metric(
    "Avg Train Confidence",
    (
        f"{filtered_rules['confidence'].mean() * 100:.1f}%"
        if len(filtered_rules) > 0
        else "0%"
    )
)

col4.metric(
    "Avg Validation Confidence",
    (
        f"{filtered_rules['validation_confidence'].mean() * 100:.1f}%"
        if len(filtered_rules) > 0
        else "0%"
    )
)

st.divider()


# 5. TAB INTERFACE


tab1, tab2, tab3 = st.tabs([
    "🛍️ Interactive Cart Simulator",
    "📊 Association Rules",
    "💡 Business Implementation"
])


# TAB 1 — INTERACTIVE CART SIMULATOR


with tab1:

    st.subheader("Simulate E-Commerce Checkout Cross-Sell")

    st.write(
        "Select a product currently in a customer's cart to view "
        "cross-sell recommendations based on the discovered association rules."
    )

    unique_antecedents = sorted(
        df_rules["antecedents"].dropna().unique().tolist()
    )

    selected_item = st.selectbox(
        "Customer's In-Cart Item:",
        unique_antecedents
    )

    recs = filtered_rules[
        filtered_rules["antecedents"] == selected_item
    ].sort_values(
        "lift",
        ascending=False
    )

    if len(recs) > 0:

        st.markdown(
            f"### Recommended Additions for **{selected_item}**"
        )

        for _, row in recs.iterrows():

            with st.container():

                r1, r2, r3, r4 = st.columns([3, 1, 1, 1])

                r1.markdown(
                    f"**➕ {row['consequents']}**"
                )

                r2.metric(
                    "Train Confidence",
                    f"{row['confidence'] * 100:.1f}%"
                )

                r3.metric(
                    "Lift",
                    f"{row['lift']:.2f}x"
                )

                r4.metric(
                    "Validation Confidence",
                    f"{row['validation_confidence'] * 100:.1f}%"
                )

    else:

        st.warning(
            "No cross-sell recommendations meet the current "
            "Confidence and Lift thresholds for this item."
        )


# TAB 2 — ALL ASSOCIATION RULES


with tab2:

    st.subheader("Discovered Association Rules")

    st.write(
        "Rules are ranked by lift. Training confidence shows the strength "
        "of the relationship in the training data, while validation confidence "
        "shows how consistently the rule performed on unseen transactions."
    )

    display_df = filtered_rules.copy()

    display_df["support"] = display_df["support"].apply(
        lambda x: f"{x * 100:.2f}%"
    )

    display_df["confidence"] = display_df["confidence"].apply(
        lambda x: f"{x * 100:.1f}%"
    )

    display_df["lift"] = display_df["lift"].apply(
        lambda x: f"{x:.2f}x"
    )

    display_df["validation_confidence"] = display_df[
        "validation_confidence"
    ].apply(
        lambda x: f"{x * 100:.1f}%"
    )

    display_df.columns = [
        "In-Cart Item (Antecedent)",
        "Recommended Cross-Sell (Consequent)",
        "Support",
        "Train Confidence",
        "Lift",
        "Validation Confidence"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# TAB 3 — BUSINESS IMPLEMENTATION


with tab3:

    st.subheader("Business Applications")

    c1, c2 = st.columns(2)

    with c1:

        st.info("""
        #### 1. E-Commerce Cross-Selling

        **Regency Teacup Association:** Customers who purchase
        `PINK REGENCY TEACUP AND SAUCER` have an **83.3% training
        confidence** of also purchasing `GREEN REGENCY TEACUP AND SAUCER`.

        **Action:** Recommend related Regency Teacup products during
        checkout to encourage cross-selling and bundle purchases.
        """)

    with c2:

        st.success("""
        #### 2. Product Placement & Inventory Planning

        **Strong Product Associations:** High-lift product pairs,
        such as Regency Teacup and Lunch Bag variations, indicate
        strong purchasing relationships.

        **Action:** These associations can help retailers explore
        related product placement, promotional bundles, and
        inventory planning.
        """)

    st.divider()

    st.markdown("### Key Business Takeaways")

    st.markdown("""
    - **High confidence** indicates that customers frequently purchase
      the consequent product when the antecedent is present.
    - **High lift** indicates a stronger-than-random relationship between
      the products.
    - **Validation confidence** helps determine whether discovered rules
      remain useful on unseen transactions.
    - These associations can support **cross-selling, bundle creation,
      product placement, and inventory planning**.
    """)

