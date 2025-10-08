"""
Async email generation module for parallel processing.
Improves performance by generating multiple drafts simultaneously.
"""
import asyncio
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_MAX_TOKENS, OPENAI_TEMPERATURE
from logger import setup_logger
from prompts import build_subject_prompt, build_email_prompt
from email_generator import EmailGenerationError

logger = setup_logger(__name__)

# Create async OpenAI client
async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def generate_completion_async(
    prompt: str,
    max_tokens: int = OPENAI_MAX_TOKENS,
    temperature: float = OPENAI_TEMPERATURE
) -> str:
    """
    Async version of generate_completion.
    
    Args:
        prompt: The prompt to send to the API
        max_tokens: Maximum tokens in response
        temperature: Temperature for generation
        
    Returns:
        Generated text completion
        
    Raises:
        EmailGenerationError: If generation fails
    """
    try:
        logger.debug(f"Async generating completion with model: {OPENAI_MODEL}")
        
        response = await async_client.chat.completions.create(
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
        logger.debug("Async completion generated successfully")
        
        return content
        
    except Exception as e:
        logger.error(f"Error in async generation: {e}")
        raise EmailGenerationError(f"Async generation failed: {e}") from e


async def get_subject_lines_async(inputs: Dict[str, any], max_lines: int = 5) -> List[str]:
    """
    Async version of get_subject_lines.
    
    Args:
        inputs: Dictionary containing email context
        max_lines: Maximum number of subject lines
        
    Returns:
        List of subject line suggestions
    """
    try:
        logger.info("Async generating subject lines")
        prompt = build_subject_prompt(inputs)
        output = await generate_completion_async(prompt)
        
        # Parse the output
        subjects = []
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
            for prefix in ['1. ', '2. ', '3. ', '4. ', '5. ', '- ', '* ', '• ']:
                if line.startswith(prefix):
                    line = line[len(prefix):]
                    break
            subjects.append(line)
        
        result = subjects[:max_lines] if len(subjects) >= max_lines else subjects
        logger.info(f"Async generated {len(result)} subject lines")
        return result
        
    except Exception as e:
        logger.error(f"Error in async subject generation: {e}")
        raise EmailGenerationError("Failed to generate subject lines") from e


async def get_email_draft_async(
    inputs: Dict[str, any],
    variation: int,
    template: Optional[str] = ""
) -> str:
    """
    Generate a single email draft asynchronously.
    
    Args:
        inputs: Dictionary containing email context
        variation: Draft variation number
        template: Optional template
        
    Returns:
        Generated email draft
    """
    try:
        logger.debug(f"Async generating draft variation {variation}")
        prompt = build_email_prompt(inputs, variation, template)
        draft = await generate_completion_async(prompt)
        return draft
    except Exception as e:
        logger.error(f"Error generating draft {variation}: {e}")
        return f"[Error generating draft {variation}: {str(e)}]"


async def get_email_drafts_async(
    inputs: Dict[str, any],
    template: Optional[str] = "",
    num_drafts: int = 2
) -> List[str]:
    """
    Generate multiple email drafts in parallel using asyncio.
    This is significantly faster than sequential generation.
    
    Args:
        inputs: Dictionary containing email context
        template: Optional template
        num_drafts: Number of drafts to generate
        
    Returns:
        List of generated email drafts
    """
    try:
        logger.info(f"Async generating {num_drafts} email drafts in parallel")
        
        # Create tasks for parallel execution
        tasks = [
            get_email_draft_async(inputs, i, template)
            for i in range(1, num_drafts + 1)
        ]
        
        # Execute all tasks in parallel
        drafts = await asyncio.gather(*tasks)
        
        logger.info(f"Successfully generated {len(drafts)} drafts in parallel")
        return list(drafts)
        
    except Exception as e:
        logger.error(f"Error in async draft generation: {e}")
        raise EmailGenerationError("Failed to generate email drafts") from e


async def generate_email_complete_async(
    inputs: Dict[str, any],
    template: Optional[str] = "",
    num_drafts: int = 2,
    num_subjects: int = 5
) -> tuple[List[str], List[str]]:
    """
    Generate both subject lines and email drafts in parallel.
    This is the most efficient way to generate a complete email set.
    
    Args:
        inputs: Dictionary containing email context
        template: Optional template
        num_drafts: Number of drafts to generate
        num_subjects: Number of subject lines to generate
        
    Returns:
        Tuple of (subject_lines, email_drafts)
    """
    try:
        logger.info("Starting complete async email generation")
        
        # Generate subjects and drafts in parallel
        subjects_task = get_subject_lines_async(inputs, num_subjects)
        drafts_task = get_email_drafts_async(inputs, template, num_drafts)
        
        subjects, drafts = await asyncio.gather(subjects_task, drafts_task)
        
        logger.info("Complete async email generation finished")
        return subjects, drafts
        
    except Exception as e:
        logger.error(f"Error in complete async generation: {e}")
        raise EmailGenerationError("Failed to generate complete email set") from e


def run_async_generation(
    inputs: Dict[str, any],
    template: Optional[str] = "",
    num_drafts: int = 2,
    num_subjects: int = 5
) -> tuple[List[str], List[str]]:
    """
    Synchronous wrapper for async generation.
    Use this in Streamlit or other sync contexts.
    
    Args:
        inputs: Dictionary containing email context
        template: Optional template
        num_drafts: Number of drafts
        num_subjects: Number of subject lines
        
    Returns:
        Tuple of (subject_lines, email_drafts)
    """
    try:
        # Create event loop if one doesn't exist
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the async function
        return loop.run_until_complete(
            generate_email_complete_async(inputs, template, num_drafts, num_subjects)
        )
    except Exception as e:
        logger.error(f"Error in sync wrapper: {e}")
        raise EmailGenerationError("Failed to run async generation") from e


# Performance comparison function
async def benchmark_async_vs_sync(inputs: Dict[str, any], iterations: int = 3) -> Dict[str, float]:
    """
    Benchmark async vs sync generation for performance comparison.
    
    Args:
        inputs: Test inputs
        iterations: Number of test iterations
        
    Returns:
        Dictionary with timing results
    """
    import time
    from email_generator import get_subject_lines, get_email_drafts
    
    logger.info(f"Running performance benchmark ({iterations} iterations)")
    
    # Test async
    async_times = []
    for i in range(iterations):
        start = time.time()
        await generate_email_complete_async(inputs)
        async_times.append(time.time() - start)
    
    # Test sync
    sync_times = []
    for i in range(iterations):
        start = time.time()
        get_subject_lines(inputs)
        get_email_drafts(inputs)
        sync_times.append(time.time() - start)
    
    avg_async = sum(async_times) / len(async_times)
    avg_sync = sum(sync_times) / len(sync_times)
    speedup = avg_sync / avg_async
    
    results = {
        "async_avg": avg_async,
        "sync_avg": avg_sync,
        "speedup": speedup,
        "improvement_percent": (speedup - 1) * 100
    }
    
    logger.info(f"Benchmark results: {speedup:.2f}x speedup with async")
    return results

