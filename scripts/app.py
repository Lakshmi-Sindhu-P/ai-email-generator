import sys
sys.path.append('../scripts')  # Ensure modules are found

import streamlit as st
from utils import load_dataset
from prompts import build_subject_prompt, build_email_prompt
from email_generator import get_subject_lines, get_email_drafts
from db import init_db, save_email_log

init_db()
df = load_dataset()

st.title("AI Email Generator")

recipient = st.text_input("Recipient")
subject_context = st.text_input("Subject Context")
tone = st.selectbox("Tone", ["Professional", "Friendly", "Formal", "Casual", "Other"])
purpose = st.text_area("Purpose / Action to Request", height=40)
bullet_points = st.text_area("Bullet Points (separate by new lines)", height=60)
length = st.selectbox("Draft Length", ["Short", "Medium", "Long"])
additional_notes = st.text_area("Additional Notes", height=40)

template = None
if df is not None and 'subject' in df.columns:
    template_options = ["None"] + list(df['subject'].dropna().unique()[:10])
    selected_template = st.selectbox("Choose dataset subject (optional)", template_options)
    template = ""
    if selected_template != "None":
        row = df[df['subject'] == selected_template]
        # If your dataset contains an actual template column, e.g. 'email_body'
        if not row.empty and 'email_body' in row.columns:
            template = row.iloc[0]['email_body']

if st.button("Generate"):
    if not all([recipient, subject_context, tone, purpose, bullet_points, length]):
        st.warning("Please fill all required fields.")
    else:
        inputs = {
            "recipient": recipient,
            "subject_context": subject_context,
            "tone": tone,
            "purpose": purpose,
            "bullet_points": [bp for bp in bullet_points.split('\n') if bp.strip()],
            "length": length,
            "additional_notes": additional_notes
        }
        with st.spinner("Generating emails..."):
            subjects = get_subject_lines(inputs)
            drafts = get_email_drafts(inputs, template)
            save_email_log(inputs, subjects, drafts)

        st.subheader("Suggested Subject Lines")
        for idx, subj in enumerate(subjects, 1):
            st.markdown(f"**{idx}. {subj}**")

        st.subheader("Email Drafts")
        for idx, draft in enumerate(drafts, 1):
            st.markdown(f"**Draft {idx}:**")
            st.code(draft, language='markdown')

        st.success("Emails generated and logged locally.")
