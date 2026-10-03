import streamlit as st
from src.pipelines.pipeline import research_pipeline

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 AI Research Assistant")
st.write("Research a topic using AI-powered search, reading, writing, and critique.")

topic = st.text_input(
    "Research Topic",
    placeholder="e.g. AI Guardrails"
)

if st.button("🚀 Start Research", type="primary"):

    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Researching... Please wait."):

            result = research_pipeline(topic)

        st.success("Research completed!")

        st.divider()

        st.subheader("📄 Final Report")

        st.markdown(result["report"])

        st.divider()

        st.download_button(
            label="⬇️ Download Report (.md)",
            data=result["report"],
            file_name=f"{topic.replace(' ', '_')}_report.md",
            mime="text/markdown"
        )