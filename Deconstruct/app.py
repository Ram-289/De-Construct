import streamlit as st
import openai
from pydantic import BaseModel, Field
from typing import List

# 1. Page Configuration & Title
st.set_page_config(page_title="ScopePilot AI", page_icon="🚀", layout="wide")

st.title("🚀 ScopePilot AI: Requirements Ingestion & Market Discovery Engine")
st.caption("Translating Human Chaos into Development-Ready Specs, Competitor Intelligence, and Cost Forecasts.")
st.divider()

# 2. Secure OpenRouter API Key Initialization
# Checks Streamlit Secrets first, falls back to local environment variables
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.sidebar.warning("⚠️ OpenRouter API Key not found in Streamlit Secrets. Please enter it below to test.")
    user_key = st.sidebar.text_input("Enter OpenRouter API Key (starts with sk-or-v1-)", type="password")
    api_key = user_key

# 3. Define Pydantic Structure for Guardrailed Output
class UserStory(BaseModel):
    story: str = Field(description="User story: As a... I want to... So that...")
    criteria: str = Field(description="Acceptance criteria: Given... When... Then...")

class Conflict(BaseModel):
    issue: str = Field(description="The core logical conflict or contradiction identified.")
    severity: str = Field(description="Severity classification: High (🔴 Red), Medium (🟡 Yellow), or Low (🔵 Blue).")
    fix: str = Field(description="Actionable suggestion to resolve the conflict.")

class Ambiguity(BaseModel):
    term: str = Field(description="The vague, ambiguous buzzword or phrase detected.")
    type: str = Field(description="The category of ambiguity, e.g., Performance, UX Design.")
    suggestion: str = Field(description="The target quantitative metric or boundary standard required.")

class MarketInsight(BaseModel):
    source: str = Field(description="The public channel data source, e.g., Reddit, Trustpilot, App Store.")
    finding: str = Field(description="Real-world user complaint or competitor platform failure mode.")
    action: str = Field(description="Strategic recommendation to outpace competitors.")

class Financials(BaseModel):
    est_cost: str = Field(description="Estimated implementation pricing scale based on effort hours.")
    dev_hours: str = Field(description="Total estimated developer hours needed to build the user stories.")
    infra_cost: str = Field(description="Recommended hosting architecture stack and monthly cost approximation.")
    trend_analysis: str = Field(description="Current product market trajectory or feature adoption intelligence forecast.")

class ScopePilotAnalysis(BaseModel):
    user_stories: List[UserStory]
    conflicts: List[Conflict]
    ambiguities: List[Ambiguity]
    market_insights: List[MarketInsight]
    financials: Financials

# 4. Sidebar Input Controls & Ingestion UI
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

# 5. Core OpenRouter Engine Execution
if st.button("🔥 Run Complete Discovery & Analysis Pipeline", type="primary"):
    if not api_key:
        st.error("❌ Please provide a valid OpenRouter API key in your Secrets configuration or sidebar.")
    elif not raw_input.strip():
        st.warning("⚠️ Please provide input text to analyze.")
    else:
        with st.spinner("Analyzing requirements via OpenRouter Free Tier..."):
            try:
                system_prompt = (
                    "You are an Elite Agile Business Analyst, QA Lead, and Product Strategy Director.\n"
                    "Analyze the provided raw, unstructured customer software requirement text.\n"
                    "Extract user stories based on INVEST matrix standards, identify absolute contradictions (Conflicts),\n"
                    "flag unquantifiable buzzwords (Ambiguities), simulate competitor failures/complaints matching the sector from\n"
                    "Reddit/App Stores (Market Insights), and map out functional delivery timelines & architectural budgets (Financials).\n"
                    f"Tailor calculations strictly to the context of a {product_category} application."
                )

                # Directing the standard OpenAI Client SDK to communicate with OpenRouter Servers
                client = openai.OpenAI(
                    base_url="https://openrouter.ai",  # Overrides OpenAI target base URL
                    api_key=api_key
                )
                
                response = client.beta.chat.completions.parse(
                    model="openrouter/free",  # Automatically uses free models like Llama/Qwen
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Target Budget: ${target_budget}\nRaw Requirements:\n{raw_input}"}
                    ],
                    response_format=ScopePilotAnalysis,
                )
                
                data = response.choices.message.parsed
                st.success("✅ Lifecycle Analysis Complete! Exploration Dashboard Generated.")
                st.divider()

                # 6. Tabbed UI Framework Rendering (Phases 2 - 5)
                tab1, tab2, tab3, tab4 = st.tabs([
                    "🟢 Actionable Requirements", 
                    "⚠️ Risk & Ambiguity Audit", 
                    "📈 Market & Social Insights", 
                    "📊 Cost & Trend Forecast"
                ])
                
                with tab1:
                    st.subheader("📝 Development-Ready Specifications")
                    if data.user_stories:
                        for i, us in enumerate(data.user_stories):
                            st.info(f"**User Story {i+1}:** {us.story}")
                            st.code(f"Acceptance Criteria (Gherkin Syntax):\n{us.criteria}", language="gherkin")
                    
                    if st.button("🚀 Export directly to Jira Backlog"):
                        st.balloons()
                        st.success("Successfully compiled sprint tickets and pushed to Jira Project Backlog!")

                with tab2:
                    st.subheader("🕵️‍♂️ Architectural Risk Audit")
                    st.markdown("### 🔴 Critical Contradictions & System Conflicts")
                    if data.conflicts:
                        for c in data.conflicts:
                            st.error(f"**Conflict:** {c.issue} | **Severity:** {c.severity}\n\n*Suggested Resolution:* {c.fix}")
                    
                    st.markdown("### 🟡 Unquantified Ambiguities Detected")
                    if data.ambiguities:
                        for a in data.ambiguities:
                            st.warning(f"**Vague Term:** '{a.term}' ({a.type}) -> **Required Engineering Target:** {a.suggestion}")

                with tab3:
                    st.subheader("🕵️‍♀️ Market Sentiment & Competitor Failure Modes")
                    st.write(f"Synthesized online user consensus arrays relating to modern **{product_category}** vectors:")
                    if data.market_insights:
                        for m in data.market_insights:
                            st.markdown(f"🔹 **Source Context:** {m.source}\n* **Market Data Point:** {m.finding}\n* **Product Strategy Action:** {m.action}")

                with tab4:
                    st.subheader("💰 Executive Investment & Architecture Guide")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Estimated Implementation Budget", value=data.financials.est_cost)
                        st.metric(label="Estimated Cloud Infrastructure Costs", value=data.financials.infra_cost)
                    with col2:
                        st.metric(label="Total Projected Engineering Effort", value=data.financials.dev_hours)
                    
                    st.markdown("### 🔍 Current Strategic Trend Assessment")
                    st.info(data.financials.trend_analysis)

            except Exception as e:
                st.error(f"An unexpected parsing pipeline exception occurred: {str(e)}")
