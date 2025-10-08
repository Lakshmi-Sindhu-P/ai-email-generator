import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import build_subject_prompt, build_email_prompt

# Load .env variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=api_key)

def generate_completion(prompt, max_tokens=350):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-4o" if available to you
        messages=[
            {"role": "system", "content": "You are an AI assistant for generating professional emails."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def get_subject_lines(inputs):
    prompt = build_subject_prompt(inputs)
    output = generate_completion(prompt)
    # Split output into lines, remove numbering
    subjects = [line.strip('12345. ') for line in output.split('\n') if line.strip()]
    return subjects[:5] if len(subjects) >= 5 else subjects

def get_email_drafts(inputs, template=""):
    draft1 = generate_completion(build_email_prompt(inputs, 1, template))
    draft2 = generate_completion(build_email_prompt(inputs, 2, template))
    return [draft1, draft2]
