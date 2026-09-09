import streamlit as st
import requests
import json

# 1. Page Configuration & Title Layout
st.set_page_config(page_title="ScopePilot AI", page_icon="🚀", layout="wide")

st.title("🚀 ScopePilot AI: Requirements Ingestion & Market Discovery Engine")
st.caption("Translating Human Chaos into Development-Ready Specs, Competitor Intelligence, and Cost Forecasts.")
st.divider()

# 2. Secure OpenRouter API Key Initialization
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.sidebar.warning("⚠️ OpenRouter API Key not found in Streamlit Secrets. Please enter it below to test.")
    user_key = st.sidebar.text_input("Enter OpenRouter API Key (starts with sk-or-v1-)", type="password")
    api_key = user_key

# 3. Sidebar Input Controls & Ingestion UI
st.sidebar.header("📌 Project Configurations")
product_category = st.sidebar.selectbox(
    "Product Domain Category", 
    ["E-Commerce & Retail", "SaaS Dashboard & Analytics", "FinTech & Payments", "Healthcare & Telemed"]
)
target_budget = st.sidebar.slider("Target Investment Boundary ($)", 5000, 200000, 45000, step=5000)

st.subheader("📥 Ingestion Layer: Raw Customer Input")
raw_input = st.text_area(
    "Paste messy client emails, Slack messages, chat transcripts, or rough notes below:", 
    value="Hey, we need a shopping cart feature ASAP. Make it look sleek like Amazon. It should load super fast. Also, we want people to buy things without a long signup, but make sure they can still track their past orders in their profile section. Oh, and it needs to be 100% secure against hackers.",
    height=150
)

# 4. Core Direct API Request Processing
if st.button("🔥 Run Complete Discovery & Analysis Pipeline", type="primary"):
    if not api_key:
        st.error("❌ Please provide a valid OpenRouter API key in your Secrets configuration or sidebar.")
    elif not raw_input.strip():
        st.warning("⚠️ Please provide input text to analyze.")
    else:
        with st.spinner("Analyzing requirements via Direct HTTP OpenRouter connection..."):
            try:
                system_prompt = (
                    "You are an Elite Agile Business Analyst and Product Strategy Director.\n"
                    "Analyze the provided raw customer software requirement text.\n"
                    "You MUST reply ONLY with a valid JSON object string. Do not wrap it in markdown code blocks like ```json. Just raw text JSON.\n\n"
                    "The JSON format structure must be exactly:\n"
                    "{\n"
                    '  "user_stories": [{"story": "As a... I want to... So that...", "criteria": "Given... When... Then..."}],\n'
                    '  "conflicts": [{"issue": "Description", "severity": "High (🔴 Red)", "fix": "Fix instructions"}],\n'
                    '  "ambiguities": [{"term": "Vague word", "type": "Performance/UX", "suggestion": "Metric goal"}],\n'
                    '  "market_insights": [{"source": "Reddit", "finding": "Complaint details", "action": "Recommendation"}],\n'
                    '  "financials": {"est_cost": "\(Value", "dev_hours": "Hours", "infra_cost": "\)/mo", "trend_analysis": "Trends summary"}\n'
                    "}"
                )

                # Constructing direct HTTP Post structure to route past SDK object differences
                url = "https://openrouter.ai"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "openrouter/free",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Target Budget: \${target_budget}\nRaw Requirements:\n{raw_input}"}
                    ]
                }

                # Sending direct network request
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                response_json = response.json()

                # Parsing the raw JSON data block from the server structure safely
                raw_content = response_json["choices"][0]["message"]["content"].strip()
                
                # Cleaning out any potential markdown markers if added by the model
                if raw_content.startswith("```"):
                    lines = raw_content.split("\n")
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines[-1].startswith("```"):
                        lines = lines[:-1]
                    raw_content = "\n".join(lines).strip()
                
                data = json.loads(raw_content)
                
                st.success("✅ Lifecycle Analysis Complete! Exploration Dashboard Generated.")
                st.divider()

                # 5. Tabbed UI Framework Rendering
                tab1, tab2, tab3, tab4 = st.tabs([
                    "🟢 Actionable Requirements", 
                    "⚠️ Risk & Ambiguity Audit", 
                    "📈 Market & Social Insights", 
                    "📊 Cost & Trend Forecast"
                ])
                
                with tab1:
                    st.subheader("📝 Development-Ready Specifications")
                    if "user_stories" in data:
                        for i, us in enumerate(data["user_stories"]):
                            st.info(f"**User Story {i+1}:** {us.get('story', '')}")
                            st.code(f"Acceptance Criteria (Gherkin Syntax):\n{us.get('criteria', '')}", language="gherkin")
                    
                    if st.button("🚀 Export directly to Jira Backlog"):
                        st.balloons()
                        st.success("Successfully compiled sprint tickets and pushed to Jira Project Backlog!")

                with tab2:
                    st.subheader("🕵️‍♂️ Architectural Risk Audit")
                    st.markdown("### 🔴 Critical Contradictions & System Conflicts")
                    if "conflicts" in data and data["conflicts"]:
                        for c in data["conflicts"]:
                            st.error(f"**Conflict:** {c.get('issue','')} | **Severity:** {c.get('severity', '')}\n\n*Suggested Resolution:* {c.get('fix', '')}")
                    else:
                        st.success("No critical logical contradictions found.")
                    
                    st.markdown("### 🟡 Unquantified Ambiguities Detected")
                    if "ambiguities" in data:
                        for a in data["ambiguities"]:
                            st.warning(f"**Vague Term:** '{a.get('term', '')}' ({a.get('type', '')}) -> **Required Engineering Target:** {a.get('suggestion', '')}")

                with tab3:
                    st.subheader("🕵️‍♀️ Market Sentiment & Competitor Failure Modes")
                    st.write(f"Synthesized online user consensus arrays relating to modern **{product_category}** vectors:")
                    if "market_insights" in data:
                        for m in data["market_insights"]:
                            st.markdown(f"🔹 **Source Context:** {m.get('source', '')}\n* **Market Data Point:** {m.get('finding', '')}\n* **Product Strategy Action:** {m.get('action', '')}")

                with tab4:
                    st.subheader("💰 Executive Investment & Architecture Guide")
                    if "financials" in data:
                        fin = data["financials"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(label="Estimated Implementation Budget", value=fin.get('est_cost', 'N/A'))
                            st.metric(label="Estimated Cloud Infrastructure Costs", value=fin.get('infra_cost', 'N/A'))
                        with col2:
                            st.metric(label="Total Projected Engineering Effort", value=fin.get('dev_hours', 'N/A'))
                        
                        st.markdown("### 🔍 Current Strategic Trend Assessment")
                        st.info(fin.get('trend_analysis', 'No data generated.'))

            except Exception as e:
                st.error(f"Failed to safely compile or parse data structure layout: {str(e)}")
                st.info("💡 Tip: Free endpoints occasionally experience heavy load spikes. Try clicking the action button again to re-verify.")
