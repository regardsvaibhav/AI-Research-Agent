import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from pipeline import run_pipeline

# Page config
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔬",
    layout="wide"
)

# Header
st.title("🔬 AI Research Agent")
st.markdown("*Autonomous literature discovery and research idea generation*")
st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    max_results = st.slider("Papers to fetch", 3, 10, 5)
    top_k = st.slider("Papers to analyze", 2, 5, 3)
    st.divider()
    st.markdown("**How it works:**")
    st.markdown("1. 🔍 Search Arxiv papers")
    st.markdown("2. 📊 Index with FAISS")
    st.markdown("3. 📖 Analyze with LLM")
    st.markdown("4. 💡 Generate ideas")

# Input
col1, col2 = st.columns([2, 1])
with col1:
    user_query = st.text_input(
        "Research Question",
        placeholder="e.g. How can federated learning be applied to EV battery monitoring?",
        label_visibility="collapsed"
    )
with col2:
    search_query = st.text_input(
        "Search Keywords",
        placeholder="e.g. federated learning EV battery",
        label_visibility="collapsed"
    )

run_button = st.button("🚀 Run Research Agent", type="primary", use_container_width=True)

# Run pipeline
if run_button and user_query:
    
    with st.spinner("🔍 Searching papers..."):
        try:
            result = run_pipeline(
                user_query=user_query,
                search_query=search_query if search_query else user_query,
                max_results=max_results
            )
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    st.success(f"✅ Found {result['papers_found']} papers, analyzed {len(result['papers_analyzed'])}")
    st.divider()

# Two columns layout
    left, right = st.columns([1, 1])

    with left:
        st.subheader("📖 Papers Analyzed")
        for i, paper in enumerate(result["papers_analyzed"]):
            with st.expander(f"📄 {paper['title'][:70]}..."):
                st.markdown(f"🔗 [View Paper]({paper['url']})")
                st.markdown(f"📅 Published: {paper['published']}")
                st.divider()
                st.markdown(paper["analysis"])

    with right:
        st.subheader("📋 Research Plan")
        plan = result["plan"]
        st.markdown(f"**Topic:** {plan['main_topic']}")
        st.markdown("**Search Queries Used:**")
        for q in plan["search_queries"]:
            st.markdown(f"- {q}")
        st.markdown("**Key Aspects:**")
        for a in plan["key_aspects"]:
            st.markdown(f"- {a}")

    st.divider()

    # Ideas + Experiments tabs
    tab1, tab2 = st.tabs(["💡 Research Ideas", "🧪 Experiment Designs"])

    with tab1:
        st.markdown(result["ideas"])

    with tab2:
        st.markdown(result["experiments"])

    # Download
    st.divider()
    output = f"""# Research Agent Results

## Query
{result['query']}

## Research Plan
Topic: {result['plan']['main_topic']}

## Papers Analyzed
"""
    for p in result["papers_analyzed"]:
        output += f"\n### {p['title']}\n{p['analysis']}\n"

    output += f"\n## Research Ideas\n{result['ideas']}"
    output += f"\n## Experiment Designs\n{result['experiments']}"

    st.download_button(
        label="📥 Download Full Report",
        data=output,
        file_name="research_report.md",
        mime="text/markdown"
    )