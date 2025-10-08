"""
Email generation module using OpenAI API.
Handles generation of email drafts and subject lines with error handling and retry logic.
"""
import time
from typing import List, Dict, Optional
from openai import OpenAI, OpenAIError, RateLimitError, APIError
from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_MAX_TOKENS,
    OPENAI_TEMPERATURE,
    OPENAI_MAX_RETRIES,
    OPENAI_RETRY_DELAY,
    validate_config
)
from logger import setup_logger
from prompts import build_subject_prompt, build_email_prompt

# Setup logger for this module
logger = setup_logger(__name__)

# Validate configuration on import
try:
    validate_config()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


class EmailGenerationError(Exception):
    """Custom exception for email generation errors."""
    pass


def generate_completion(
    prompt: str, 
    max_tokens: int = OPENAI_MAX_TOKENS,
    temperature: float = OPENAI_TEMPERATURE,
    retry_count: int = 0
) -> str:
    """
    Generate a completion using OpenAI API with retry logic.
    
    Args:
        prompt: The prompt to send to the API
        max_tokens: Maximum tokens in the response
        temperature: Temperature for response generation (0.0-1.0)
        retry_count: Current retry attempt number
        
    Returns:
        Generated text completion
        
    Raises:
        EmailGenerationError: If generation fails after all retries
    """
    try:
        logger.info(f"Generating completion with model: {OPENAI_MODEL}")
        logger.debug(f"Prompt length: {len(prompt)} characters")
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant specialized in generating professional, "
                              "well-structured emails. You understand various tones, contexts, and "
                              "business communication best practices."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        content = response.choices[0].message.content.strip()
        logger.info("Successfully generated completion")
        logger.debug(f"Response length: {len(content)} characters")
        
        # Log token usage for cost tracking
        if hasattr(response, 'usage'):
            logger.info(
                f"Token usage - Prompt: {response.usage.prompt_tokens}, "
                f"Completion: {response.usage.completion_tokens}, "
                f"Total: {response.usage.total_tokens}"
            )
        
        return content
        
    except RateLimitError as e:
        logger.warning(f"Rate limit hit: {e}")
        if retry_count < OPENAI_MAX_RETRIES:
            wait_time = OPENAI_RETRY_DELAY * (2 ** retry_count)  # Exponential backoff
            logger.info(f"Retrying in {wait_time} seconds (attempt {retry_count + 1}/{OPENAI_MAX_RETRIES})")
            time.sleep(wait_time)
            return generate_completion(prompt, max_tokens, temperature, retry_count + 1)
        else:
            logger.error("Max retries exceeded due to rate limiting")
            raise EmailGenerationError(
                "OpenAI rate limit exceeded. Please try again later."
            ) from e
            
    except APIError as e:
        logger.error(f"OpenAI API error: {e}")
        if retry_count < OPENAI_MAX_RETRIES:
            wait_time = OPENAI_RETRY_DELAY * (2 ** retry_count)
            logger.info(f"Retrying in {wait_time} seconds (attempt {retry_count + 1}/{OPENAI_MAX_RETRIES})")
            time.sleep(wait_time)
            return generate_completion(prompt, max_tokens, temperature, retry_count + 1)
        else:
            logger.error("Max retries exceeded due to API errors")
            raise EmailGenerationError(
                f"Failed to generate email after {OPENAI_MAX_RETRIES} attempts. "
                "Please check your connection and try again."
            ) from e
            
    except OpenAIError as e:
        logger.error(f"OpenAI error: {e}")
        raise EmailGenerationError(
            "An error occurred while communicating with OpenAI. Please try again."
        ) from e
        
    except Exception as e:
        logger.error(f"Unexpected error in generate_completion: {e}", exc_info=True)
        raise EmailGenerationError(
            "An unexpected error occurred during email generation."
        ) from e


def get_subject_lines(inputs: Dict[str, any], max_lines: int = 5) -> List[str]:
    """
    Generate multiple subject line suggestions for an email.
    
    Args:
        inputs: Dictionary containing email context (recipient, tone, purpose, etc.)
        max_lines: Maximum number of subject lines to return
        
    Returns:
        List of subject line suggestions
        
    Raises:
        EmailGenerationError: If generation fails
    """
    try:
        logger.info("Generating subject lines")
        prompt = build_subject_prompt(inputs)
        output = generate_completion(prompt)
        
        # Parse the output - remove numbering and clean up
        subjects = []
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
            # Remove common numbering patterns
            for prefix in ['1. ', '2. ', '3. ', '4. ', '5. ', '- ', '* ', '• ']:
                if line.startswith(prefix):
                    line = line[len(prefix):]
                    break
            subjects.append(line)
        
        # Return requested number of subject lines
        result = subjects[:max_lines] if len(subjects) >= max_lines else subjects
        logger.info(f"Generated {len(result)} subject lines")
        return result
        
    except EmailGenerationError:
        raise
    except Exception as e:
        logger.error(f"Error generating subject lines: {e}", exc_info=True)
        raise EmailGenerationError("Failed to generate subject lines") from e


def get_email_drafts(
    inputs: Dict[str, any], 
    template: Optional[str] = "",
    num_drafts: int = 2
) -> List[str]:
    """
    Generate multiple email drafts with varying styles.
    
    Args:
        inputs: Dictionary containing email context
        template: Optional email template to base drafts on
        num_drafts: Number of draft variations to generate
        
    Returns:
        List of email draft strings
        
    Raises:
        EmailGenerationError: If generation fails
    """
    try:
        logger.info(f"Generating {num_drafts} email drafts")
        drafts = []
        
        for i in range(1, num_drafts + 1):
            try:
                logger.debug(f"Generating draft {i}/{num_drafts}")
                draft = generate_completion(build_email_prompt(inputs, i, template))
                drafts.append(draft)
            except EmailGenerationError as e:
                logger.error(f"Failed to generate draft {i}: {e}")
                # Add error message as placeholder
                drafts.append(f"[Error generating draft {i}: {str(e)}]")
        
        logger.info(f"Successfully generated {len(drafts)} drafts")
        return drafts
        
    except Exception as e:
        logger.error(f"Error generating email drafts: {e}", exc_info=True)
        raise EmailGenerationError("Failed to generate email drafts") from e


def estimate_cost(prompt_tokens: int, completion_tokens: int, model: str = OPENAI_MODEL) -> float:
    """
    Estimate the cost of an API call.
    
    Args:
        prompt_tokens: Number of tokens in the prompt
        completion_tokens: Number of tokens in the completion
        model: Model name used
        
    Returns:
        Estimated cost in USD
    """
    from config import GPT_35_TURBO_INPUT_COST, GPT_35_TURBO_OUTPUT_COST
    from config import GPT_4_INPUT_COST, GPT_4_OUTPUT_COST
    
    if "gpt-4" in model.lower():
        input_cost = (prompt_tokens / 1000) * GPT_4_INPUT_COST
        output_cost = (completion_tokens / 1000) * GPT_4_OUTPUT_COST
    else:  # Default to GPT-3.5 pricing
        input_cost = (prompt_tokens / 1000) * GPT_35_TURBO_INPUT_COST
        output_cost = (completion_tokens / 1000) * GPT_35_TURBO_OUTPUT_COST
    
    return input_cost + output_cost
