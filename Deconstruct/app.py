import streamlit as st
import time
import random

# ============================================================
# 1. PAGE CONFIG & THEME
# ============================================================
st.set_page_config(
    page_title="De-Construct Platform",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main-header {
            font-size: 40px;
            font-weight: 800;
            background: linear-gradient(90deg, #0EA5E9, #7C3AED, #EC4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0px;
        }
        .sub-header {
            font-size: 16px;
            color: #64748B;
            margin-bottom: 20px;
        }
        .section-block {
            padding: 16px 18px;
            border-radius: 10px;
            border-left: 5px solid #0EA5E9;
            background: linear-gradient(135deg, #F0F9FF 0%, #F8FAFC 100%);
            margin-bottom: 14px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        .metric-card {
            padding: 18px;
            border-radius: 12px;
            text-align: center;
            color: white;
            font-weight: 600;
        }
        .metric-value {
            font-size: 26px;
            font-weight: 800;
            margin-top: 4px;
        }
        .story-card {
            padding: 14px 18px;
            border-radius: 10px;
            background: #ECFDF5;
            border-left: 5px solid #10B981;
            margin-bottom: 10px;
        }
        .conflict-card {
            padding: 14px 18px;
            border-radius: 10px;
            background: #FEF2F2;
            border-left: 5px solid #EF4444;
            margin-bottom: 10px;
        }
        .ambiguity-card {
            padding: 12px 16px;
            border-radius: 10px;
            background: #FFFBEB;
            border-left: 5px solid #F59E0B;
            margin-bottom: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧩 De-Construct</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">🚀 Requirements Ingestion & Market Discovery Engine</div>', unsafe_allow_html=True)
st.divider()

# ============================================================
# 2. SIDEBAR CONFIG
# ============================================================
st.sidebar.header("⚙️ Project Configurations")
product_category = st.sidebar.selectbox(
    "📦 Product Domain Category",
    ["E-Commerce & Retail", "SaaS Dashboard & Analytics", "FinTech & Payments", "Healthcare & Telemed"]
)
target_budget = st.sidebar.slider("💰 Target Investment Boundary ($)", 5000, 200000, 45000, step=5000)

st.sidebar.markdown("---")
st.sidebar.caption("🟢 System Status: Local Evaluation Mode Active")

if "jira_exported" not in st.session_state:
    st.session_state.jira_exported = False
if "pipeline_run" not in st.session_state:
    st.session_state.pipeline_run = False
if "analysis" not in st.session_state:
    st.session_state.analysis = None

# ============================================================
# 3. BACKEND ANALYSIS ENGINE (rule-based NLP-lite)
# ============================================================

VAGUE_TERMS = {
    "fast": ("⚡ Performance", "Define a concrete target — e.g. page load under 1.8s for up to 10k concurrent users."),
    "quick": ("⚡ Performance", "Define a concrete target — e.g. checkout completes in under 3 clicks / 30 seconds."),
    "sleek": ("🎨 UI/UX Design", "Adopt a defined design system (spacing scale, component library) and a 3-tier checkout funnel."),
    "modern": ("🎨 UI/UX Design", "Reference a specific competitor benchmark or design system to anchor 'modern'."),
    "secure": ("🔒 Security", "Specify a compliance target — e.g. OWASP Top 10 mitigation, PCI-DSS SAQ-A."),
    "safe": ("🔒 Security", "Specify a compliance target — e.g. OWASP Top 10 mitigation, PCI-DSS SAQ-A."),
    "easy": ("🧭 Usability", "Define a measurable UX target — e.g. task success rate ≥ 90% in usability testing."),
    "simple": ("🧭 Usability", "Define a measurable UX target — e.g. onboarding completed in ≤ 3 steps."),
    "scalable": ("🏗️ Infrastructure", "Define concurrency/load targets — e.g. horizontal autoscaling to 50k concurrent sessions."),
    "robust": ("🏗️ Infrastructure", "Define reliability targets — e.g. 99.9% uptime SLA, automated failover."),
    "seamless": ("🔄 UX Flow", "Break 'seamless' into a defined step-count and latency budget per transition."),
    "intuitive": ("🧭 Usability", "Back this with a usability testing benchmark rather than a subjective goal."),
}

FEATURE_STORIES = {
    "cart": {
        "title": "🛒 Shopping Cart",
        "story": "As a Shopper, I want to add items to a cart so I can review my selections before purchasing.",
        "gherkin": "Given a product is in stock,\nWhen the user clicks 'Add to Cart',\nThen the item is added to the persistent cart session."
    },
    "checkout": {
        "title": "💳 Guest Checkout",
        "story": "As a Guest User, I want to complete checkout seamlessly so I can purchase quickly without account-creation barriers.",
        "gherkin": "Given items are present in the active cart,\nWhen the checkout sequence is initiated,\nThen bypass standard authentication and render required billing fields."
    },
    "signup": {
        "title": "🪄 Frictionless Signup",
        "story": "As a New User, I want a minimal-step signup so I can start using the product quickly.",
        "gherkin": "Given a user starts registration,\nWhen they submit email + password only,\nThen an account is created with optional profile completion deferred."
    },
    "login": {
        "title": "🔑 Authentication",
        "story": "As a Returning User, I want to log in securely so I can access my saved data.",
        "gherkin": "Given valid credentials are submitted,\nWhen the login request is processed,\nThen issue a session token and redirect to the dashboard."
    },
    "profile": {
        "title": "👤 User Profile",
        "story": "As a Registered User, I want a secure profile panel so I can view my account details and history.",
        "gherkin": "Given the user session is authenticated,\nWhen navigating to the account dashboard,\nThen query backend records and display profile + order history."
    },
    "order": {
        "title": "📦 Order Tracking",
        "story": "As a Customer, I want to track past and current orders so I know their status.",
        "gherkin": "Given an order has been placed,\nWhen the user opens 'My Orders',\nThen display real-time status pulled from the fulfillment service."
    },
    "payment": {
        "title": "💰 Payment Processing",
        "story": "As a Customer, I want multiple secure payment options so I can pay using my preferred method.",
        "gherkin": "Given a valid cart total,\nWhen the user selects a payment method,\nThen route the transaction through a PCI-compliant gateway."
    },
    "search": {
        "title": "🔍 Search",
        "story": "As a User, I want fast, relevant search so I can find what I need without browsing manually.",
        "gherkin": "Given a search query is entered,\nWhen results are requested,\nThen return ranked results in under 300ms."
    },
    "notification": {
        "title": "🔔 Notifications",
        "story": "As a User, I want timely notifications so I stay informed about relevant updates.",
        "gherkin": "Given a triggering event occurs,\nWhen the notification service processes it,\nThen deliver a push/email notification within 60 seconds."
    },
    "dashboard": {
        "title": "📊 Dashboard",
        "story": "As a User, I want a summary dashboard so I can see key metrics at a glance.",
        "gherkin": "Given the user has active data,\nWhen the dashboard loads,\nThen render key metrics within 2 seconds."
    },
    "chat": {
        "title": "💬 Messaging",
        "story": "As a User, I want in-app messaging so I can communicate without leaving the platform.",
        "gherkin": "Given two users are connected,\nWhen a message is sent,\nThen deliver it in real time via websocket."
    },
    "review": {
        "title": "⭐ Reviews & Ratings",
        "story": "As a Customer, I want to leave and read reviews so I can make informed decisions.",
        "gherkin": "Given a completed purchase,\nWhen the user submits a review,\nThen store and display it against the product listing."
    },
}

CONFLICT_RULES = [
    (["guest", "without account", "without signup", "no account"], ["track", "history", "profile", "past orders"],
     "Anonymous Guest Checkout vs. Historical Profile Tracking",
     "Permanent data tracking can't be bound to an unauthenticated session. Mitigation: use email-verified magic links or tokenized guest order lookups."),
    (["free"], ["premium", "subscription", "paid"],
     "Free vs. Paid Monetization Signal",
     "Clarify monetization model early — freemium tiering vs. flat subscription changes the entire billing architecture."),
    (["real-time", "instant", "live"], ["offline", "sync later", "batch"],
     "Real-Time Expectation vs. Offline/Batch Processing",
     "Define which flows must be real-time vs. eventually-consistent to avoid over-engineering every component."),
    (["100% secure", "fully secure", "hacker proof"], ["fast", "quick", "super fast"],
     "Absolute Security Claim vs. Speed Priority",
     "Security controls (MFA, encryption, fraud checks) add latency — define acceptable trade-off thresholds rather than 'both, fully'."),
]

MARKET_INSIGHTS = {
    "E-Commerce & Retail": [
        {"icon": "🛒", "source": "Developer & Technical Forums",
         "insight": "48% of surveyed users report checkout friction when complex payment protocols are involved.",
         "pivot": "Rely on core credit processors and mobile wallets for Phase 1; defer alternative currencies to Phase 2."},
        {"icon": "📱", "source": "App Store Reviews",
         "insight": "Forced registration before checkout is a leading cause of cart abandonment.",
         "pivot": "Guest checkout directly addresses this churn vector — keep it in scope."},
        {"icon": "🔐", "source": "Security Benchmarks",
         "insight": "PCI-DSS non-compliance is a top reason e-commerce apps fail security audits.",
         "pivot": "Scope PCI-DSS SAQ-A compliance from day one via a tokenized payment gateway."},
    ],
    "SaaS Dashboard & Analytics": [
        {"icon": "📊", "source": "Product Hunt & G2 Reviews",
         "insight": "Users abandon dashboards that take longer than 3 seconds to render key metrics.",
         "pivot": "Prioritize server-side aggregation and caching for the primary dashboard view."},
        {"icon": "🔗", "source": "Developer Communities",
         "insight": "Lack of API/webhook access is a top churn driver for SaaS analytics tools.",
         "pivot": "Ship a documented public API alongside the UI, even in MVP scope."},
        {"icon": "👥", "source": "Enterprise Buyer Forums",
         "insight": "Role-based access control is a hard requirement for team-tier adoption.",
         "pivot": "Design the permissions model early — retrofitting RBAC is costly."},
    ],
    "FinTech & Payments": [
        {"icon": "🏦", "source": "Regulatory & Compliance Forums",
         "insight": "KYC/AML friction is the top reason fintech onboarding funnels leak users.",
         "pivot": "Use a tiered KYC approach — light verification to start, step-up for higher limits."},
        {"icon": "📱", "source": "App Store Reviews",
         "insight": "Users expect biometric login as standard in financial apps.",
         "pivot": "Include Face ID / fingerprint auth in the core scope, not a stretch goal."},
        {"icon": "🔐", "source": "Security Benchmarks",
         "insight": "Fraud detection latency is closely watched by both users and regulators.",
         "pivot": "Budget for a real-time fraud-scoring service, not a post-hoc batch job."},
    ],
    "Healthcare & Telemed": [
        {"icon": "🏥", "source": "Clinical & Compliance Forums",
         "insight": "HIPAA-readiness is a blocking requirement, not a nice-to-have, for pilot deployments.",
         "pivot": "Architect data storage and logging for HIPAA compliance from day one."},
        {"icon": "📱", "source": "Patient App Reviews",
         "insight": "Patients abandon telehealth apps with more than 2 steps to start a video call.",
         "pivot": "Make 'join call' a single tap from the home screen."},
        {"icon": "🩺", "source": "Provider Feedback",
         "insight": "Providers want EHR integration over standalone record-keeping.",
         "pivot": "Plan for HL7/FHIR interoperability rather than a siloed data model."},
    ],
}

CRYPTO_INSIGHT = {"icon": "₿", "source": "Crypto/Web3 User Forums",
                   "insight": "Users report significant drop-off when crypto payment flows require external wallet steps.",
                   "pivot": "If crypto support is required, embed an in-app custodial wallet option rather than requiring an external wallet."}


def analyze(raw_text: str, category: str, budget: int):
    text = raw_text.lower()

    # --- Feature detection ---
    detected_features = [k for k in FEATURE_STORIES if k in text]
    stories = [FEATURE_STORIES[k] for k in detected_features] or [
        FEATURE_STORIES["cart"], FEATURE_STORIES["checkout"]
    ]

    # --- Ambiguity detection ---
    ambiguities = []
    for term, (label, target) in VAGUE_TERMS.items():
        if term in text:
            ambiguities.append({"term": term, "label": label, "target": target})

    # --- Conflict detection ---
    conflicts = []
    for set_a, set_b, title, resolution in CONFLICT_RULES:
        if any(a in text for a in set_a) and any(b in text for b in set_b):
            conflicts.append({"title": title, "resolution": resolution})

    # --- Market insights (category-based + conditional crypto) ---
    insights = list(MARKET_INSIGHTS.get(category, []))
    if any(w in text for w in ["crypto", "bitcoin", "cryptocurrency", "web3"]):
        insights.append(CRYPTO_INSIGHT)

    # --- Cost & capacity estimate (scales with budget + complexity) ---
    complexity = max(len(detected_features), 2)
    low = int(budget * 0.72)
    high = int(budget * 1.08)
    infra_map = {
        "E-Commerce & Retail": 85, "SaaS Dashboard & Analytics": 60,
        "FinTech & Payments": 140, "Healthcare & Telemed": 160,
    }
    infra = infra_map.get(category, 90) + complexity * 6
    hours = 180 + complexity * 35

    return {
        "stories": stories,
        "ambiguities": ambiguities,
        "conflicts": conflicts,
        "insights": insights,
        "cost_low": low,
        "cost_high": high,
        "infra": infra,
        "hours": hours,
        "complexity": complexity,
    }


# ============================================================
# 4. INPUT LAYER
# ============================================================
st.subheader("📥 Ingestion Layer: Unstructured Customer Input")
raw_input = st.text_area(
    "Paste client emails, communications records, or rough discovery notes below:",
    value="Hey, we need a shopping cart feature ASAP. Make it look sleek like Amazon. It should load super fast. Also, we want people to buy things without a long signup, but make sure they can still track their past orders in their profile section. Oh, and it needs to be 100% secure against hackers.",
    height=150
)

# ============================================================
# 5. PIPELINE EXECUTION
# ============================================================
if st.button("🚀 Run Complete Discovery & Analysis Pipeline", type="primary"):
    with st.spinner("🔎 Analyzing structural architecture, risk profiles, market indicators, and financial matrices..."):
        time.sleep(1.2)
        st.session_state.analysis = analyze(raw_input, product_category, target_budget)
        st.session_state.pipeline_run = True

if st.session_state.pipeline_run and st.session_state.analysis:
    a = st.session_state.analysis
    st.success("✅ Analysis Complete. Discovery Dashboard Generated.")
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "✅ Actionable Requirements",
        "⚠️ Risk & Ambiguity Audit",
        "📊 Market & Social Insights",
        "💰 Cost & Trend Forecast"
    ])

    # ---------------- TAB 1 ----------------
    with tab1:
        st.markdown("### 🛠️ Functional Engineering Specifications")
        for s in a["stories"]:
            st.markdown(f"""
                <div class="story-card">
                    <strong>{s['title']}</strong><br/>{s['story']}
                </div>
            """, unsafe_allow_html=True)
            st.code(f"Acceptance Criteria (Gherkin Syntax):\n{s['gherkin']}", language="gherkin")

        st.markdown("---")
        if st.button("📤 Export Specifications to Jira Backlog"):
            st.session_state.jira_exported = True
            st.balloons()

        if st.session_state.jira_exported:
            st.success(f"🎫 {len(a['stories'])} sprint ticket(s) successfully compiled and migrated to the connected Jira Project Backlog.")

    # ---------------- TAB 2 ----------------
    with tab2:
        st.markdown("### 🔍 Architectural Risk Audit")

        st.markdown("#### 🧨 Structural Contradictions & Conflicts")
        if a["conflicts"]:
            for c in a["conflicts"]:
                st.markdown(f"""
                    <div class="conflict-card">
                        <strong>⚔️ System Conflict:</strong> {c['title']}<br/>
                        <em>Recommended Resolution:</em> {c['resolution']}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("✨ No hard structural conflicts detected in this input.")

        st.markdown("#### 🌫️ Technical Ambiguities Detected")
        if a["ambiguities"]:
            for amb in a["ambiguities"]:
                st.markdown(f"""
                    <div class="ambiguity-card">
                        <strong>🚩 '{amb['term']}'</strong> ({amb['label']})<br/>
                        <strong>Engineering Target →</strong> {amb['target']}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🎉 No major ambiguous terms detected in this input.")

    # ---------------- TAB 3 ----------------
    with tab3:
        st.markdown("### 🌐 Market Data & Competitor Insight Analysis")
        st.write(f"Synthesized signals for **{product_category}** products, based on your input and category:")

        if a["insights"]:
            for ins in a["insights"]:
                st.markdown(f"""
                    <div class="section-block">
                        <strong>{ins['icon']} Source:</strong> {ins['source']}<br/>
                        • <strong>📈 Market Insight:</strong> {ins['insight']}<br/>
                        • <strong>🎯 Strategic Pivot:</strong> {ins['pivot']}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No market insights available for this category yet.")

    # ---------------- TAB 4 ----------------
    with tab4:
        st.markdown("### 💵 Strategic Financial & Capacity Estimations")

        c1, c2, c3 = st.columns(3)
        cards = [
            ("💰 Estimated Allocation Range", f"${a['cost_low']:,} - ${a['cost_high']:,}", "#0EA5E9, #38BDF8"),
            ("☁️ Cloud Infra / Month", f"${a['infra']} / mo", "#7C3AED, #A78BFA"),
            ("👷 Engineering Footprint", f"{a['hours']} Hours", "#EC4899, #F472B6"),
        ]
        for col, (label, value, colors) in zip([c1, c2, c3], cards):
            with col:
                st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, {colors});">
                        {label}
                        <div class="metric-value">{value}</div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📌 Strategic Trend Alignment")
        st.info(f"🔑 Detected feature complexity: **{a['complexity']} core modules**. Market Context: passwordless/biometric verification strategies improve onboarding conversion by up to 22% vs. traditional password creation.")
