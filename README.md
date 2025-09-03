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
```

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

## 📂 Repo Structure

```
ai-email-generator/
├── notebooks/          # Prototyping notebooks
├── src/                # Core Python modules
│   ├── preprocess.py
│   ├── generator.py
│   ├── formatter.py
│   └── snowflake_utils.py
├── streamlit_app/      # Streamlit UI
├── requirements.txt
├── README.md
├── .gitignore
└── docs/               # Diagrams, reports, notes
```

---

## 🧩 Draft Generation Logic

* **Draft 1:** Formal / structured / detailed
* **Draft 2:** Friendly / concise / conversational

**Variation Dimensions:** Tone ✅ Structure ✅ Length ✅
**Output:** JSON (easy parsing in Streamlit)

---

## ⚡ Workflow

1. User fills the form 🖊
2. Backend calls AI 🤖 → generates drafts + subjects
3. Streamlit displays output 🖥
4. User selects draft ✅ → copy-paste
5. Optional: log emails in Snowflake 📊

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

---

## 👩‍💻 Author

**Lakshmi Sindhu Pulugundla**
Master’s in Data Science | Illinois Institute of Technology

---

✅ **Tip:** Keep this README as your **project blueprint** for every step!

---

