"""
Email History Page - View and manage previously generated emails
"""
import sys
sys.path.append('../scripts')
sys.path.append('.')

import streamlit as st
from datetime import datetime
from db import get_email_logs, toggle_favorite, delete_email_log, DatabaseError
from utils import export_to_txt, export_to_html, format_bullet_points
from logger import setup_logger

logger = setup_logger(__name__)

# Page config
st.set_page_config(
    page_title="Email History - AI Email Generator",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Email History")
st.markdown("View, search, and manage all your previously generated emails.")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    
    show_favorites = st.checkbox("Show Favorites Only", value=False)
    
    st.markdown("---")
    
    limit = st.slider("Results per page", min_value=10, max_value=100, value=20, step=10)
    
    st.markdown("---")
    
    st.header("📊 Statistics")
    try:
        all_logs = get_email_logs(limit=1000)
        total_emails = len(all_logs)
        total_favorites = len([log for log in all_logs if log['is_favorite']])
        
        st.metric("Total Emails", total_emails)
        st.metric("Favorites", total_favorites)
        
        if all_logs:
            total_cost = sum(log.get('cost_estimate', 0) for log in all_logs)
            st.metric("Total Cost", f"${total_cost:.4f}")
    except Exception as e:
        st.error(f"Error loading statistics: {e}")
        logger.error(f"Error in statistics: {e}")

# Main content
try:
    logs = get_email_logs(limit=limit, favorites_only=show_favorites)
    
    if not logs:
        st.info("📭 No emails found. Generate your first email to see it here!")
    else:
        st.markdown(f"**Found {len(logs)} email(s)**")
        st.markdown("---")
        
        for idx, log in enumerate(logs):
            with st.expander(
                f"**{log['recipient']}** - {log['subject_context']} "
                f"({'⭐ Favorite' if log['is_favorite'] else ''}) - "
                f"{datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d %H:%M')}",
                expanded=False
            ):
                # Header with metadata
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Tone", log['tone'])
                with col2:
                    st.metric("Length", log['length'])
                with col3:
                    st.metric("Cost", f"${log.get('cost_estimate', 0):.4f}")
                with col4:
                    is_fav = bool(log['is_favorite'])
                    fav_btn_label = "⭐ Unfavorite" if is_fav else "☆ Favorite"
                    if st.button(fav_btn_label, key=f"fav_{log['id']}"):
                        try:
                            toggle_favorite(log['id'])
                            st.rerun()
                        except DatabaseError as e:
                            st.error(f"Error toggling favorite: {e}")
                
                st.markdown("---")
                
                # Email details
                st.markdown("### 📋 Details")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Recipient:** {log['recipient']}")
                    st.markdown(f"**Purpose:** {log['purpose']}")
                with col2:
                    st.markdown(f"**Context:** {log['subject_context']}")
                    st.markdown(f"**Generated:** {datetime.fromisoformat(log['timestamp']).strftime('%B %d, %Y at %I:%M %p')}")
                
                if log['bullet_points']:
                    st.markdown("**Key Points:**")
                    bullet_points = log['bullet_points'].split('; ')
                    st.markdown(format_bullet_points(bullet_points))
                
                if log['additional_notes']:
                    st.markdown(f"**Additional Notes:** {log['additional_notes']}")
                
                st.markdown("---")
                
                # Subject lines
                st.markdown("### 📬 Subject Lines")
                subjects = log['subjects'].split('; ')
                for i, subj in enumerate(subjects, 1):
                    col1, col2 = st.columns([10, 1])
                    with col1:
                        st.markdown(f"{i}. {subj}")
                    with col2:
                        if st.button("📋", key=f"copy_subj_{log['id']}_{i}", help="Copy"):
                            st.code(subj, language=None)
                
                st.markdown("---")
                
                # Email drafts
                st.markdown("### ✉️ Email Drafts")
                
                tab1, tab2 = st.tabs(["📄 Draft 1", "📄 Draft 2"])
                
                with tab1:
                    if log['draft1']:
                        st.text_area(
                            "Draft 1",
                            value=log['draft1'],
                            height=300,
                            key=f"draft1_{log['id']}"
                        )
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("📋 Copy", key=f"copy_d1_{log['id']}"):
                                st.code(log['draft1'], language=None)
                        with col2:
                            # Download as TXT
                            st.download_button(
                                label="💾 Download TXT",
                                data=log['draft1'],
                                file_name=f"email_{log['id']}_draft1.txt",
                                mime="text/plain",
                                key=f"dl_txt_d1_{log['id']}"
                            )
                        with col3:
                            # Download as HTML
                            try:
                                html_content = export_to_html(
                                    subjects[0] if subjects else "Email",
                                    log['draft1'],
                                    log['recipient'],
                                    "temp",
                                    "exports"
                                )
                                with open(html_content, 'r') as f:
                                    html_data = f.read()
                                st.download_button(
                                    label="🌐 Download HTML",
                                    data=html_data,
                                    file_name=f"email_{log['id']}_draft1.html",
                                    mime="text/html",
                                    key=f"dl_html_d1_{log['id']}"
                                )
                            except Exception as e:
                                logger.error(f"Error creating HTML export: {e}")
                
                with tab2:
                    if log['draft2']:
                        st.text_area(
                            "Draft 2",
                            value=log['draft2'],
                            height=300,
                            key=f"draft2_{log['id']}"
                        )
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("📋 Copy", key=f"copy_d2_{log['id']}"):
                                st.code(log['draft2'], language=None)
                        with col2:
                            st.download_button(
                                label="💾 Download TXT",
                                data=log['draft2'],
                                file_name=f"email_{log['id']}_draft2.txt",
                                mime="text/plain",
                                key=f"dl_txt_d2_{log['id']}"
                            )
                        with col3:
                            try:
                                html_content = export_to_html(
                                    subjects[0] if subjects else "Email",
                                    log['draft2'],
                                    log['recipient'],
                                    "temp",
                                    "exports"
                                )
                                with open(html_content, 'r') as f:
                                    html_data = f.read()
                                st.download_button(
                                    label="🌐 Download HTML",
                                    data=html_data,
                                    file_name=f"email_{log['id']}_draft2.html",
                                    mime="text/html",
                                    key=f"dl_html_d2_{log['id']}"
                                )
                            except Exception as e:
                                logger.error(f"Error creating HTML export: {e}")
                
                st.markdown("---")
                
                # Delete button
                if st.button("🗑️ Delete This Email", key=f"del_{log['id']}", type="secondary"):
                    try:
                        delete_email_log(log['id'])
                        st.success("Email deleted successfully!")
                        st.rerun()
                    except DatabaseError as e:
                        st.error(f"Error deleting email: {e}")
                        logger.error(f"Error deleting log {log['id']}: {e}")

except DatabaseError as e:
    st.error(f"❌ Database Error: {e}")
    logger.error(f"Database error in history page: {e}")
except Exception as e:
    st.error(f"❌ Unexpected Error: {e}")
    logger.error(f"Unexpected error in history page: {e}", exc_info=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>💡 Tip: Use the sidebar to filter by favorites and adjust the number of results</p>
    </div>
    """,
    unsafe_allow_html=True
)

