"""
AI Email Generator - Streamlit Application
Main application file for the email generation interface.
"""
import sys
sys.path.append('../scripts')

import streamlit as st
from typing import Optional
from utils import load_dataset, count_words, count_characters
from prompts import build_subject_prompt, build_email_prompt, validate_inputs
from email_generator import get_subject_lines, get_email_drafts, EmailGenerationError
from db import init_db, save_email_log, DatabaseError
from config import APP_TITLE, APP_ICON, DEFAULT_TONES, DEFAULT_LENGTHS, validate_config
from logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
try:
    init_db()
    logger.info("Application started successfully")
except DatabaseError as e:
    st.error(f"Database initialization failed: {e}")
    logger.error(f"Database initialization failed: {e}")
    st.stop()

# Validate configuration
if not validate_config(raise_error=False):
    st.error("⚠️ Configuration Error: OPENAI_API_KEY not found")
    
    st.info("""
    **To fix this issue:**
    
    **Local Development:**
    1. Copy `.env.example` to `.env`
    2. Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`
    3. Restart the app
    
    **Streamlit Cloud:**
    1. Go to your app settings
    2. Click on "Secrets" in the sidebar
    3. Add: `OPENAI_API_KEY = "your_key_here"`
    4. Save and redeploy
    """)
    
    logger.error("OpenAI API key not configured")
    st.stop()

# Load dataset
df = load_dataset()

# Application Title
st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown("Generate professional emails with AI assistance. Create multiple drafts and subject lines tailored to your needs.")

# Sidebar for information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This tool helps you generate:
    - **5 subject line options**
    - **2 email drafts** with different styles
    
    All generated emails are saved locally for your reference.
    """)
    
    st.header("💡 Tips")
    st.markdown("""
    - Be specific in your purpose
    - Add clear bullet points
    - Choose the right tone
    - Review and edit generated drafts
    """)

# Main form
st.header("📝 Email Details")

col1, col2 = st.columns(2)

with col1:
    recipient = st.text_input(
        "Recipient *",
        placeholder="e.g., John Doe, HR Manager",
        help="Name and/or title of the email recipient"
    )
    
    subject_context = st.text_input(
        "Subject Context *",
        placeholder="e.g., Follow-up on job application",
        help="Brief context for the email subject"
    )
    
    tone = st.multiselect(
        "Tone (select 1-3) *",
        DEFAULT_TONES,
        default=[DEFAULT_TONES[0]],
        max_selections=3,
        help="Select up to 3 tones to create nuanced emails (e.g., Professional + Friendly)"
    )

with col2:
    purpose = st.text_area(
        "Purpose / Action to Request *",
        height=100,
        placeholder="e.g., Request a meeting to discuss the project timeline",
        help="Main purpose or action you want from this email"
    )
    
    length = st.selectbox(
        "Draft Length *",
        DEFAULT_LENGTHS,
        help="Desired length of the email drafts"
    )

bullet_points = st.text_area(
    "Key Points (one per line) *",
    height=120,
    placeholder="Point 1\nPoint 2\nPoint 3",
    help="Enter each key point on a new line"
)

additional_notes = st.text_area(
    "Additional Notes (optional)",
    height=80,
    placeholder="Any specific requirements or preferences...",
    help="Optional: Any extra context or special instructions"
)

# Optional template selection from dataset
template = None
if df is not None and 'subject' in df.columns:
    with st.expander("📄 Use Dataset Template (Optional)"):
        template_options = ["None"] + list(df['subject'].dropna().unique()[:10])
        selected_template = st.selectbox(
            "Choose a template from dataset",
            template_options,
            help="Optionally base your email on an existing template"
        )
        
        if selected_template != "None":
            row = df[df['subject'] == selected_template]
            if not row.empty and 'email_body' in row.columns:
                template = row.iloc[0]['email_body']
                st.info(f"Selected template: {selected_template}")

st.markdown("---")

# Generate button
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    generate_button = st.button("✨ Generate Emails", type="primary", use_container_width=True)
with col2:
    if st.button("🔄 Clear Form", use_container_width=True):
        st.rerun()

if generate_button:
    # Prepare inputs
    inputs = {
        "recipient": recipient.strip() if recipient else "",
        "subject_context": subject_context.strip() if subject_context else "",
        "tone": tone,  # List of tones
        "purpose": purpose.strip() if purpose else "",
        "bullet_points": [bp.strip() for bp in bullet_points.split('\n') if bp.strip()],
        "length": length,
        "additional_notes": additional_notes.strip() if additional_notes else ""
    }
    
    # Convert tone list to string for database storage
    tone_str = ' + '.join(tone) if isinstance(tone, list) else tone
    
    # Validate inputs
    is_valid, error_message = validate_inputs(inputs)
    
    if not is_valid:
        st.error(f"⚠️ Validation Error: {error_message}")
        logger.warning(f"Validation failed: {error_message}")
    else:
        try:
            with st.spinner("🤖 Generating emails... This may take a few moments."):
                # Generate subject lines
                logger.info("Starting email generation")
                subjects = get_subject_lines(inputs)
                
                # Generate drafts
                drafts = get_email_drafts(inputs, template)
                
                # Save to database (convert tone to string for storage)
                try:
                    storage_inputs = inputs.copy()
                    storage_inputs['tone'] = tone_str
                    log_id = save_email_log(storage_inputs, subjects, drafts)
                    logger.info(f"Email generation completed and saved with ID: {log_id}")
                except DatabaseError as e:
                    logger.error(f"Failed to save email log: {e}")
                    st.warning("⚠️ Emails generated but couldn't be saved to database.")
            
            # Display results
            st.success("✅ Emails generated successfully!")
            
            # Subject Lines Section
            st.header("📬 Suggested Subject Lines")
            st.markdown("*Click on any subject line to copy it*")
            
            for idx, subj in enumerate(subjects, 1):
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.markdown(f"**{idx}.** {subj}")
                with col2:
                    if st.button("📋", key=f"copy_subject_{idx}", help="Copy to clipboard"):
                        st.code(subj, language=None)
            
            st.markdown("---")
            
            # Email Drafts Section
            st.header("✉️ Email Drafts")
            
            tabs = st.tabs([f"📄 Draft {i+1}" for i in range(len(drafts))])
            
            for idx, (tab, draft) in enumerate(zip(tabs, drafts), 1):
                with tab:
                    # Show draft metadata with tone combination
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Words", count_words(draft))
                    with col2:
                        st.metric("Characters", count_characters(draft))
                    with col3:
                        # Determine tone combination for this draft
                        if isinstance(tone, list) and len(tone) > 0:
                            if len(tone) == 1:
                                draft_tone = tone[0]
                            elif len(tone) == 2:
                                draft_tone = tone[0] if idx == 1 else f"{tone[0]} + {tone[1]}"
                            else:  # 3 tones
                                draft_tone = f"{tone[0]} + {tone[1]}" if idx == 1 else ' + '.join(tone)
                        else:
                            draft_tone = "Professional" if idx == 1 else "Formal"
                        st.metric("Tone Used", draft_tone)
                    
                    st.markdown("---")
                    
                    # Display draft
                    st.text_area(
                        f"Draft {idx}",
                        value=draft,
                        height=400,
                        key=f"draft_{idx}",
                        help="You can edit this draft directly"
                    )
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📋 Copy Draft {idx}", key=f"copy_draft_{idx}", use_container_width=True):
                            st.code(draft, language=None)
                    with col2:
                        if st.button(f"💾 Download TXT", key=f"download_txt_{idx}", use_container_width=True):
                            st.download_button(
                                label=f"Download Draft {idx} as TXT",
                                data=draft,
                                file_name=f"email_draft_{idx}.txt",
                                mime="text/plain",
                                key=f"download_btn_{idx}"
                            )
            
            st.markdown("---")
            st.info("💡 **Tip:** All generated emails are saved to your local database. View them in the History page!")
            
        except EmailGenerationError as e:
            st.error(f"❌ Email Generation Error: {e}")
            logger.error(f"Email generation failed: {e}")
            st.info("Please check your internet connection and API key, then try again.")
            
        except Exception as e:
            st.error(f"❌ Unexpected Error: An error occurred during generation.")
            logger.error(f"Unexpected error in app: {e}", exc_info=True)
            st.info("Please try again. If the problem persists, check the logs.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>AI Email Generator | Powered by OpenAI | Built with Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
