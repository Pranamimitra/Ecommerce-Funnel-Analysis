import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import graphviz

# ---------------------------
# Colour Palette
# ---------------------------
PRIMARY = "#4285F4"     # Google Blue
SECONDARY = "#FBBC05"   # Google Yellow
SUCCESS = "#34A853"     # Google Green
BACKGROUND = "#0E1117"

# Page configuration
st.set_page_config(
    page_title = "E-commerce Customer Conversion Funnel Analysis",
    page_icon = "🛒",
    layout = "wide"
)

#Load Data
overall = pd.read_csv("data/overall_funnel.csv")
weekday = pd.read_csv("data/weekday_conversion.csv")

#Title
st.title("🛒 E-commerce Conversion Funnel Analysis")
st.markdown("""### Objective

Analyse user behaviour across the e-commerce purchase funnel to identify
where customers drop off and uncover opportunities to improve conversion.
""")
st.caption(
    "Dataset: E-commerce Behaviour Data | Analysis Grain: Session Level"
)

#Sidebar
st.markdown("""
<style>

/* Sidebar */
[data-testid="stSidebar"]{
    background-color:#161B22;
}

/* Metric Cards */
[data-testid="stMetric"]{
    background-color:#1B222C;
    padding:15px;
    border-radius:10px;
    border:1px solid #30363D;
}

/* Main Container */
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title("Project Overview")

st.sidebar.markdown("""### Dataset
E-commerce Behaviour Data

### Tools Used
- SQL Server
- SQL
- Streamlit
- Pandas
- Plotly

### Analysis Level
Session-based Funnel Analysis
""")

#KPI Metrics
viewed = int(overall["sessions_viewed"][0])
carted = int(overall["sessions_carted"][0])
purchased = int(overall["sessions_purchased"][0])

view_to_purchase = overall["view_to_purchase_rate"][0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Sessions Viewed", f"{viewed:,}")
col2.metric("Sessions Carted", f"{carted:,}")
col3.metric("Sessions Purchased", f"{purchased:,}")
col4.metric("View → Purchase", f"{view_to_purchase:.2f}%")

st.divider()

funnel = pd.DataFrame({
    "Stage": [
        "Viewed",
        "Carted",
        "Purchased"
    ],
    "Sessions": [
        viewed, 
        carted, 
        purchased
    ]
})

fig = px.funnel(
    funnel,
    x="Sessions",
    y="Stage",
    title="Customer Conversion Funnel"
)
fig = go.Figure(go.Funnel(
    y=["Viewed", "Carted", "Purchased"],
    x=[viewed, carted, purchased],
    marker={
        "color": [
            "#3B82F6",   # Blue
            "#F59E0B",   # Orange
            "#10B981"    # Green
        ]
    }
))

fig.update_layout(
    template="plotly_dark",
    title="Customer Conversion Funnel",
    title_x=0.02,
    font=dict(size=14),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=40, b=10)
)
#st.plotly_chart(fig, use_container_width=True)

#Put Funnel and Metrics Side-by-Side

left, right = st.columns([3,2])

with left:
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Conversion Rates")

    st.metric(
        "View → Cart",
        f"{overall['view_to_cart_rate'][0]:.2f}%"
    )

    st.metric(
        "Cart → Purchase",
        f"{overall['cart_to_purchase_rate'][0]:.2f}%"
    )

    st.metric(
        "View → Purchase",
        f"{overall['view_to_purchase_rate'][0]:.2f}%"
    )
st.markdown("---")

st.caption(
    "Cart-to-purchase is the weakest stage of the funnel."
)

#Build the Day-of-Week Chart
colors = []

max_value = weekday["cart_to_purchase_rate"].max()

for value in weekday["cart_to_purchase_rate"]:
    if value == max_value:
        colors.append("#10B981")   # Green highlight
    else:
        colors.append("#3B82F6")   # Blue

fig_day = go.Figure()

fig_day.add_bar(
    x=weekday["DAYNAME"],
    y=weekday["cart_to_purchase_rate"],
    text=weekday["cart_to_purchase_rate"].round(1),
    textposition="outside",
    marker_color=colors
)

fig_day.update_layout(
    title="Cart → Purchase Conversion by Day of Week",
    xaxis_title="Day",
    yaxis_title="Conversion Rate(%)",
    template="plotly_dark"
)

st.plotly_chart(fig_day, use_container_width=True)

#Add an Insight Box
st.subheader("Key Business Insight")

st.success("""
### Cart-to-purchase represents the greatest optimisation opportunity.

Only **3.55%** of sessions that viewed a product resulted in a purchase.

Although the largest numerical drop occurs before customers reach the cart,
only **16.5%** of cart sessions convert into purchases.

Cart-to-purchase conversion peaks on **Monday (18.1%)** and **Tuesday (18.8%)**
before declining through the rest of the week, suggesting opportunities to
improve Cart-to-purchase completion during mid-week.
""")

#Recommendations
st.subheader("Business Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
**Reduce Cart Abandonment**

Target reminder emails and promotional offers
during Wednesday–Saturday.
""")

with col2:
    st.info("""
**Investigate Behaviour**

Analyse why Monday and Tuesday shoppers
complete purchases more frequently.
""")

with col3:
    st.info("""
**Improve Cart-to-purchase**

Review payment failures,
shipping costs and UX friction.
""")

st.divider()

st.subheader("Analysis Workflow")


# Create a Graphviz directed graph
dot = graphviz.Digraph()

# Force transparent background to adapt to light/dark themes
dot.attr(bgcolor='transparent')

# Set graph attributes for a clean, professional look
dot.attr(rankdir='LR')
dot.attr('node', shape='box', style='filled,rounded', color='#1E88E5', fillcolor='#E3F2FD', fontname='Helvetica', fontsize='12')
dot.attr('edge', color='#90A4AE', arrowhead='vee')

# Define nodes
dot.node('A', 'Raw Event Data')
dot.node('B', 'Data Cleaning &\nValidation\n(SQL Server)')
dot.node('C', 'Session-Level\nFunnel Creation')
dot.node('D', 'Conversion Rate\nAnalysis')
dot.node('E', 'Business Insights')
dot.node('F', 'Interactive\nDashboard\n(Streamlit)', fillcolor='#FFE0B2', color='#FB8C00')

# Connect the nodes
dot.edges(['AB', 'BC', 'CD', 'DE', 'EF'])

# Render the flowchart
st.graphviz_chart(dot)

st.divider()

st.caption(
    "Built using SQL Server • SQL • Python • Pandas • Plotly • Streamlit"
)

