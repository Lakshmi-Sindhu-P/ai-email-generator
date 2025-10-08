def build_subject_prompt(inputs):
    return (
        f"Recipient: {inputs['recipient']}\n"
        f"Context: {inputs['subject_context']}\n"
        f"Tone: {inputs['tone']}\n"
        f"Purpose: {inputs['purpose']}\n"
        f"Bullet Points: {', '.join(inputs['bullet_points'])}\n"
        f"Generate 5 distinct, effective subject lines for this email context."
    )

def build_email_prompt(inputs, variation, template=""):
    details = (
        f"Recipient: {inputs['recipient']}\n"
        f"Context: {inputs['subject_context']}\n"
        f"Tone: {inputs['tone']}\n"
        f"Purpose: {inputs['purpose']}\n"
        f"Bullet Points: {', '.join(inputs['bullet_points'])}\n"
        f"Length: {inputs['length']}\n"
        f"Notes: {inputs['additional_notes']}\n"
    )
    if template:
        details += f"Suggested Template: {template}\n"
    if variation == 1:
        return f"{details}Write a concise, professional, and friendly email draft addressing the above."
    else:
        return f"{details}Write a more formal, thorough email draft with a different structure and tone."
