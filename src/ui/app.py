import streamlit as st

st.set_page_config(
    page_title="Medical Edge Triage System",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 Medical Edge Triage System")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Patient Symptoms")
    symptoms = st.text_area(
        "Describe the symptoms",
        placeholder="e.g., fever 39C headache stiff neck",
        height=120,
    )

    col_age, col_dur = st.columns(2)
    with col_age:
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
    with col_dur:
        duration = st.number_input(
            "Duration (hours)", min_value=0, max_value=720, value=0
        )

    analyze_btn = st.button("Analyze", type="primary", use_container_width=True)

st.divider()

if analyze_btn and symptoms.strip():
    with st.spinner("Running triage analysis..."):
        from src.orchestrator import run_triage, run_counterfactual

        result = run_triage(symptoms)

        col_res, col_cf = st.columns(2)

        with col_res:
            st.subheader("Triage Result")

            urgency_color = {
                "Level 1": "🔴",
                "Level 2": "🟠",
                "Level 3": "🟡",
                "Level 4": "🟢",
                "Level 5": "⚪",
            }
            emoji = "🔴"
            for key, val in urgency_color.items():
                if key in result.triage_level:
                    emoji = val

            st.markdown(f"### {emoji} {result.triage_level}")
            st.metric("Confidence", f"{result.confidence:.2%}")

            with st.expander("Reasoning", expanded=True):
                st.write(result.reasoning)

            if result.supporting_evidence:
                st.markdown("**Supporting Evidence:**")
                for ev in result.supporting_evidence:
                    st.markdown(f"- {ev}")

            if result.knowledge_warnings:
                with st.expander("⚠️ Knowledge Warnings"):
                    for w in result.knowledge_warnings:
                        st.warning(w)

            st.markdown("**Pass Votes:**")
            votes = result.pass_votes
            for i, v in enumerate(votes, 1):
                st.text(f"  Pass {i}: {v}")

        with col_cf:
            st.subheader("Counterfactual Analysis")
            remove_term = st.text_input(
                "Remove a symptom to test impact",
                placeholder="e.g., stiff neck",
            )

            if remove_term and st.button("Run Counterfactual"):
                cf_result = run_counterfactual(symptoms, remove_term)
                st.markdown(f"**Original:** {cf_result.original_level}")
                st.markdown(
                    f"**Without '{cf_result.removed_symptom}':** "
                    f"{cf_result.counterfactual_level}"
                )
                with st.expander("Counterfactual Reasoning"):
                    st.write(cf_result.reasoning)

elif analyze_btn:
    st.warning("Please enter symptoms before analyzing.")
