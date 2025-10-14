# 📧 AI Email Generator

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-UI-orange)
![OpenAI](https://img.shields.io/badge/LLM-AI-purple) ![License](https://img.shields.io/badge/License-MIT-green) ![Tests](https://img.shields.io/badge/Tests-Passing-success)

> Your **context-aware AI assistant** to draft professional emails effortlessly.  
> Generates 2 email drafts with varying tone + 5 subject line suggestions based on user inputs.

---

## 📑 Table of Contents

- [Features](#-features)
- [Demo](#-demo-preview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup Instructions](#-setup-instructions)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Features
- **Multiple Email Drafts**: Generate 2 distinct email drafts with different writing styles
- **Subject Line Suggestions**: Get 5 creative subject line options for each email
- **Tone Customization**: Choose from Professional, Friendly, Formal, Casual, Persuasive, or Enthusiastic tones
- **Length Control**: Select Short, Medium, or Long draft lengths
- **Smart Context Handling**: AI understands recipient, purpose, and key points

### Advanced Features
- **Email History**: View all previously generated emails with search and filter
- **Favorites System**: Star your best emails for quick access
- **Export Options**: Export emails to TXT or HTML formats
- **Cost Tracking**: Monitor API usage and estimated costs
- **Word & Character Count**: Real-time metrics for each draft
- **Error Handling**: Comprehensive error handling with retry logic
- **Local Storage**: SQLite database for persistent storage
- **Logging System**: Complete logging for debugging and monitoring

### Technical Features
- **Type-Safe**: Full type hints throughout the codebase
- **Well-Documented**: Comprehensive docstrings and comments
- **Tested**: 60+ unit tests with high coverage
- **Configurable**: Environment-based configuration
- **Production-Ready**: Error handling, logging, and validation

---

## 🎬 Demo Preview

### Main Interface
![Email Generation Interface](<img width="1705" height="947" alt="Screenshot 2025-10-14 at 2 40 55 PM" src="https://github.com/user-attachments/assets/6a5512ff-3609-4dd3-884e-36cb65109f76" />
)

### Generated Results
![Generated Emails](docs/screenshot_results.png)

---

## 🏗 Tech Stack

| Layer         | Technology                  | Purpose                          |
|---------------|-----------------------------|----------------------------------|
| Frontend      | Streamlit                   | Interactive web UI               |
| Backend       | Python 3.10+                | Core application logic           |
| AI/LLM        | OpenAI API (GPT-3.5/4)      | Email and subject generation     |
| Database      | SQLite                      | Local data persistence           |
| Testing       | Pytest                      | Unit and integration tests       |
| Logging       | Python logging              | Application monitoring           |
| Version Control | Git + GitHub              | Source code management           |

---

## 📁 Project Structure

```
ai-email-generator/
├── scripts/                 # Main application code
│   ├── app.py              # Streamlit UI application
│   ├── email_generator.py  # OpenAI API integration
│   ├── prompts.py          # Prompt templates and validation
│   ├── db.py               # Database operations
│   ├── utils.py            # Utility functions
│   ├── config.py           # Configuration management
│   └── logger.py           # Logging setup
├── tests/                   # Test suite
│   ├── conftest.py         # Pytest fixtures
│   ├── test_email_generator.py
│   ├── test_prompts.py
│   ├── test_db.py
│   └── test_utils.py
├── data/                    # Data files
├── logs/                    # Application logs
├── exports/                 # Exported emails
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

---

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.10 or higher**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-email-generator.git
cd ai-email-generator
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Use your preferred text editor
nano .env  # or vim, code, etc.
```

Add your API key to `.env`:
```env
OPENAI_API_KEY=your_actual_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### Step 5: Initialize Database

The database will be automatically created on first run, or you can initialize it manually:

```bash
cd scripts
python -c "from db import init_db; init_db()"
```

### Step 6: Run the Application

```bash
# From the project root
cd scripts
streamlit run app.py
```

The application should open in your default browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Basic Email Generation

1. **Fill in Required Fields**:
   - **Recipient**: Name and/or title (e.g., "Dr. Jane Smith, CEO")
   - **Subject Context**: Brief context (e.g., "Follow-up on project proposal")
   - **Tone**: Select appropriate tone
   - **Purpose**: Main goal of the email
   - **Key Points**: List important points (one per line)
   - **Length**: Choose desired email length

2. **Optional Fields**:
   - **Additional Notes**: Any special requirements or context

3. **Generate**: Click "✨ Generate Emails" button

4. **Review Results**:
   - Review 5 subject line suggestions
   - Compare 2 email drafts
   - Check word and character counts
   - Edit drafts directly in the text areas

5. **Export or Copy**:
   - Use copy buttons to copy to clipboard
   - Download as TXT file
   - All emails are automatically saved to history

### Viewing Email History

```python
# Access history through the UI (coming in Phase 3)
# Or query the database directly
from db import get_email_logs

logs = get_email_logs(limit=10)
for log in logs:
    print(f"To: {log['recipient']} - {log['timestamp']}")
```

### Exporting Emails

```python
from utils import export_to_txt, export_to_html

# Export to text
export_to_txt(email_content, "my_email.txt")

# Export to HTML
export_to_html(subject, body, recipient, "my_email.html")
```

---

## ⚙️ Configuration

### Environment Variables

All configuration is managed through environment variables. See `.env.example` for all available options:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *Required* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | Model to use (gpt-3.5-turbo or gpt-4) |
| `OPENAI_MAX_TOKENS` | `350` | Maximum tokens per response |
| `OPENAI_TEMPERATURE` | `0.7` | Temperature for generation (0.0-1.0) |
| `DB_PATH` | `ai_email_generator.db` | Database file path |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FILE` | `logs/app.log` | Log file path |

### Cost Estimates

Approximate costs per email generation (using GPT-3.5-turbo):
- Subject lines (5): ~$0.001-0.002
- Email drafts (2): ~$0.002-0.005
- **Total per generation: ~$0.003-0.007**

Using GPT-4 is approximately 20x more expensive but may produce higher quality results.

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=scripts --cov-report=html

# Run specific test file
pytest tests/test_email_generator.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_prompts.py::TestValidateInputs::test_validate_inputs_valid
```

### Test Structure

The test suite includes:
- **60+ unit tests** covering all modules
- **Mocked API calls** (no actual OpenAI charges during testing)
- **Fixtures** for common test data
- **Coverage tracking** to ensure code quality

### Writing Tests

```python
# Example test
def test_generate_completion(mock_client):
    """Test email generation."""
    from email_generator import generate_completion
    
    mock_client.chat.completions.create.return_value = Mock(
        choices=[Mock(message=Mock(content="Test"))]
    )
    
    result = generate_completion("Test prompt")
    assert result == "Test"
```

---

## 📚 API Documentation

### Core Functions

#### `get_email_drafts(inputs, template, num_drafts)`

Generate email drafts based on user inputs.

**Parameters:**
- `inputs` (dict): User inputs containing recipient, purpose, tone, etc.
- `template` (str, optional): Template to base emails on
- `num_drafts` (int): Number of drafts to generate (default: 2)

**Returns:**
- `list[str]`: List of generated email drafts

**Raises:**
- `EmailGenerationError`: If generation fails

**Example:**
```python
inputs = {
    "recipient": "John Doe",
    "subject_context": "Meeting follow-up",
    "tone": "Professional",
    "purpose": "Schedule next meeting",
    "bullet_points": ["Review action items", "Set timeline"],
    "length": "Medium",
    "additional_notes": ""
}

drafts = get_email_drafts(inputs)
```

#### `get_subject_lines(inputs, max_lines)`

Generate subject line suggestions.

**Parameters:**
- `inputs` (dict): User inputs
- `max_lines` (int): Maximum number of suggestions (default: 5)

**Returns:**
- `list[str]`: List of subject lines

#### `save_email_log(inputs, subjects, drafts, cost_estimate)`

Save generated email to database.

**Parameters:**
- `inputs` (dict): User inputs
- `subjects` (list[str]): Generated subject lines
- `drafts` (list[str]): Generated email drafts
- `cost_estimate` (float): Estimated API cost

**Returns:**
- `int`: ID of saved record

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "OPENAI_API_KEY not found"

**Problem**: API key is not configured.

**Solution**:
```bash
# Ensure .env file exists
cp .env.example .env

# Add your API key to .env
echo "OPENAI_API_KEY=your_key_here" >> .env
```

#### 2. "Rate limit exceeded"

**Problem**: Too many API requests in a short time.

**Solution**: The app automatically retries with exponential backoff. Wait a moment and try again.

#### 3. "Database locked"

**Problem**: Multiple processes accessing the database.

**Solution**: Close other instances of the application and try again.

#### 4. Import Errors

**Problem**: Module not found errors.

**Solution**:
```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### 5. Streamlit Issues

**Problem**: Streamlit won't start.

**Solution**:
```bash
# Clear Streamlit cache
streamlit cache clear

# Check if port 8501 is available
# Try a different port
streamlit run app.py --server.port 8502
```

### Debug Mode

Enable debug logging for more detailed output:

```bash
# In .env
LOG_LEVEL=DEBUG
```

Then check `logs/app.log` for detailed information.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues

1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information

### Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints to all functions
- Write docstrings for all public functions
- Add tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT API
- **Streamlit** for the amazing UI framework
- **Contributors** who help improve this project

---

## 📞 Support

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/ai-email-generator/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/ai-email-generator/discussions)

---

## 🗺️ Roadmap

### ✅ Completed
- [x] Core email generation
- [x] Subject line suggestions
- [x] Multiple tone options
- [x] Local database storage
- [x] Error handling and retry logic
- [x] Comprehensive testing
- [x] Type hints and documentation
- [x] Logging system

### 🚧 In Progress (Phase 3)
- [ ] Email history viewer UI
- [ ] Copy-to-clipboard functionality
- [ ] Cost tracking dashboard
- [ ] Export to PDF
- [ ] Favorites system UI

### 📋 Planned (Phase 4)
- [ ] Multi-page UI with tabs
- [ ] Async email generation
- [ ] Email template library
- [ ] Docker containerization
- [ ] Side-by-side draft comparison

### 💡 Future Ideas
- [ ] Email threading support
- [ ] Multi-language support
- [ ] Custom tone training
- [ ] Browser extension
- [ ] Mobile app
- [ ] Team collaboration features
- [ ] Analytics dashboard

---
