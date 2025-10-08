"""
Pytest configuration and fixtures for testing.
"""
import pytest
import sys
import os
from pathlib import Path

# Add scripts directory to path
scripts_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

@pytest.fixture
def sample_inputs():
    """Sample email inputs for testing."""
    return {
        "recipient": "John Doe",
        "subject_context": "Follow-up on meeting",
        "tone": "Professional",
        "purpose": "Schedule next steps",
        "bullet_points": ["Review action items", "Set timeline", "Assign responsibilities"],
        "length": "Medium",
        "additional_notes": "Keep it concise"
    }

@pytest.fixture
def sample_subjects():
    """Sample subject lines for testing."""
    return [
        "Follow-up: Next Steps from Our Meeting",
        "Action Items and Timeline Discussion",
        "Meeting Follow-up - Scheduling Next Steps",
        "Quick Follow-up on Our Recent Discussion",
        "Next Steps: Timeline and Responsibilities"
    ]

@pytest.fixture
def sample_drafts():
    """Sample email drafts for testing."""
    return [
        "Dear John,\n\nI hope this email finds you well...",
        "Dear John,\n\nThank you for taking the time to meet..."
    ]

@pytest.fixture
def test_db_path(tmp_path):
    """Temporary database path for testing."""
    return str(tmp_path / "test_email_generator.db")

