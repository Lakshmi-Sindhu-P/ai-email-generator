# 📧 AI Email Generator

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-UI-orange) ![Snowflake](https://img.shields.io/badge/Snowflake-DB-lightblue) ![OpenAI](https://img.shields.io/badge/LLM-AI-purple)
![License](https://img.shields.io/badge/License-MIT-green) ![Demo](https://img.shields.io/badge/Live-Demo-brightgreen)

> Your **context-aware AI assistant** for drafting professional emails! ✨  
> Generates **2 full email drafts + 5 subject line suggestions** from structured input.

---

## 🌈 Demo / GIF Preview

> *(Add your own GIF or short screen recording of Streamlit app in action here)*

![Demo Placeholder](https://media.giphy.com/media/xUPGcxpCV81ebKh7R6/giphy.gif)

---

## 🎯 Project Goal

We are building a **smart AI email assistant** that:

* Takes **user inputs + optional email history**  
* Produces **ready-to-send email drafts**  
* Minimizes manual edits ✅  
* Adapts to **misspellings, incomplete info, or partial input**  

<details>
<summary>📝 User Input Fields (Click to Expand)</summary>

| Field               | Type     | Description                                           |
| ------------------- | -------- | ----------------------------------------------------- |
| 👤 Recipient        | Optional | Adjusts tone (formal vs casual)                       |
| 📝 Subject Context  | Text     | What the email is about                               |
| 🎭 Tone             | Dropdown | Formal, Polite, Friendly, Persuasive, Neutral         |
| ✅ Purpose / Action  | Dropdown | Request, Follow-up, Schedule, Accept, Decline, Inform |
| 📌 Key Info         | Textarea | Facts to include                                      |
| ⏱ Length            | Dropdown | Short, Medium, Detailed                               |
| 🖊 Additional Notes | Text     | Special instructions                                  |

</details>

---

## 🖥 Output Structure

* **Subjects:** 5 suggestions 🔹 short, clear, catchy  
* **Drafts:** 2 variations 🔹 Formal vs Friendly  
* **Handles errors** and logs generation failures  
* Output **JSON** for easy parsing in Streamlit

<details>
<summary>Example JSON Output</summary>

```json
{
  "subjects": [
    "Request for Project Timeline Update",
    "Following Up on Project Status",
    "Next Steps for Our Collaboration",
    "Project Timeline – Quick Check-In",
    "Update on Our Ongoing Project"
  ],
  "drafts": [
    {
      "tone": "Formal",
      "body": "Dear [Recipient],\n\nI hope this message finds you well. I am writing to kindly request an update on the current status of the project. ...\n\nBest regards,\n[Your Name]"
    },
    {
      "tone": "Friendly",
      "body": "Hi [Recipient],\n\nJust wanted to quickly check in about the project timeline. Could you share where things stand right now? ...\n\nThanks a lot,\n[Your Name]"
    }
  ]
}
````

</details>

---

## 🛠 Tech Stack

| Layer           | Technology                         |
| --------------- | ---------------------------------- |
| Frontend        | Streamlit (Snowflake / External)   |
| Backend         | Python + OpenAI / HuggingFace LLM  |
| Data            | Snowflake (templates, logs, users) |
| Version Control | Git + GitHub                       |
| Optional        | Gmail / Outlook API                |

---

## 📂 Snowflake Database Schema

<details>
<summary>Click to Expand Tables & Fields</summary>

### 1️⃣ USERS

```sql
CREATE TABLE USERS (
    USER_ID NUMBER AUTOINCREMENT PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(255) UNIQUE NOT NULL,
    ROLE VARCHAR(50) DEFAULT 'Regular',
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);
```

### 2️⃣ EMAIL\_TEMPLATES

```sql
CREATE TABLE EMAIL_TEMPLATES (
    TEMPLATE_ID NUMBER AUTOINCREMENT PRIMARY KEY,
    TEMPLATE_NAME VARCHAR(100),
    SUBJECT_PLACEHOLDER VARCHAR(255),
    BODY_PLACEHOLDER VARCHAR(5000),
    USAGE_COUNT NUMBER DEFAULT 0,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);
```

### 3️⃣ EMAIL\_PROMPTS

```sql
CREATE TABLE EMAIL_PROMPTS (
    PROMPT_ID NUMBER AUTOINCREMENT PRIMARY KEY,
    USER_ID NUMBER REFERENCES USERS(USER_ID),
    RECIPIENT_EMAIL VARCHAR(255),
    SUBJECT_CONTEXT VARCHAR(500),
    TONE VARCHAR(50),
    PURPOSE VARCHAR(50),
    BULLET_POINTS VARCHAR(2000),
    LENGTH VARCHAR(50),
    ADDITIONAL_NOTES VARCHAR(2000),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);
```

### 4️⃣ GENERATED\_EMAILS

```sql
CREATE TABLE GENERATED_EMAILS (
    EMAIL_ID NUMBER AUTOINCREMENT PRIMARY KEY,
    PROMPT_ID NUMBER REFERENCES EMAIL_PROMPTS(PROMPT_ID),
    USER_ID NUMBER REFERENCES USERS(USER_ID),
    SUBJECT VARCHAR(255),
    BODY VARCHAR(5000),
    DRAFT_NUMBER NUMBER,  -- 1 or 2
    TONE VARCHAR(50),
    PRIORITY VARCHAR(50) DEFAULT 'Normal',
    IS_READ BOOLEAN DEFAULT FALSE,
    STATUS VARCHAR(50) DEFAULT 'Draft',  -- Draft, Sent, Archived
    GENERATION_STATUS VARCHAR(50) DEFAULT 'Success',  -- Success, Failed
    ERROR_MESSAGE VARCHAR(1000),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP,
    SENT_AT TIMESTAMP_NTZ
);
```

### 5️⃣ SUBJECT\_SUGGESTIONS

```sql
CREATE TABLE SUBJECT_SUGGESTIONS (
    SUGGESTION_ID NUMBER AUTOINCREMENT PRIMARY KEY,
    PROMPT_ID NUMBER REFERENCES EMAIL_PROMPTS(PROMPT_ID),
    USER_ID NUMBER REFERENCES USERS(USER_ID),
    SUBJECT_LINE VARCHAR(255),
    GENERATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP,
    SELECTED BOOLEAN DEFAULT FALSE
);
```

### 6️⃣ EMAIL\_FEEDBACK

```sql
CREATE TABLE EMAIL_FEEDBACK (
    FEEDBACK_ID NUMBER AUTOINCREMENT PRIMARY KEY,
    EMAIL_ID NUMBER REFERENCES GENERATED_EMAILS(EMAIL_ID),
    USER_ID NUMBER REFERENCES USERS(USER_ID),
    RATING NUMBER CHECK(RATING BETWEEN 1 AND 5),
    COMMENTS VARCHAR(2000),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);
```

</details>

---

## 🧩 Draft Generation Logic

* **Draft 1:** Formal / structured / detailed
* **Draft 2:** Friendly / concise / conversational

**Variation Dimensions:** Tone ✅ Structure ✅ Length ✅
**JSON output** for easy parsing in Streamlit

---

## ⚡ Workflow

1. User fills the form 🖊
2. Backend calls AI 🤖 → generates drafts + subjects
3. Streamlit displays output 🖥
4. User selects draft ✅ → copy-paste
5. Optional: log emails & feedback in Snowflake 📊

---

## 🚀 Setup Instructions

```bash
# Clone repo
git clone https://github.com/Lakshmi-Sindhu-P/ai-email-generator.git
cd ai-email-generator

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app/app.py
```

> ⚠️ Configure Snowflake credentials & OpenAI/HuggingFace API keys first.

---

## 🌟 Future Improvements

* Direct Gmail / Outlook integration 📧
* Extra draft variations 🎨
* Context-aware history storage 🗄
* User authentication 🔒
* Analytics dashboard: subject selection, feedback, AI success rate 📊

---

## 👩‍💻 Author

**Lakshmi Sindhu Pulugundla**
Master’s in Data Science | Illinois Institute of Technology

---
