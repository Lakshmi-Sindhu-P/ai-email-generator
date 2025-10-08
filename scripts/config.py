"""
Configuration management for AI Email Generator.
Centralizes all configuration settings and environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure logs directory exists
LOGS_DIR.mkdir(exist_ok=True)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "350"))
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_RETRIES = 3
OPENAI_RETRY_DELAY = 1  # seconds

# Database Configuration
DB_PATH = os.getenv("DB_PATH", str(PROJECT_ROOT / "ai_email_generator.db"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", str(LOGS_DIR / "app.log"))
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Data Configuration
DATA_PATH = os.getenv(
    "DATA_PATH",
    str(DATA_DIR / "Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv")
)

# Application Settings
APP_TITLE = "AI Email Generator"
APP_ICON = "📧"
DEFAULT_TONES = [
    "Professional",        # Standard business communication
    "Empathetic",         # Understanding & compassionate (claims, difficult news)
    "Formal",             # Legal, compliance, official matters
    "Explanatory",        # Complex information, policy details
    "Reassuring",         # Building confidence, addressing concerns
    "Transparent",        # Honest, clear communication
    "Solution-Oriented",  # Problem-solving, next steps
    "Customer-Centric"    # Customer needs focused
]
DEFAULT_LENGTHS = ["Short", "Medium", "Long"]
MAX_SUBJECT_LINES = 5
NUM_EMAIL_DRAFTS = 2

# Cost Tracking (approximate costs per 1K tokens)
GPT_35_TURBO_INPUT_COST = 0.0015  # $0.0015 per 1K tokens
GPT_35_TURBO_OUTPUT_COST = 0.002  # $0.002 per 1K tokens
GPT_4_INPUT_COST = 0.03
GPT_4_OUTPUT_COST = 0.06

def validate_config():
    """Validate that all required configuration is present."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY not found. Please set it in your .env file. "
            "Copy .env.example to .env and add your API key."
        )
    return True

