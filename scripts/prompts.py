"""
Prompt templates for email and subject line generation.
Constructs prompts based on user inputs.
"""
from typing import Dict, List


def build_subject_prompt(inputs: Dict[str, any]) -> str:
    """
    Build a prompt for generating email subject lines.
    
    Args:
        inputs: Dictionary containing:
            - recipient: Name/title of email recipient
            - subject_context: Context for the email
            - tone: Desired tone (Professional, Friendly, etc.)
            - purpose: Main purpose/action of the email
            - bullet_points: List of key points to cover
            
    Returns:
        Formatted prompt string for subject line generation
    """
    bullet_points_str = ', '.join(inputs.get('bullet_points', []))
    
    prompt = f"""Generate 5 distinct, compelling email subject lines for the following context:

Recipient: {inputs.get('recipient', 'N/A')}
Context: {inputs.get('subject_context', 'N/A')}
Tone: {inputs.get('tone', 'Professional')}
Purpose: {inputs.get('purpose', 'N/A')}
Key Points: {bullet_points_str}

Requirements:
- Each subject line should be concise (under 60 characters)
- Make them engaging and action-oriented
- Vary the approach (direct, question-based, benefit-focused, etc.)
- Match the specified tone
- Ensure they accurately reflect the email's purpose

Please provide exactly 5 subject lines, numbered 1-5."""
    
    return prompt


def build_email_prompt(inputs: Dict[str, any], variation: int = 1, template: str = "") -> str:
    """
    Build a prompt for generating an email draft.
    
    Args:
        inputs: Dictionary containing email parameters:
            - recipient: Name/title of email recipient
            - subject_context: Context for the email
            - tone: Desired tone
            - purpose: Main purpose/action
            - bullet_points: List of key points
            - length: Desired length (Short/Medium/Long)
            - additional_notes: Any extra instructions
        variation: Draft variation number (1-n) to generate different styles
        template: Optional template to base the email on
        
    Returns:
        Formatted prompt string for email generation
    """
    bullet_points_str = '\n'.join([f"- {point}" for point in inputs.get('bullet_points', [])])
    length = inputs.get('length', 'Medium')
    
    # Define length guidelines
    length_guide = {
        'Short': '2-3 paragraphs (approximately 100-150 words)',
        'Medium': '3-4 paragraphs (approximately 200-300 words)',
        'Long': '4-6 paragraphs (approximately 350-500 words)'
    }
    
    # Define variation styles
    if variation == 1:
        style_instruction = (
            "Write a concise, professional, and friendly email. "
            "Use a warm greeting, clear structure, and a polite closing. "
            "Focus on clarity and directness."
        )
    else:
        style_instruction = (
            "Write a more formal and thorough email with detailed explanations. "
            "Use a formal greeting, provide comprehensive context, "
            "and include a professional closing with clear next steps."
        )
    
    prompt = f"""Write a professional email with the following specifications:

RECIPIENT: {inputs.get('recipient', 'N/A')}
CONTEXT: {inputs.get('subject_context', 'N/A')}
TONE: {inputs.get('tone', 'Professional')}
PURPOSE: {inputs.get('purpose', 'N/A')}

KEY POINTS TO INCLUDE:
{bullet_points_str}

LENGTH: {length} - {length_guide.get(length, length_guide['Medium'])}

ADDITIONAL NOTES: {inputs.get('additional_notes', 'None')}

STYLE GUIDANCE:
{style_instruction}
"""

    if template:
        prompt += f"""
TEMPLATE REFERENCE:
Use the following as a structural reference (not to copy verbatim):
{template}
"""

    prompt += """

REQUIREMENTS:
- Use appropriate greeting and closing
- Maintain the specified tone throughout
- Include all key points naturally
- Use proper email formatting
- Be clear, concise, and professional
- Ensure proper grammar and punctuation
- Add a clear call-to-action if applicable

Please write the complete email now:"""
    
    return prompt


def validate_inputs(inputs: Dict[str, any]) -> tuple[bool, str]:
    """
    Validate user inputs before generating emails.
    
    Args:
        inputs: Dictionary containing user inputs
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['recipient', 'subject_context', 'tone', 'purpose', 'bullet_points']
    
    for field in required_fields:
        if field not in inputs or not inputs[field]:
            return False, f"Missing required field: {field}"
    
    # Validate bullet points is a list
    if not isinstance(inputs.get('bullet_points', []), list):
        return False, "Bullet points must be a list"
    
    if len(inputs.get('bullet_points', [])) == 0:
        return False, "At least one bullet point is required"
    
    # Validate tone
    valid_tones = ["Professional", "Friendly", "Formal", "Casual", "Persuasive", "Enthusiastic", "Other"]
    if inputs.get('tone') not in valid_tones:
        return False, f"Invalid tone. Must be one of: {', '.join(valid_tones)}"
    
    # Validate length
    valid_lengths = ["Short", "Medium", "Long"]
    if inputs.get('length') not in valid_lengths:
        return False, f"Invalid length. Must be one of: {', '.join(valid_lengths)}"
    
    return True, ""
