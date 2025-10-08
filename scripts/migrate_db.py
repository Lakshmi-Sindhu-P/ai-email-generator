"""
Database migration script to add new columns to existing database.
Run this once to upgrade your existing database schema.
"""
import sqlite3
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import DB_PATH

def migrate_database():
    """Add new columns to existing database schema."""
    
    print(f"Migrating database at: {DB_PATH}")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Check if columns already exist
        cur.execute("PRAGMA table_info(email_logs)")
        columns = [row[1] for row in cur.fetchall()]
        
        print(f"Current columns: {columns}")
        
        # Add is_favorite column if it doesn't exist
        if 'is_favorite' not in columns:
            print("Adding 'is_favorite' column...")
            cur.execute("ALTER TABLE email_logs ADD COLUMN is_favorite INTEGER DEFAULT 0")
            print("✅ Added 'is_favorite' column")
        else:
            print("✓ 'is_favorite' column already exists")
        
        # Add cost_estimate column if it doesn't exist
        if 'cost_estimate' not in columns:
            print("Adding 'cost_estimate' column...")
            cur.execute("ALTER TABLE email_logs ADD COLUMN cost_estimate REAL DEFAULT 0.0")
            print("✅ Added 'cost_estimate' column")
        else:
            print("✓ 'cost_estimate' column already exists")
        
        # Create indices if they don't exist
        print("Creating indices...")
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON email_logs(timestamp DESC)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_favorite ON email_logs(is_favorite)")
            print("✅ Indices created")
        except sqlite3.OperationalError as e:
            print(f"Note: {e}")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Migration completed successfully!")
        print(f"Database is now up to date at: {DB_PATH}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)

