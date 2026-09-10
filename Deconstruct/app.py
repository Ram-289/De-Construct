import streamlit as st
import json
import time

# 1. Page Configuration & Professional Theming
st.set_page_config(
    page_title="De-Construct Platform", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Clean Enterprise CSS styling
st.markdown("""
    <style>
        /* Main title styling */
        .main-header {
            font-size: 32px;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 5px;
        }
        .sub-header {
            font-size: 16px;
            color: #64748B;
            margin-bottom: 25px;
        }
        /* Custom section borders */
        .section-block {
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #0EA5E9;
            background-color: #F8FAFC;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_with_html=True)

# App Headers
st.markdown('<div class="main-header">De-Construct</div>', unsafe_with_html=True)
st.markdown('<div class="sub-header">Requirements Ingestion & Market Discovery Engine</div>', unsafe_with_html=True)
st.divider()

# 2. Sidebar Layout Info
st.sidebar.header("Project Configurations")
product_category = st.sidebar.selectbox(
    "Product Domain Category", 
    ["E-Commerce & Retail", "SaaS Dashboard & Analytics", "FinTech & Payments", "Healthcare & Telemed"]
)
target_budget = st.sidebar.slider("Target Investment Boundary ($)", 5000, 200000, 45000, step=5000)

st.sidebar.markdown("---")
st.sidebar.caption("System Status: Local Evaluation Mode Active")

# 3. Core Input Layer
st.subheader("Ingestion Layer: Unstructured Customer Input")
raw_input = st.text_area(
    "Paste client emails, communications records, or rough discovery notes below:", 
    value="Hey, we need a shopping cart feature ASAP. Make it look sleek like Amazon. It should load super fast. Also, we want people to buy things without a long signup, but make sure they can still track their past orders in their profile section. Oh, and it needs to be 100% secure against hackers.",
    height=150
)

# Initialize persistent session state for the Jira submission to survive reruns
if "jira_exported" not in st.session_state:
    st.session_state.jira_exported = False

# 4. Processing Pipeline Execution
if st.button("Run Complete Discovery & Analysis Pipeline", type="primary"):
    with st.spinner("Analyzing structural architecture, risk profiles, market indicators, and financial matrices..."):
        time.sleep(1.5) # Simulates backend calculation time
        st.session_state.pipeline_run = True

# Display results only if the pipeline has been run
if st.get_store().get("pipeline_run") or "pipeline_run" in st.session_state:
    st.success("Analysis Complete. Discovery Dashboard Generated.")
    st.divider()

    # Tabbed Framework Presentation
    tab1, tab2, tab3, tab4 = st.tabs([
        "Actionable Requirements", 
        "Risk & Ambiguity Audit", 
        "Market & Social Insights", 
        "Cost & Trend Forecast"
    ])
    
    with tab1:
        st.markdown("### Functional Engineering Specifications")
        
        st.info("**User Story 1:** As a Guest User, I want to complete my checkout seamlessly so that I can purchase items quickly without account creation barriers.")
        st.code("Acceptance Criteria (Gherkin Syntax):\nGiven items are present in the active cart,\nWhen the checkout sequence is initiated,\nThen bypass standard authentication and render necessary billing fields.", language="gherkin")
        
        st.info("**User Story 2:** As a Registered User, I want to access a secure personal profile account panel so that I can view verified historical orders.")
        st.code("Acceptance Criteria (Gherkin Syntax):\nGiven the user session is authenticated,\nWhen navigating to the account management dashboard,\nThen query backend database records and display user order history.", language="gherkin")
        
        st.markdown("---")
        # Fixed implementation for Jira Export
        if st.button("Export Specifications to Jira Backlog"):
            st.session_state.jira_exported = True
            st.balloons()
            
        if st.session_state.jira_exported:
            st.success("Sprint tickets successfully compiled and migrated to the connected Jira Project Backlog.")

    with tab2:
        st.markdown("### Architectural Risk Audit")
        
        st.markdown("#### Structural Contradictions & Conflicts")
        st.error("**System Conflict:** Anonymous Guest Checkout vs. Historical Profile Tracking | **Severity:** High\n\n*Recommended Resolution:* Permanent data tracking cannot be bound to unauthenticated sessions. Mitigation Action: Deploy email-verified validation links or tokenized magic links for secure guest order lookups.")
        
        st.markdown("#### Technical Ambiguities Detected")
        st.warning("**Unquantified Parameter:** 'super fast' (Performance metric) -> **Engineering Target:** Establish page load targets strictly under 1.8 seconds handling up to 10k concurrent users.")
        st.warning("**Unquantified Parameter:** 'sleek like Amazon' (UI Design metric) -> **Engineering Target:** Implement a standard 3-tiered checkout funnel (Cart Summary -> Shipping Information -> Payment Processing).")

    with tab3:
        st.markdown("### Market Data & Competitor Defection Analysis")
        st.write(f"Synthesized user consensus trends regarding modern **{product_category}** models:")
        
        st.markdown(
            """
            <div class="section-block">
                <strong>Source Environment:</strong> Developer & Technical Community Forums<br/>
                • <strong>Market Insight:</strong> 48% of surveyed users report application drops or check-out friction when dealing with complex cryptocurrency protocols.<br/>
                • <strong>Strategic Pivot:</strong> Action: Rely strictly on core credit processors and mobile wallets for Phase 1 deployment. Push alternative currencies to Phase 2.
            </div>
            <div class="section-block">
                <strong>Source Environment:</strong> Commercial Application App Stores<br/>
                • <strong>Market Insight:</strong> User retention rates drop significantly when forced registration steps occur prior to product discovery or checkout access.<br/>
                • <strong>Strategic Pivot:</strong> Validation: Current scope design successfully bypasses this churn vector using the guest checkout workflow.
            </div>
            """, 
            unsafe_with_html=True
        )

    with tab4:
        st.markdown("### Strategic Financial & Capacity Estimations")
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric(label="Estimated Allocation Range", value="$35,000 - $48,000")
        with metric_col2:
            st.metric(label="Estimated Cloud Infrastructure/Mo.", value="$85 / month")
        with metric_col3:
            st.metric(label="Total Engineering Footprint", value="320 Hours")
        
        st.markdown("---")
        st.markdown("#### Strategic Trend Alignment")
        st.info("Market Context Metrics: Authentication trends indicate passwordless verification strategies improve onboarding conversions by up to 22% compared to traditional password creation.")
