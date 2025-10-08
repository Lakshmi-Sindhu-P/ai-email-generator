"""
Tests for email_generator module.
Note: These tests use mocking to avoid actual API calls.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


class TestGenerateCompletion:
    """Tests for generate_completion function."""
    
    @patch('email_generator.client')
    def test_generate_completion_success(self, mock_client, sample_inputs):
        """Test successful completion generation."""
        from email_generator import generate_completion
        
        # Mock the API response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test email content"))]
        mock_response.usage = Mock(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        mock_client.chat.completions.create.return_value = mock_response
        
        result = generate_completion("Test prompt")
        
        assert result == "Test email content"
        assert mock_client.chat.completions.create.called
        
    @patch('email_generator.client')
    def test_generate_completion_with_custom_params(self, mock_client):
        """Test completion with custom parameters."""
        from email_generator import generate_completion
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Content"))]
        mock_response.usage = Mock(prompt_tokens=50, completion_tokens=25, total_tokens=75)
        mock_client.chat.completions.create.return_value = mock_response
        
        result = generate_completion("Prompt", max_tokens=500, temperature=0.9)
        
        assert result == "Content"
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]['max_tokens'] == 500
        assert call_args[1]['temperature'] == 0.9
        
    @patch('email_generator.client')
    @patch('email_generator.time.sleep')
    def test_generate_completion_retry_on_rate_limit(self, mock_sleep, mock_client):
        """Test retry logic on rate limit error."""
        from email_generator import generate_completion
        from openai import RateLimitError
        
        # First call raises error, second succeeds
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Success"))]
        mock_response.usage = Mock(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        
        mock_client.chat.completions.create.side_effect = [
            RateLimitError("Rate limit", response=Mock(status_code=429), body=None),
            mock_response
        ]
        
        result = generate_completion("Test")
        
        assert result == "Success"
        assert mock_sleep.called
        assert mock_client.chat.completions.create.call_count == 2
        
    @patch('email_generator.client')
    @patch('email_generator.time.sleep')
    def test_generate_completion_max_retries_exceeded(self, mock_sleep, mock_client):
        """Test that max retries are respected."""
        from email_generator import generate_completion, EmailGenerationError
        from openai import RateLimitError
        
        # Always raise error
        mock_client.chat.completions.create.side_effect = RateLimitError(
            "Rate limit", response=Mock(status_code=429), body=None
        )
        
        with pytest.raises(EmailGenerationError):
            generate_completion("Test")
            
    @patch('email_generator.client')
    def test_generate_completion_api_error(self, mock_client):
        """Test handling of API errors."""
        from email_generator import generate_completion, EmailGenerationError
        from openai import APIError
        
        mock_client.chat.completions.create.side_effect = APIError(
            "API Error", request=Mock(), body=None
        )
        
        with pytest.raises(EmailGenerationError):
            generate_completion("Test")


class TestGetSubjectLines:
    """Tests for get_subject_lines function."""
    
    @patch('email_generator.generate_completion')
    def test_get_subject_lines_success(self, mock_generate, sample_inputs):
        """Test successful subject line generation."""
        from email_generator import get_subject_lines
        
        mock_generate.return_value = """1. First Subject
2. Second Subject
3. Third Subject
4. Fourth Subject
5. Fifth Subject"""
        
        subjects = get_subject_lines(sample_inputs)
        
        assert len(subjects) == 5
        assert "First Subject" in subjects
        assert "Fifth Subject" in subjects
        
    @patch('email_generator.generate_completion')
    def test_get_subject_lines_with_bullets(self, mock_generate, sample_inputs):
        """Test subject line parsing with bullet points."""
        from email_generator import get_subject_lines
        
        mock_generate.return_value = """- First Subject
- Second Subject
• Third Subject
* Fourth Subject
1. Fifth Subject"""
        
        subjects = get_subject_lines(sample_inputs)
        
        assert len(subjects) == 5
        assert all(not s.startswith(('1. ', '- ', '• ', '* ')) for s in subjects)
        
    @patch('email_generator.generate_completion')
    def test_get_subject_lines_fewer_than_requested(self, mock_generate, sample_inputs):
        """Test when fewer subject lines are returned."""
        from email_generator import get_subject_lines
        
        mock_generate.return_value = """1. First Subject
2. Second Subject
3. Third Subject"""
        
        subjects = get_subject_lines(sample_inputs, max_lines=5)
        
        assert len(subjects) == 3
        
    @patch('email_generator.generate_completion')
    def test_get_subject_lines_error_handling(self, mock_generate, sample_inputs):
        """Test error handling in subject line generation."""
        from email_generator import get_subject_lines, EmailGenerationError
        
        mock_generate.side_effect = EmailGenerationError("Test error")
        
        with pytest.raises(EmailGenerationError):
            get_subject_lines(sample_inputs)


class TestGetEmailDrafts:
    """Tests for get_email_drafts function."""
    
    @patch('email_generator.generate_completion')
    def test_get_email_drafts_success(self, mock_generate, sample_inputs):
        """Test successful email draft generation."""
        from email_generator import get_email_drafts
        
        mock_generate.side_effect = [
            "Dear John,\n\nThis is draft 1...",
            "Dear John,\n\nThis is draft 2..."
        ]
        
        drafts = get_email_drafts(sample_inputs)
        
        assert len(drafts) == 2
        assert "draft 1" in drafts[0]
        assert "draft 2" in drafts[1]
        assert mock_generate.call_count == 2
        
    @patch('email_generator.generate_completion')
    def test_get_email_drafts_with_template(self, mock_generate, sample_inputs):
        """Test draft generation with a template."""
        from email_generator import get_email_drafts
        
        mock_generate.return_value = "Email content"
        template = "Template content"
        
        drafts = get_email_drafts(sample_inputs, template=template)
        
        assert len(drafts) == 2
        
    @patch('email_generator.generate_completion')
    def test_get_email_drafts_custom_count(self, mock_generate, sample_inputs):
        """Test generating custom number of drafts."""
        from email_generator import get_email_drafts
        
        mock_generate.return_value = "Email content"
        
        drafts = get_email_drafts(sample_inputs, num_drafts=3)
        
        assert len(drafts) == 3
        assert mock_generate.call_count == 3
        
    @patch('email_generator.generate_completion')
    def test_get_email_drafts_partial_failure(self, mock_generate, sample_inputs):
        """Test handling when some drafts fail."""
        from email_generator import get_email_drafts, EmailGenerationError
        
        # First succeeds, second fails
        mock_generate.side_effect = [
            "Draft 1 content",
            EmailGenerationError("Generation failed")
        ]
        
        drafts = get_email_drafts(sample_inputs)
        
        assert len(drafts) == 2
        assert "Draft 1 content" in drafts[0]
        assert "[Error" in drafts[1]  # Error message placeholder


class TestEstimateCost:
    """Tests for estimate_cost function."""
    
    def test_estimate_cost_gpt35(self):
        """Test cost estimation for GPT-3.5."""
        from email_generator import estimate_cost
        
        cost = estimate_cost(1000, 500, model="gpt-3.5-turbo")
        
        assert cost > 0
        assert isinstance(cost, float)
        
    def test_estimate_cost_gpt4(self):
        """Test cost estimation for GPT-4."""
        from email_generator import estimate_cost
        
        cost = estimate_cost(1000, 500, model="gpt-4")
        
        assert cost > 0
        assert isinstance(cost, float)
        
    def test_estimate_cost_gpt4_more_expensive(self):
        """Test that GPT-4 is estimated as more expensive."""
        from email_generator import estimate_cost
        
        cost_gpt35 = estimate_cost(1000, 500, model="gpt-3.5-turbo")
        cost_gpt4 = estimate_cost(1000, 500, model="gpt-4")
        
        assert cost_gpt4 > cost_gpt35
        
    def test_estimate_cost_zero_tokens(self):
        """Test cost estimation with zero tokens."""
        from email_generator import estimate_cost
        
        cost = estimate_cost(0, 0)
        
        assert cost == 0.0

