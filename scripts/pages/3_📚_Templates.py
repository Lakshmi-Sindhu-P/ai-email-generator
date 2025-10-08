"""
Templates Page - Manage and use email templates
"""
import sys
sys.path.append('../scripts')
sys.path.append('.')

import streamlit as st
import json
from pathlib import Path
from typing import List, Dict
from logger import setup_logger

logger = setup_logger(__name__)

# Page config
st.set_page_config(
    page_title="Templates - AI Email Generator",
    page_icon="📚",
    layout="wide"
)

# Template storage file
TEMPLATES_FILE = Path("../data/email_templates.json")
TEMPLATES_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_templates() -> List[Dict]:
    """Load templates from JSON file."""
    try:
        if TEMPLATES_FILE.exists():
            with open(TEMPLATES_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"Error loading templates: {e}")
        return []


def save_templates(templates: List[Dict]) -> None:
    """Save templates to JSON file."""
    try:
        with open(TEMPLATES_FILE, 'w') as f:
            json.dump(templates, indent=2, fp=f)
        logger.info("Templates saved successfully")
    except Exception as e:
        logger.error(f"Error saving templates: {e}")
        raise


st.title("📚 Email Templates")
st.markdown("Create, manage, and use email templates for faster generation.")

# Load existing templates
templates = load_templates()

# Tabs for different actions
tab1, tab2, tab3 = st.tabs(["➕ Create Template", "📋 My Templates", "🔧 Preset Templates"])

with tab1:
    st.header("➕ Create New Template")
    st.markdown("Save commonly used email patterns as templates for quick reuse.")
    
    with st.form("create_template"):
        template_name = st.text_input(
            "Template Name *",
            placeholder="e.g., Meeting Follow-up",
            help="A descriptive name for this template"
        )
        
        template_category = st.selectbox(
            "Category",
            ["Business", "Personal", "Sales", "Support", "Marketing", "Other"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            default_tone = st.selectbox(
                "Default Tone",
                ["Professional", "Friendly", "Formal", "Casual", "Persuasive", "Enthusiastic"]
            )
        
        with col2:
            default_length = st.selectbox(
                "Default Length",
                ["Short", "Medium", "Long"]
            )
        
        subject_template = st.text_input(
            "Subject Template",
            placeholder="e.g., Follow-up: {topic}",
            help="Use {placeholders} for variable content"
        )
        
        body_template = st.text_area(
            "Body Template *",
            height=200,
            placeholder="Dear {recipient},\n\nThank you for...",
            help="Use {placeholders} for variable parts"
        )
        
        key_points_template = st.text_area(
            "Default Key Points (one per line)",
            height=100,
            placeholder="Point 1\nPoint 2\nPoint 3"
        )
        
        template_notes = st.text_area(
            "Notes",
            height=60,
            placeholder="Additional notes about when to use this template..."
        )
        
        submit = st.form_submit_button("💾 Save Template", type="primary")
        
        if submit:
            if not template_name or not body_template:
                st.error("⚠️ Please fill in required fields (Name and Body)")
            else:
                # Create new template
                new_template = {
                    "id": len(templates) + 1,
                    "name": template_name,
                    "category": template_category,
                    "tone": default_tone,
                    "length": default_length,
                    "subject": subject_template,
                    "body": body_template,
                    "key_points": [kp.strip() for kp in key_points_template.split('\n') if kp.strip()],
                    "notes": template_notes,
                    "uses": 0
                }
                
                templates.append(new_template)
                save_templates(templates)
                
                st.success(f"✅ Template '{template_name}' created successfully!")
                st.balloons()

with tab2:
    st.header("📋 My Templates")
    
    if not templates:
        st.info("📭 No templates yet. Create your first template in the 'Create Template' tab!")
    else:
        # Filter by category
        categories = list(set(t['category'] for t in templates))
        selected_category = st.selectbox(
            "Filter by Category",
            ["All"] + sorted(categories)
        )
        
        filtered_templates = templates if selected_category == "All" else [
            t for t in templates if t['category'] == selected_category
        ]
        
        st.markdown(f"**Showing {len(filtered_templates)} template(s)**")
        st.markdown("---")
        
        for template in filtered_templates:
            with st.expander(
                f"**{template['name']}** ({template['category']}) - Used {template['uses']} times",
                expanded=False
            ):
                # Template details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Tone", template['tone'])
                with col2:
                    st.metric("Length", template['length'])
                with col3:
                    st.metric("Times Used", template['uses'])
                
                st.markdown("---")
                
                st.markdown("### 📝 Template Content")
                
                if template['subject']:
                    st.markdown(f"**Subject:** `{template['subject']}`")
                
                st.markdown("**Body:**")
                st.code(template['body'], language=None)
                
                if template['key_points']:
                    st.markdown("**Default Key Points:**")
                    for kp in template['key_points']:
                        st.markdown(f"• {kp}")
                
                if template['notes']:
                    st.markdown(f"**Notes:** {template['notes']}")
                
                st.markdown("---")
                
                # Actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📋 Use Template", key=f"use_{template['id']}"):
                        # Increment use counter
                        for t in templates:
                            if t['id'] == template['id']:
                                t['uses'] += 1
                        save_templates(templates)
                        
                        st.success("✅ Template applied! Go to the main page to generate.")
                        st.session_state['selected_template'] = template
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{template['id']}"):
                        st.info("Edit functionality coming soon!")
                
                with col3:
                    if st.button("🗑️ Delete", key=f"del_{template['id']}", type="secondary"):
                        templates = [t for t in templates if t['id'] != template['id']]
                        save_templates(templates)
                        st.success("Template deleted!")
                        st.rerun()

with tab3:
    st.header("🔧 Preset Templates")
    st.markdown("Ready-to-use templates for common scenarios.")
    
    preset_templates = [
        {
            "name": "Meeting Follow-up",
            "category": "Business",
            "description": "Follow up after a meeting with action items",
            "body": """Dear {recipient},

Thank you for taking the time to meet with me {when}. I appreciated the opportunity to discuss {topic}.

As we discussed, here are the key action items:
{action_items}

I'll {my_action} and will follow up with you {timeline}.

Please let me know if you have any questions or need any clarification.

Best regards"""
        },
        {
            "name": "Introduction/Networking",
            "category": "Business",
            "description": "Introduce yourself to a new contact",
            "body": """Dear {recipient},

I hope this email finds you well. My name is {your_name} and I'm {your_role}.

I came across your {where_found} and was impressed by {what_impressed}. I'm reaching out because {reason}.

I'd love to {request} if you have time. {additional_context}

Thank you for considering my request. I look forward to hearing from you.

Best regards"""
        },
        {
            "name": "Thank You Note",
            "category": "Personal",
            "description": "Express gratitude professionally",
            "body": """Dear {recipient},

I wanted to take a moment to thank you for {what_for}.

{specific_impact}

Your {quality} made a real difference, and I'm grateful for {specific_thing}.

Thank you again, and I hope we can {future_action}.

Warm regards"""
        },
        {
            "name": "Request for Information",
            "category": "Business",
            "description": "Ask for information or clarification",
            "body": """Dear {recipient},

I hope you're doing well. I'm writing to request some information regarding {topic}.

Specifically, I'm interested in:
{questions}

This information would help me {purpose}. If possible, I would appreciate a response by {deadline}.

Thank you for your time and assistance.

Best regards"""
        },
        {
            "name": "Apology/Correction",
            "category": "Business",
            "description": "Apologize or correct a mistake",
            "body": """Dear {recipient},

I'm writing to sincerely apologize for {what_happened}.

I understand that {impact}, and I take full responsibility for {mistake}.

To make this right, I will {corrective_action}. Additionally, {preventive_measures}.

Thank you for your patience and understanding. Please let me know if there's anything else I can do.

Sincerely"""
        }
    ]
    
    for preset in preset_templates:
        with st.expander(f"**{preset['name']}** - {preset['description']}", expanded=False):
            st.markdown(f"**Category:** {preset['category']}")
            st.markdown("**Template:**")
            st.code(preset['body'], language=None)
            
            if st.button("➕ Add to My Templates", key=f"add_preset_{preset['name']}"):
                new_template = {
                    "id": len(templates) + 1,
                    "name": preset['name'],
                    "category": preset['category'],
                    "tone": "Professional",
                    "length": "Medium",
                    "subject": "",
                    "body": preset['body'],
                    "key_points": [],
                    "notes": preset['description'],
                    "uses": 0
                }
                
                templates.append(new_template)
                save_templates(templates)
                st.success(f"✅ '{preset['name']}' added to your templates!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>💡 Tip: Templates help you generate consistent emails faster. Use placeholders like {recipient} for customization.</p>
    </div>
    """,
    unsafe_allow_html=True
)

