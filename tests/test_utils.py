"""
Tests for utils module.
"""
import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from utils import (
    count_words,
    count_characters,
    estimate_reading_time,
    sanitize_input,
    format_bullet_points,
    export_to_txt,
    export_to_html
)


class TestCountWords:
    """Tests for count_words function."""
    
    def test_count_words_basic(self):
        """Test basic word counting."""
        text = "This is a test sentence"
        assert count_words(text) == 5
        
    def test_count_words_empty(self):
        """Test word counting with empty string."""
        assert count_words("") == 0
        
    def test_count_words_with_newlines(self):
        """Test word counting with newlines."""
        text = "Line one\nLine two\nLine three"
        assert count_words(text) == 6
        
    def test_count_words_with_multiple_spaces(self):
        """Test word counting with multiple spaces."""
        text = "Word1    Word2     Word3"
        assert count_words(text) == 3


class TestCountCharacters:
    """Tests for count_characters function."""
    
    def test_count_characters_with_spaces(self):
        """Test character counting including spaces."""
        text = "Hello World"
        assert count_characters(text, include_spaces=True) == 11
        
    def test_count_characters_without_spaces(self):
        """Test character counting excluding spaces."""
        text = "Hello World"
        assert count_characters(text, include_spaces=False) == 10
        
    def test_count_characters_empty(self):
        """Test character counting with empty string."""
        assert count_characters("", include_spaces=True) == 0
        assert count_characters("", include_spaces=False) == 0
        
    def test_count_characters_with_newlines(self):
        """Test character counting with newlines."""
        text = "Line1\nLine2"
        assert count_characters(text, include_spaces=True) == 11


class TestEstimateReadingTime:
    """Tests for estimate_reading_time function."""
    
    def test_estimate_reading_time_basic(self):
        """Test basic reading time estimation."""
        text = " ".join(["word"] * 200)  # 200 words
        reading_time = estimate_reading_time(text, words_per_minute=200)
        assert reading_time == 60  # Should be 1 minute = 60 seconds
        
    def test_estimate_reading_time_short_text(self):
        """Test reading time for short text."""
        text = "Hello world"
        reading_time = estimate_reading_time(text, words_per_minute=200)
        assert reading_time >= 0
        assert reading_time < 60
        
    def test_estimate_reading_time_empty(self):
        """Test reading time for empty text."""
        reading_time = estimate_reading_time("")
        assert reading_time == 0


class TestSanitizeInput:
    """Tests for sanitize_input function."""
    
    def test_sanitize_input_basic(self):
        """Test basic input sanitization."""
        text = "  Hello World  "
        assert sanitize_input(text) == "Hello World"
        
    def test_sanitize_input_empty(self):
        """Test sanitizing empty input."""
        assert sanitize_input("") == ""
        assert sanitize_input(None) == ""
        
    def test_sanitize_input_with_max_length(self):
        """Test sanitization with max length."""
        text = "A" * 100
        result = sanitize_input(text, max_length=50)
        assert len(result) == 50
        
    def test_sanitize_input_under_max_length(self):
        """Test sanitization when text is under max length."""
        text = "Short text"
        result = sanitize_input(text, max_length=100)
        assert result == text


class TestFormatBulletPoints:
    """Tests for format_bullet_points function."""
    
    def test_format_bullet_points_basic(self):
        """Test basic bullet point formatting."""
        points = ["Point 1", "Point 2", "Point 3"]
        result = format_bullet_points(points)
        
        assert "• Point 1" in result
        assert "• Point 2" in result
        assert "• Point 3" in result
        assert result.count("\n") == 2
        
    def test_format_bullet_points_empty(self):
        """Test formatting empty bullet points."""
        assert format_bullet_points([]) == ""
        
    def test_format_bullet_points_with_empty_strings(self):
        """Test formatting with empty strings in list."""
        points = ["Point 1", "", "Point 2", "  ", "Point 3"]
        result = format_bullet_points(points)
        
        # Should only include non-empty points
        assert "• Point 1" in result
        assert "• Point 2" in result
        assert "• Point 3" in result


class TestExportToTxt:
    """Tests for export_to_txt function."""
    
    def test_export_to_txt_basic(self, tmp_path):
        """Test basic text export."""
        content = "Test email content"
        filename = "test_email"
        output_dir = str(tmp_path)
        
        filepath = export_to_txt(content, filename, output_dir)
        
        assert os.path.exists(filepath)
        assert filepath.endswith('.txt')
        
        with open(filepath, 'r') as f:
            assert f.read() == content
            
    def test_export_to_txt_with_extension(self, tmp_path):
        """Test export with .txt extension already provided."""
        content = "Test content"
        filename = "test.txt"
        output_dir = str(tmp_path)
        
        filepath = export_to_txt(content, filename, output_dir)
        
        assert os.path.exists(filepath)
        assert filepath.count('.txt') == 1  # Should not add .txt twice
        
    def test_export_to_txt_creates_directory(self, tmp_path):
        """Test that export creates output directory if it doesn't exist."""
        content = "Test"
        filename = "test"
        output_dir = str(tmp_path / "new_dir")
        
        filepath = export_to_txt(content, filename, output_dir)
        
        assert os.path.exists(filepath)
        assert os.path.exists(output_dir)


class TestExportToHtml:
    """Tests for export_to_html function."""
    
    def test_export_to_html_basic(self, tmp_path):
        """Test basic HTML export."""
        subject = "Test Subject"
        body = "Test email body"
        recipient = "Test Recipient"
        filename = "test_email"
        output_dir = str(tmp_path)
        
        filepath = export_to_html(subject, body, recipient, filename, output_dir)
        
        assert os.path.exists(filepath)
        assert filepath.endswith('.html')
        
        with open(filepath, 'r') as f:
            content = f.read()
            assert subject in content
            assert body in content
            assert recipient in content
            assert "<!DOCTYPE html>" in content
            
    def test_export_to_html_with_extension(self, tmp_path):
        """Test HTML export with extension already provided."""
        filepath = export_to_html(
            "Subject", "Body", "Recipient", "test.html", str(tmp_path)
        )
        
        assert os.path.exists(filepath)
        assert filepath.count('.html') == 1

