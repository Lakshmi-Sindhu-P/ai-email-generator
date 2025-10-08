"""
Prompt templates for email and subject line generation.
Constructs prompts based on user inputs.
"""
from typing import Dict, List


def _get_style_instruction_for_tone(tone: str, variation: int) -> str:
    """
    Get style instructions for a specific tone.
    
    Args:
        tone: The tone to use
        variation: Variation number for slight differences
        
    Returns:
        Style instruction string
    """
    tone_instructions = {
        'Professional': (
            "Write in a professional manner with clear, direct language. "
            "Use proper business etiquette, maintain formality, and focus on efficiency. "
            "Include a professional greeting and closing."
        ),
        'Friendly': (
            "Write in a warm, friendly manner that builds rapport. "
            "Use conversational language while remaining appropriate. "
            "Include a warm greeting and friendly closing. Show enthusiasm where appropriate."
        ),
        'Formal': (
            "Write in a highly formal, respectful manner. "
            "Use formal language, avoid contractions, and maintain a serious tone. "
            "Include proper formal salutations and closings. Be thorough and detailed."
        ),
        'Casual': (
            "Write in a relaxed, casual manner. "
            "Use everyday language and be conversational. "
            "Keep it light and approachable while staying on topic."
        ),
        'Persuasive': (
            "Write persuasively to convince the recipient. "
            "Use compelling arguments, emphasize benefits, and include clear calls-to-action. "
            "Be convincing while remaining genuine and respectful."
        ),
        'Enthusiastic': (
            "Write with energy and enthusiasm. "
            "Show excitement about the topic, use dynamic language, and convey positivity. "
            "Be engaging and motivating while staying professional."
        ),
        'Empathetic': (
            "Write with empathy and understanding. "
            "Show that you understand the recipient's perspective, feelings, or situation. "
            "Use compassionate language and demonstrate genuine care and concern."
        ),
        'Assertive': (
            "Write with confidence and directness. "
            "Be clear about your position or needs while remaining respectful. "
            "Use strong, decisive language without being aggressive."
        ),
        'Apologetic': (
            "Write with sincerity and regret where appropriate. "
            "Take responsibility, acknowledge the issue, and offer solutions. "
            "Be genuine in your apology without over-apologizing or being defensive."
        ),
        'Grateful': (
            "Write with appreciation and thankfulness. "
            "Express genuine gratitude for the recipient's time, effort, or contribution. "
            "Make them feel valued and recognized."
        ),
        'Urgent': (
            "Write with a sense of urgency and importance. "
            "Clearly communicate time-sensitivity without being alarmist. "
            "Use action-oriented language and specify deadlines or immediate needs."
        ),
        'Diplomatic': (
            "Write with tact and diplomacy. "
            "Navigate sensitive topics carefully, consider multiple perspectives. "
            "Use neutral language that avoids offense while still being clear."
        ),
        'Confident': (
            "Write with self-assurance and authority. "
            "Demonstrate expertise and certainty in your message. "
            "Use strong, positive language while avoiding arrogance."
        ),
        'Humble': (
            "Write with humility and modesty. "
            "Acknowledge limitations, give credit to others, and show openness to feedback. "
            "Be respectful and self-aware without diminishing your message."
        ),
        'Motivational': (
            "Write to inspire and energize the recipient. "
            "Use uplifting language, highlight possibilities, and encourage action. "
            "Be positive and empowering while staying genuine."
        ),
        'Informative': (
            "Write to educate and inform clearly. "
            "Focus on delivering information in an organized, easy-to-understand way. "
            "Be thorough, accurate, and objective in your presentation."
        ),
        'Reassuring': (
            "Write to provide comfort and confidence. "
            "Address concerns proactively, emphasize stability and support. "
            "Use calming language that builds trust and reduces anxiety."
        ),
        'Compassionate': (
            "Write with deep care and concern for the recipient's situation. "
            "Show genuine sympathy, especially in difficult circumstances. "
            "Be supportive, understanding, and human in your approach."
        ),
        'Authoritative': (
            "Write as a subject matter expert with established credibility. "
            "Demonstrate deep knowledge and experience in the field. "
            "Be definitive and trustworthy while remaining accessible."
        ),
        'Explanatory': (
            "Write to clarify complex topics in simple terms. "
            "Break down information step-by-step, use examples when helpful. "
            "Anticipate questions and address them proactively."
        ),
        'Consultative': (
            "Write as a trusted advisor providing guidance. "
            "Ask relevant questions, consider the recipient's unique situation. "
            "Offer recommendations based on expertise and their specific needs."
        ),
        'Compliance-Focused': (
            "Write with attention to regulatory requirements and legal precision. "
            "Use clear, unambiguous language that meets compliance standards. "
            "Reference relevant policies, regulations, or terms when appropriate. "
            "Maintain professional documentation standards."
        ),
        'Risk-Aware': (
            "Write with consideration of potential risks and their mitigation. "
            "Address uncertainties transparently, discuss protective measures. "
            "Balance risk communication with reassurance. "
            "Use precise language when discussing coverage, limitations, or exposures."
        ),
        'Customer-Centric': (
            "Write with the customer's needs and experience as the priority. "
            "Focus on how information benefits them, anticipate their concerns. "
            "Use accessible language, show that you value their business. "
            "Make it easy for them to understand and take next steps."
        ),
        'Detail-Oriented': (
            "Write with meticulous attention to accuracy and completeness. "
            "Include specific facts, figures, dates, and reference numbers. "
            "Organize information logically, ensure nothing is overlooked. "
            "Be thorough without being overwhelming."
        ),
        'Transparent': (
            "Write with openness and honesty about all relevant information. "
            "Clearly explain processes, timelines, and potential outcomes. "
            "Don't hide difficult information; present it clearly and fairly. "
            "Build trust through candid, straightforward communication."
        ),
        'Solution-Oriented': (
            "Write with focus on solutions, next steps, and positive outcomes. "
            "When presenting challenges, immediately offer options or paths forward. "
            "Be proactive in suggesting alternatives and resolutions. "
            "Maintain a constructive, forward-looking approach."
        )
    }
    
    return tone_instructions.get(tone, tone_instructions['Professional'])


def _get_combined_style_instruction(tones: List[str]) -> str:
    """
    Get style instructions for combined tones.
    
    Args:
        tones: List of tones to combine
        
    Returns:
        Combined style instruction string
    """
    tone_characteristics = {
        'Professional': 'professional language and clear structure',
        'Empathetic': 'understanding and compassionate approach',
        'Formal': 'formal language and respectful manner',
        'Explanatory': 'clear step-by-step clarification',
        'Reassuring': 'comforting and confidence-building approach',
        'Transparent': 'honest and open communication',
        'Solution-Oriented': 'proactive problem-solving focus',
        'Customer-Centric': 'customer needs and experience priority'
    }
    
    characteristics = [tone_characteristics.get(t, t) for t in tones]
    
    if len(tones) == 2:
        combined = f"{characteristics[0]} combined with {characteristics[1]}"
    else:
        combined = ', '.join(characteristics[:-1]) + f", and {characteristics[-1]}"
    
    return (
        f"Write an email that balances {combined}. "
        f"Blend these tones naturally to create a nuanced communication style. "
        f"Ensure the email feels cohesive and authentic, not forced."
    )


def build_subject_prompt(inputs: Dict[str, any]) -> str:
    """
    Build a prompt for generating email subject lines.
    
    Args:
        inputs: Dictionary containing:
            - recipient: Name/title of email recipient
            - subject_context: Context for the email
            - tone: Desired tone(s) - can be a string or list
            - purpose: Main purpose/action of the email
            - bullet_points: List of key points to cover
            
    Returns:
        Formatted prompt string for subject line generation
    """
    bullet_points_str = ', '.join(inputs.get('bullet_points', []))
    
    # Handle tone as either string or list
    tone = inputs.get('tone', 'Professional')
    if isinstance(tone, list):
        tone_str = ' + '.join(tone) if tone else 'Professional'
    else:
        tone_str = tone
    
    prompt = f"""Generate 5 distinct, compelling email subject lines for the following context:

Recipient: {inputs.get('recipient', 'N/A')}
Context: {inputs.get('subject_context', 'N/A')}
Tone: {tone_str}
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
            - tone: Desired tone(s) - can be string or list
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
    
    # Handle tone as either string or list and create variations
    tone = inputs.get('tone', 'Professional')
    if isinstance(tone, list) and len(tone) > 0:
        # Create different tone combinations for different variations
        if len(tone) == 1:
            # If only one tone, use it for all variations
            tone_str = tone[0]
            style_instruction = _get_style_instruction_for_tone(tone[0], variation)
        elif len(tone) == 2:
            # Two tones: use different combinations
            if variation == 1:
                tone_str = tone[0]
                style_instruction = _get_style_instruction_for_tone(tone[0], variation)
            else:
                tone_str = f"{tone[0]} + {tone[1]}"
                style_instruction = _get_combined_style_instruction(tone[:2])
        else:  # 3 tones
            # Three tones: create interesting combinations
            if variation == 1:
                tone_str = f"{tone[0]} + {tone[1]}"
                style_instruction = _get_combined_style_instruction(tone[:2])
            else:
                tone_str = ' + '.join(tone)
                style_instruction = _get_combined_style_instruction(tone)
    else:
        # Single tone string
        tone_str = tone if isinstance(tone, str) else 'Professional'
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
TONE: {tone_str}
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
    
    # Validate tone (can be string or list)
    valid_tones = [
        "Professional", "Empathetic", "Formal", "Explanatory",
        "Reassuring", "Transparent", "Solution-Oriented", "Customer-Centric"
    ]
    tone = inputs.get('tone')
    if isinstance(tone, list):
        if len(tone) == 0:
            return False, "At least one tone must be selected"
        if len(tone) > 3:
            return False, "Maximum 3 tones can be selected"
        for t in tone:
            if t not in valid_tones:
                return False, f"Invalid tone '{t}'. Must be one of: {', '.join(valid_tones)}"
    elif isinstance(tone, str):
        if tone not in valid_tones:
            return False, f"Invalid tone. Must be one of: {', '.join(valid_tones)}"
    else:
        return False, "Tone must be a string or list of strings"
    
    # Validate length
    valid_lengths = ["Short", "Medium", "Long"]
    if inputs.get('length') not in valid_lengths:
        return False, f"Invalid length. Must be one of: {', '.join(valid_lengths)}"
    
    return True, ""
