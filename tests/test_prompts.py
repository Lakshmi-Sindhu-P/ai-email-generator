"""
Tests for prompts module.
"""
import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from prompts import build_subject_prompt, build_email_prompt, validate_inputs


class TestBuildSubjectPrompt:
    """Tests for build_subject_prompt function."""
    
    def test_build_subject_prompt_basic(self, sample_inputs):
        """Test basic subject prompt building."""
        prompt = build_subject_prompt(sample_inputs)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert sample_inputs["recipient"] in prompt
        assert sample_inputs["subject_context"] in prompt
        assert sample_inputs["tone"] in prompt
        
    def test_build_subject_prompt_includes_all_fields(self, sample_inputs):
        """Test that all input fields are included in prompt."""
        prompt = build_subject_prompt(sample_inputs)
        
        assert "Recipient:" in prompt
        assert "Context:" in prompt
        assert "Tone:" in prompt
        assert "Purpose:" in prompt
        assert "Key Points:" in prompt
        
    def test_build_subject_prompt_with_empty_bullets(self):
        """Test prompt building with empty bullet points."""
        inputs = {
            "recipient": "Jane Doe",
            "subject_context": "Test",
            "tone": "Casual",
            "purpose": "Testing",
            "bullet_points": []
        }
        
        prompt = build_subject_prompt(inputs)
        assert isinstance(prompt, str)
        assert len(prompt) > 0


class TestBuildEmailPrompt:
    """Tests for build_email_prompt function."""
    
    def test_build_email_prompt_variation_1(self, sample_inputs):
        """Test email prompt building for variation 1."""
        prompt = build_email_prompt(sample_inputs, variation=1)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "RECIPIENT:" in prompt
        assert "concise" in prompt.lower() or "friendly" in prompt.lower()
        
    def test_build_email_prompt_variation_2(self, sample_inputs):
        """Test email prompt building for variation 2."""
        prompt = build_email_prompt(sample_inputs, variation=2)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "formal" in prompt.lower() or "thorough" in prompt.lower()
        
    def test_build_email_prompt_with_template(self, sample_inputs):
        """Test email prompt building with a template."""
        template = "This is a sample template email."
        prompt = build_email_prompt(sample_inputs, variation=1, template=template)
        
        assert template in prompt
        assert "TEMPLATE REFERENCE:" in prompt
        
    def test_build_email_prompt_different_lengths(self):
        """Test prompt building with different length options."""
        inputs = {
            "recipient": "Test",
            "subject_context": "Test",
            "tone": "Professional",
            "purpose": "Test",
            "bullet_points": ["Point 1"],
            "length": "Short",
            "additional_notes": ""
        }
        
        for length in ["Short", "Medium", "Long"]:
            inputs["length"] = length
            prompt = build_email_prompt(inputs)
            assert inputs["length"] in prompt


class TestValidateInputs:
    """Tests for validate_inputs function."""
    
    def test_validate_inputs_valid(self, sample_inputs):
        """Test validation with valid inputs."""
        is_valid, error_msg = validate_inputs(sample_inputs)
        assert is_valid is True
        assert error_msg == ""
        
    def test_validate_inputs_missing_recipient(self, sample_inputs):
        """Test validation fails with missing recipient."""
        sample_inputs["recipient"] = ""
        is_valid, error_msg = validate_inputs(sample_inputs)
        assert is_valid is False
        assert "recipient" in error_msg.lower()
        
    def test_validate_inputs_missing_purpose(self, sample_inputs):
        """Test validation fails with missing purpose."""
        del sample_inputs["purpose"]
        is_valid, error_msg = validate_inputs(sample_inputs)
        assert is_valid is False
        assert "purpose" in error_msg.lower()
        
    def test_validate_inputs_empty_bullet_points(self, sample_inputs):
        """Test validation fails with empty bullet points."""
        sample_inputs["bullet_points"] = []
        is_valid, error_msg = validate_inputs(sample_inputs)
        assert is_valid is False
        assert "bullet point" in error_msg.lower()
        
    def test_validate_inputs_invalid_tone(self, sample_inputs):
        """Test validation fails with invalid tone."""
        sample_inputs["tone"] = "InvalidTone"
        is_valid, error_msg = validate_inputs(sample_inputs)
        assert is_valid is False
        assert "tone" in error_msg.lower()
        
    def test_validate_inputs_invalid_length(self, sample_inputs):
        """Test validation fails with invalid length."""
        sample_inputs["length"] = "ExtraLong"
        is_valid, error_msg = validate_inputs(sample_inputs)
        assert is_valid is False
        assert "length" in error_msg.lower()
        
    def test_validate_inputs_bullet_points_not_list(self, sample_inputs):
        """Test validation fails when bullet points is not a list."""
        sample_inputs["bullet_points"] = "Not a list"
        is_valid, error_msg = validate_inputs(sample_inputs)
        assert is_valid is False
        assert "list" in error_msg.lower()

