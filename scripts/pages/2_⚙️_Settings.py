"""
Settings Page - Configuration and preferences
"""
import sys
sys.path.append('../scripts')
sys.path.append('.')

import streamlit as st
import os
from pathlib import Path
from config import (
    OPENAI_MODEL,
    OPENAI_MAX_TOKENS,
    OPENAI_TEMPERATURE,
    DB_PATH,
    LOG_LEVEL,
    DATA_PATH
)
from db import get_email_logs, get_total_cost
from logger import setup_logger

logger = setup_logger(__name__)

# Page config
st.set_page_config(
    page_title="Settings - AI Email Generator",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Settings & Configuration")
st.markdown("Configure your AI Email Generator preferences and view system information.")

# Tabs for different settings sections
tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Settings", "💰 Cost Tracking", "📊 Statistics", "ℹ️ System Info"])

with tab1:
    st.header("AI Model Configuration")
    st.markdown("Current AI settings (read from environment):")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Model", OPENAI_MODEL)
        st.metric("Max Tokens", OPENAI_MAX_TOKENS)
        st.metric("Temperature", OPENAI_TEMPERATURE)
        
        st.markdown("---")
        
        st.markdown("### 📝 Model Information")
        st.markdown("""
        **GPT-3.5-turbo**: Fast and cost-effective
        - ✅ Good for most use cases
        - ✅ Low cost (~$0.003-0.007 per email)
        - ⚡ Fast response times
        
        **GPT-4**: Higher quality, more expensive
        - ✅ Best quality outputs
        - ⚠️ Higher cost (~$0.06-0.14 per email)
        - ⏱️ Slower response times
        """)
    
    with col2:
        st.markdown("### 🔧 Temperature Guide")
        st.markdown("""
        **Temperature** controls randomness in outputs:
        
        - **0.0-0.3**: Very focused and deterministic
        - **0.4-0.7**: Balanced (recommended)
        - **0.8-1.0**: More creative and varied
        
        Current setting: **{:.1f}** {}
        """.format(
            OPENAI_TEMPERATURE,
            "✅" if 0.4 <= OPENAI_TEMPERATURE <= 0.7 else "⚠️"
        ))
        
        st.markdown("### 🎯 Max Tokens Guide")
        st.markdown("""
        **Max Tokens** limits response length:
        
        - **100-200**: Very short emails
        - **200-400**: Medium emails (recommended)
        - **400-600**: Long, detailed emails
        
        Current setting: **{}** tokens
        """.format(OPENAI_MAX_TOKENS))
    
    st.markdown("---")
    st.info("💡 **To change these settings**, edit the `.env` file in your project root and restart the application.")
    
    with st.expander("📖 How to modify settings"):
        st.markdown("""
        1. Open `.env` file in your project root
        2. Modify the desired values:
           ```
           OPENAI_MODEL=gpt-4
           OPENAI_MAX_TOKENS=500
           OPENAI_TEMPERATURE=0.8
           ```
        3. Save the file
        4. Restart the Streamlit application
        """)

with tab2:
    st.header("💰 Cost Tracking")
    
    try:
        all_logs = get_email_logs(limit=1000)
        total_cost = get_total_cost()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Emails", len(all_logs))
        with col2:
            st.metric("Total Cost", f"${total_cost:.4f}")
        with col3:
            avg_cost = total_cost / len(all_logs) if all_logs else 0
            st.metric("Avg Cost/Email", f"${avg_cost:.4f}")
        with col4:
            # Estimate monthly cost if continuing at current rate
            if all_logs and len(all_logs) > 1:
                # Calculate emails per day
                first_date = all_logs[-1]['timestamp']
                last_date = all_logs[0]['timestamp']
                from datetime import datetime
                days = (datetime.fromisoformat(last_date) - datetime.fromisoformat(first_date)).days + 1
                emails_per_day = len(all_logs) / days if days > 0 else 0
                monthly_est = emails_per_day * 30 * avg_cost
                st.metric("Est. Monthly", f"${monthly_est:.2f}")
            else:
                st.metric("Est. Monthly", "N/A")
        
        st.markdown("---")
        
        # Cost breakdown
        st.markdown("### 📊 Cost Breakdown")
        
        if all_logs:
            import pandas as pd
            from datetime import datetime
            
            # Prepare data
            df_data = []
            for log in all_logs:
                date = datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d')
                df_data.append({
                    'Date': date,
                    'Cost': log.get('cost_estimate', 0),
                    'Recipient': log['recipient']
                })
            
            df = pd.DataFrame(df_data)
            
            # Daily costs
            daily_costs = df.groupby('Date')['Cost'].sum().reset_index()
            daily_costs['Cost'] = daily_costs['Cost'].round(4)
            
            st.markdown("**Daily Costs:**")
            st.dataframe(daily_costs, use_container_width=True)
            
            # Bar chart
            st.bar_chart(daily_costs.set_index('Date')['Cost'])
        else:
            st.info("No cost data available yet. Generate some emails to see cost tracking!")
        
        st.markdown("---")
        
        # Cost optimization tips
        with st.expander("💡 Cost Optimization Tips"):
            st.markdown("""
            1. **Use GPT-3.5-turbo** for most use cases (20x cheaper than GPT-4)
            2. **Reduce max_tokens** if you need shorter emails
            3. **Batch similar emails** to reduce context switching
            4. **Review and reuse** good drafts instead of regenerating
            5. **Use favorites** to mark best results for future reference
            
            **Price Comparison:**
            - GPT-3.5-turbo: ~$0.003-0.007 per email
            - GPT-4: ~$0.06-0.14 per email
            """)
    
    except Exception as e:
        st.error(f"Error loading cost data: {e}")
        logger.error(f"Error in cost tracking: {e}", exc_info=True)

with tab3:
    st.header("📊 Usage Statistics")
    
    try:
        all_logs = get_email_logs(limit=1000)
        
        if not all_logs:
            st.info("No statistics available yet. Generate some emails first!")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📈 General Stats")
                st.metric("Total Emails Generated", len(all_logs))
                st.metric("Favorite Emails", len([l for l in all_logs if l['is_favorite']]))
                
                # Most common tone
                tones = [log['tone'] for log in all_logs]
                from collections import Counter
                most_common_tone = Counter(tones).most_common(1)[0] if tones else ("N/A", 0)
                st.metric("Most Used Tone", f"{most_common_tone[0]} ({most_common_tone[1]})")
                
                # Most common length
                lengths = [log['length'] for log in all_logs]
                most_common_length = Counter(lengths).most_common(1)[0] if lengths else ("N/A", 0)
                st.metric("Most Used Length", f"{most_common_length[0]} ({most_common_length[1]})")
            
            with col2:
                st.markdown("### 📅 Timeline")
                from datetime import datetime
                
                first_email = datetime.fromisoformat(all_logs[-1]['timestamp'])
                last_email = datetime.fromisoformat(all_logs[0]['timestamp'])
                
                st.metric("First Email", first_email.strftime('%Y-%m-%d'))
                st.metric("Latest Email", last_email.strftime('%Y-%m-%d'))
                
                days_active = (last_email - first_email).days + 1
                st.metric("Days Active", days_active)
                
                emails_per_day = len(all_logs) / days_active if days_active > 0 else 0
                st.metric("Avg Emails/Day", f"{emails_per_day:.1f}")
            
            st.markdown("---")
            
            # Distribution charts
            st.markdown("### 📊 Distributions")
            
            import pandas as pd
            
            # Tone distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Tone Distribution:**")
                tone_counts = pd.Series(tones).value_counts()
                st.bar_chart(tone_counts)
            
            with col2:
                st.markdown("**Length Distribution:**")
                length_counts = pd.Series(lengths).value_counts()
                st.bar_chart(length_counts)
    
    except Exception as e:
        st.error(f"Error loading statistics: {e}")
        logger.error(f"Error in statistics: {e}", exc_info=True)

with tab4:
    st.header("ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📁 Paths")
        st.code(f"Database: {DB_PATH}", language=None)
        st.code(f"Data: {DATA_PATH}", language=None)
        
        # Check if files exist
        db_exists = "✅" if os.path.exists(DB_PATH) else "❌"
        data_exists = "✅" if os.path.exists(DATA_PATH) else "❌"
        
        st.markdown(f"**Database exists:** {db_exists}")
        st.markdown(f"**Data file exists:** {data_exists}")
        
        if os.path.exists(DB_PATH):
            db_size = os.path.getsize(DB_PATH) / 1024  # KB
            st.markdown(f"**Database size:** {db_size:.2f} KB")
    
    with col2:
        st.markdown("### ⚙️ Configuration")
        st.code(f"Log Level: {LOG_LEVEL}", language=None)
        st.code(f"Model: {OPENAI_MODEL}", language=None)
        
        # Environment check
        api_key_set = "✅" if os.getenv("OPENAI_API_KEY") else "❌"
        st.markdown(f"**API Key configured:** {api_key_set}")
    
    st.markdown("---")
    
    # Version info
    st.markdown("### 📦 Version Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        import streamlit as st_version
        st.metric("Streamlit", st_version.__version__)
    
    with col2:
        import openai
        st.metric("OpenAI", openai.__version__)
    
    with col3:
        import sys
        st.metric("Python", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### 🔧 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗂️ Open Logs Folder", help="View application logs"):
            logs_path = Path("../logs")
            st.info(f"Logs are located at: {logs_path.absolute()}")
    
    with col2:
        if st.button("📊 Open Database", help="View database location"):
            st.info(f"Database file: {DB_PATH}")
    
    with col3:
        if st.button("♻️ Clear Cache", help="Clear Streamlit cache"):
            st.cache_data.clear()
            st.success("Cache cleared successfully!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>AI Email Generator v1.0 | Built with ❤️ using Streamlit and OpenAI</p>
    </div>
    """,
    unsafe_allow_html=True
)

