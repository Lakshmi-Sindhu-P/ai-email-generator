"""
Utility functions for the AI Email Generator.
Includes data loading, text processing, and helper functions.
"""
import pandas as pd
import os
from typing import Optional
from pathlib import Path
from config import DATA_PATH
from logger import setup_logger

logger = setup_logger(__name__)


def load_dataset() -> Optional[pd.DataFrame]:
    """
    Load the email analytics dataset if available.
    
    Returns:
        DataFrame containing the dataset, or None if not found
    """
    try:
        if os.path.exists(DATA_PATH):
            logger.info(f"Loading dataset from {DATA_PATH}")
            df = pd.read_csv(DATA_PATH)
            logger.info(f"Dataset loaded successfully: {len(df)} rows, {len(df.columns)} columns")
            return df
        else:
            logger.warning(f"Dataset not found at {DATA_PATH}")
            return None
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return None


def count_words(text: str) -> int:
    """
    Count the number of words in a text string.
    
    Args:
        text: Input text
        
    Returns:
        Number of words
    """
    return len(text.split())


def count_characters(text: str, include_spaces: bool = True) -> int:
    """
    Count the number of characters in a text string.
    
    Args:
        text: Input text
        include_spaces: Whether to include spaces in count
        
    Returns:
        Number of characters
    """
    if include_spaces:
        return len(text)
    else:
        return len(text.replace(' ', '').replace('\n', '').replace('\t', ''))


def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Estimate reading time for a text in seconds.
    
    Args:
        text: Input text
        words_per_minute: Average reading speed
        
    Returns:
        Estimated reading time in seconds
    """
    word_count = count_words(text)
    minutes = word_count / words_per_minute
    return int(minutes * 60)


def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize user input by removing potentially harmful content.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Truncate if necessary
    if max_length and len(text) > max_length:
        text = text[:max_length]
        logger.warning(f"Input truncated to {max_length} characters")
    
    return text


def format_bullet_points(bullet_points: list) -> str:
    """
    Format a list of bullet points into a readable string.
    
    Args:
        bullet_points: List of bullet point strings
        
    Returns:
        Formatted string with bullet points
    """
    if not bullet_points:
        return ""
    
    return "\n".join([f"• {point}" for point in bullet_points if point.strip()])


def export_to_txt(content: str, filename: str, output_dir: str = "exports") -> str:
    """
    Export content to a text file.
    
    Args:
        content: Content to export
        filename: Name of the output file
        output_dir: Directory to save the file
        
    Returns:
        Path to the created file
        
    Raises:
        IOError: If file creation fails
    """
    try:
        # Create exports directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Ensure .txt extension
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Exported content to {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error exporting to txt: {e}")
        raise IOError(f"Failed to export file: {e}") from e


def export_to_html(
    subject: str,
    body: str,
    recipient: str,
    filename: str,
    output_dir: str = "exports"
) -> str:
    """
    Export email to HTML format.
    
    Args:
        subject: Email subject
        body: Email body content
        recipient: Recipient name
        filename: Name of the output file
        output_dir: Directory to save the file
        
    Returns:
        Path to the created file
        
    Raises:
        IOError: If file creation fails
    """
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        if not filename.endswith('.html'):
            filename += '.html'
        
        filepath = os.path.join(output_dir, filename)
        
        # Create HTML template
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .email-container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .email-header {{
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }}
        .email-subject {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .email-meta {{
            color: #666;
            font-size: 14px;
        }}
        .email-body {{
            line-height: 1.6;
            color: #333;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <div class="email-subject">{subject}</div>
            <div class="email-meta">To: {recipient}</div>
        </div>
        <div class="email-body">{body}</div>
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Exported content to {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error exporting to HTML: {e}")
        raise IOError(f"Failed to export HTML file: {e}") from e
