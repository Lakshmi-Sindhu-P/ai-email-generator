"""
Database operations for storing email generation logs.
Uses SQLite for local persistence.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from contextlib import contextmanager
from config import DB_PATH
from logger import setup_logger

logger = setup_logger(__name__)


class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Ensures proper connection handling and cleanup.
    
    Yields:
        sqlite3.Connection: Database connection
        
    Raises:
        DatabaseError: If connection fails
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise DatabaseError(f"Database operation failed: {e}") from e
    finally:
        if conn:
            conn.close()


def init_db() -> None:
    """
    Initialize the database with required tables.
    Creates tables if they don't exist.
    
    Raises:
        DatabaseError: If database initialization fails
    """
    try:
        logger.info(f"Initializing database at {DB_PATH}")
        
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            # Main email logs table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS email_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipient TEXT NOT NULL,
                    subject_context TEXT,
                    tone TEXT,
                    purpose TEXT,
                    bullet_points TEXT,
                    length TEXT,
                    additional_notes TEXT,
                    subjects TEXT,
                    draft1 TEXT,
                    draft2 TEXT,
                    timestamp TEXT NOT NULL,
                    is_favorite INTEGER DEFAULT 0,
                    cost_estimate REAL DEFAULT 0.0
                )
            """)
            
            # Create index for faster queries
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON email_logs(timestamp DESC)
            """)
            
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_favorite 
                ON email_logs(is_favorite)
            """)
            
            logger.info("Database initialized successfully")
            
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error initializing database: {e}")
        raise DatabaseError("Failed to initialize database") from e


def save_email_log(
    inputs: Dict[str, any],
    subjects: List[str],
    drafts: List[str],
    cost_estimate: float = 0.0
) -> int:
    """
    Save a generated email log to the database.
    
    Args:
        inputs: Dictionary containing user inputs
        subjects: List of generated subject lines
        drafts: List of generated email drafts
        cost_estimate: Estimated cost of API calls
        
    Returns:
        ID of the inserted record
        
    Raises:
        DatabaseError: If save operation fails
    """
    try:
        logger.info("Saving email log to database")
        
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO email_logs (
                    recipient, subject_context, tone, purpose, bullet_points, length,
                    additional_notes, subjects, draft1, draft2, timestamp, cost_estimate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                inputs.get('recipient', ''),
                inputs.get('subject_context', ''),
                inputs.get('tone', ''),
                inputs.get('purpose', ''),
                "; ".join(inputs.get('bullet_points', [])),
                inputs.get('length', ''),
                inputs.get('additional_notes', ''),
                "; ".join(subjects),
                drafts[0] if len(drafts) > 0 else '',
                drafts[1] if len(drafts) > 1 else '',
                datetime.now().isoformat(),
                cost_estimate
            ))
            
            record_id = cur.lastrowid
            logger.info(f"Email log saved with ID: {record_id}")
            return record_id
            
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Error saving email log: {e}")
        raise DatabaseError("Failed to save email log") from e


def get_email_logs(limit: int = 50, offset: int = 0, favorites_only: bool = False) -> List[Dict]:
    """
    Retrieve email logs from the database.
    
    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
        favorites_only: If True, only return favorited emails
        
    Returns:
        List of email log dictionaries
        
    Raises:
        DatabaseError: If retrieval fails
    """
    try:
        logger.info(f"Retrieving email logs (limit={limit}, offset={offset}, favorites_only={favorites_only})")
        
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            query = "SELECT * FROM email_logs"
            if favorites_only:
                query += " WHERE is_favorite = 1"
            query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            
            cur.execute(query, (limit, offset))
            rows = cur.fetchall()
            
            # Convert rows to dictionaries
            logs = [dict(row) for row in rows]
            logger.info(f"Retrieved {len(logs)} email logs")
            return logs
            
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving email logs: {e}")
        raise DatabaseError("Failed to retrieve email logs") from e


def get_email_log_by_id(log_id: int) -> Optional[Dict]:
    """
    Retrieve a specific email log by ID.
    
    Args:
        log_id: ID of the log to retrieve
        
    Returns:
        Dictionary containing log data, or None if not found
        
    Raises:
        DatabaseError: If retrieval fails
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM email_logs WHERE id = ?", (log_id,))
            row = cur.fetchone()
            return dict(row) if row else None
            
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving email log {log_id}: {e}")
        raise DatabaseError(f"Failed to retrieve email log {log_id}") from e


def toggle_favorite(log_id: int) -> bool:
    """
    Toggle the favorite status of an email log.
    
    Args:
        log_id: ID of the log to toggle
        
    Returns:
        New favorite status (True/False)
        
    Raises:
        DatabaseError: If update fails
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            # Get current status
            cur.execute("SELECT is_favorite FROM email_logs WHERE id = ?", (log_id,))
            row = cur.fetchone()
            
            if not row:
                raise DatabaseError(f"Email log {log_id} not found")
            
            new_status = 0 if row['is_favorite'] else 1
            
            # Update status
            cur.execute(
                "UPDATE email_logs SET is_favorite = ? WHERE id = ?",
                (new_status, log_id)
            )
            
            logger.info(f"Toggled favorite status for log {log_id} to {bool(new_status)}")
            return bool(new_status)
            
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Error toggling favorite for log {log_id}: {e}")
        raise DatabaseError(f"Failed to toggle favorite status") from e


def delete_email_log(log_id: int) -> None:
    """
    Delete an email log from the database.
    
    Args:
        log_id: ID of the log to delete
        
    Raises:
        DatabaseError: If deletion fails
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM email_logs WHERE id = ?", (log_id,))
            
            if cur.rowcount == 0:
                raise DatabaseError(f"Email log {log_id} not found")
            
            logger.info(f"Deleted email log {log_id}")
            
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Error deleting email log {log_id}: {e}")
        raise DatabaseError(f"Failed to delete email log {log_id}") from e


def get_total_cost() -> float:
    """
    Calculate total estimated cost of all generated emails.
    
    Returns:
        Total cost in USD
        
    Raises:
        DatabaseError: If calculation fails
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT SUM(cost_estimate) as total FROM email_logs")
            row = cur.fetchone()
            return row['total'] if row['total'] else 0.0
            
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Error calculating total cost: {e}")
        raise DatabaseError("Failed to calculate total cost") from e
