"""
Compare Page - Side-by-side comparison of email drafts
"""
import sys
sys.path.append('../scripts')
sys.path.append('.')

import streamlit as st
from db import get_email_logs
from logger import setup_logger
from datetime import datetime

logger = setup_logger(__name__)

# Page config
st.set_page_config(
    page_title="Compare Drafts - AI Email Generator",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 Compare Email Drafts")
st.markdown("View and compare multiple email drafts side-by-side to choose the best one.")

# Get recent emails for comparison
try:
    recent_logs = get_email_logs(limit=20)
    
    if not recent_logs:
        st.info("📭 No emails to compare. Generate some emails first!")
    else:
        st.header("Select Emails to Compare")
        
        # Create selection options
        email_options = {
            f"{log['recipient']} - {log['subject_context']} ({datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d %H:%M')})": log
            for log in recent_logs
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected1 = st.selectbox(
                "First Email",
                options=list(email_options.keys()),
                key="email1"
            )
        
        with col2:
            selected2 = st.selectbox(
                "Second Email",
                options=list(email_options.keys()),
                key="email2",
                index=min(1, len(email_options) - 1)
            )
        
        if st.button("📊 Compare Selected Emails", type="primary"):
            email1 = email_options[selected1]
            email2 = email_options[selected2]
            
            st.markdown("---")
            st.header("📊 Comparison Results")
            
            # Metadata comparison
            st.subheader("📋 Metadata Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Email 1")
                st.metric("Recipient", email1['recipient'])
                st.metric("Tone", email1['tone'])
                st.metric("Length", email1['length'])
                st.metric("Cost", f"${email1.get('cost_estimate', 0):.4f}")
                if email1['is_favorite']:
                    st.markdown("⭐ **Favorite**")
            
            with col2:
                st.markdown("### Email 2")
                st.metric("Recipient", email2['recipient'])
                st.metric("Tone", email2['tone'])
                st.metric("Length", email2['length'])
                st.metric("Cost", f"${email2.get('cost_estimate', 0):.4f}")
                if email2['is_favorite']:
                    st.markdown("⭐ **Favorite**")
            
            st.markdown("---")
            
            # Subject lines comparison
            st.subheader("📬 Subject Lines Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Email 1 Subjects")
                subjects1 = email1['subjects'].split('; ')
                for i, subj in enumerate(subjects1, 1):
                    st.markdown(f"{i}. {subj}")
            
            with col2:
                st.markdown("### Email 2 Subjects")
                subjects2 = email2['subjects'].split('; ')
                for i, subj in enumerate(subjects2, 1):
                    st.markdown(f"{i}. {subj}")
            
            st.markdown("---")
            
            # Draft comparison tabs
            st.subheader("✉️ Draft Comparison")
            
            draft_tab1, draft_tab2 = st.tabs(["📄 Draft 1 Comparison", "📄 Draft 2 Comparison"])
            
            with draft_tab1:
                st.markdown("### Comparing First Drafts")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Email 1 - Draft 1**")
                    st.text_area(
                        "Draft 1",
                        value=email1['draft1'],
                        height=400,
                        key="compare_e1_d1",
                        disabled=True
                    )
                    
                    # Stats
                    words1 = len(email1['draft1'].split())
                    chars1 = len(email1['draft1'])
                    st.caption(f"📊 {words1} words | {chars1} characters")
                
                with col2:
                    st.markdown("**Email 2 - Draft 1**")
                    st.text_area(
                        "Draft 1",
                        value=email2['draft1'],
                        height=400,
                        key="compare_e2_d1",
                        disabled=True
                    )
                    
                    # Stats
                    words2 = len(email2['draft1'].split())
                    chars2 = len(email2['draft1'])
                    st.caption(f"📊 {words2} words | {chars2} characters")
                
                # Comparison insights
                st.markdown("---")
                st.markdown("#### 📈 Comparison Insights")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    word_diff = abs(words1 - words2)
                    st.metric("Word Count Difference", word_diff)
                
                with col2:
                    longer = "Email 1" if words1 > words2 else "Email 2"
                    st.metric("Longer Draft", longer)
                
                with col3:
                    avg_word_length1 = chars1 / words1 if words1 > 0 else 0
                    avg_word_length2 = chars2 / words2 if words2 > 0 else 0
                    more_detailed = "Email 1" if avg_word_length1 > avg_word_length2 else "Email 2"
                    st.metric("More Detailed", more_detailed)
            
            with draft_tab2:
                st.markdown("### Comparing Second Drafts")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Email 1 - Draft 2**")
                    st.text_area(
                        "Draft 2",
                        value=email1['draft2'],
                        height=400,
                        key="compare_e1_d2",
                        disabled=True
                    )
                    
                    # Stats
                    words1 = len(email1['draft2'].split())
                    chars1 = len(email1['draft2'])
                    st.caption(f"📊 {words1} words | {chars1} characters")
                
                with col2:
                    st.markdown("**Email 2 - Draft 2**")
                    st.text_area(
                        "Draft 2",
                        value=email2['draft2'],
                        height=400,
                        key="compare_e2_d2",
                        disabled=True
                    )
                    
                    # Stats
                    words2 = len(email2['draft2'].split())
                    chars2 = len(email2['draft2'])
                    st.caption(f"📊 {words2} words | {chars2} characters")
                
                # Comparison insights
                st.markdown("---")
                st.markdown("#### 📈 Comparison Insights")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    word_diff = abs(words1 - words2)
                    st.metric("Word Count Difference", word_diff)
                
                with col2:
                    longer = "Email 1" if words1 > words2 else "Email 2"
                    st.metric("Longer Draft", longer)
                
                with col3:
                    avg_word_length1 = chars1 / words1 if words1 > 0 else 0
                    avg_word_length2 = chars2 / words2 if words2 > 0 else 0
                    more_detailed = "Email 1" if avg_word_length1 > avg_word_length2 else "Email 2"
                    st.metric("More Detailed", more_detailed)
            
            # Recommendations
            st.markdown("---")
            st.subheader("💡 Recommendations")
            
            recommendations = []
            
            # Tone-based recommendation
            if email1['tone'] == 'Professional' and email2['tone'] == 'Friendly':
                recommendations.append("🎯 Email 1 (Professional) is better for formal business contexts. Email 2 (Friendly) works well for existing relationships.")
            
            # Length-based recommendation
            if email1['length'] != email2['length']:
                recommendations.append(f"📏 Email 1 is {email1['length']} length while Email 2 is {email2['length']}. Choose based on your recipient's preferences.")
            
            # Favorite-based recommendation
            if email1['is_favorite'] and not email2['is_favorite']:
                recommendations.append("⭐ You previously marked Email 1 as a favorite, suggesting it performed well.")
            elif email2['is_favorite'] and not email1['is_favorite']:
                recommendations.append("⭐ You previously marked Email 2 as a favorite, suggesting it performed well.")
            
            # Cost consideration
            if email1.get('cost_estimate', 0) != email2.get('cost_estimate', 0):
                cheaper = "Email 1" if email1.get('cost_estimate', 0) < email2.get('cost_estimate', 0) else "Email 2"
                recommendations.append(f"💰 {cheaper} was more cost-effective to generate.")
            
            if recommendations:
                for rec in recommendations:
                    st.markdown(f"• {rec}")
            else:
                st.markdown("Both emails have similar characteristics. Choose based on specific content preference.")

except Exception as e:
    st.error(f"❌ Error: {e}")
    logger.error(f"Error in compare page: {e}", exc_info=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>💡 Tip: Compare different tones and lengths to understand what works best for your needs</p>
    </div>
    """,
    unsafe_allow_html=True
)

