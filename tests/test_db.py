"""
Tests for database operations.
"""
import pytest
import sys
import os
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Mock the DB_PATH before importing db module
import config
original_db_path = config.DB_PATH


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Create a temporary database for testing."""
    test_db_path = str(tmp_path / "test_email_generator.db")
    monkeypatch.setattr('config.DB_PATH', test_db_path)
    
    # Re-import db module to use new path
    import importlib
    import db
    importlib.reload(db)
    
    yield test_db_path
    
    # Cleanup
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


class TestInitDb:
    """Tests for init_db function."""
    
    def test_init_db_creates_database(self, temp_db):
        """Test that init_db creates the database file."""
        from db import init_db
        
        init_db()
        assert os.path.exists(temp_db)
        
    def test_init_db_creates_tables(self, temp_db):
        """Test that init_db creates required tables."""
        from db import init_db
        
        init_db()
        
        conn = sqlite3.connect(temp_db)
        cur = conn.cursor()
        
        # Check if email_logs table exists
        cur.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='email_logs'
        """)
        
        assert cur.fetchone() is not None
        conn.close()
        
    def test_init_db_idempotent(self, temp_db):
        """Test that init_db can be called multiple times safely."""
        from db import init_db
        
        # Should not raise any errors when called multiple times
        init_db()
        init_db()
        init_db()
        
        assert os.path.exists(temp_db)


class TestSaveEmailLog:
    """Tests for save_email_log function."""
    
    def test_save_email_log_basic(self, temp_db, sample_inputs, sample_subjects, sample_drafts):
        """Test basic email log saving."""
        from db import init_db, save_email_log
        
        init_db()
        log_id = save_email_log(sample_inputs, sample_subjects, sample_drafts)
        
        assert isinstance(log_id, int)
        assert log_id > 0
        
    def test_save_email_log_data_integrity(self, temp_db, sample_inputs, sample_subjects, sample_drafts):
        """Test that saved data matches input data."""
        from db import init_db, save_email_log, get_email_log_by_id
        
        init_db()
        log_id = save_email_log(sample_inputs, sample_subjects, sample_drafts, cost_estimate=0.05)
        
        # Retrieve and verify
        log = get_email_log_by_id(log_id)
        
        assert log is not None
        assert log['recipient'] == sample_inputs['recipient']
        assert log['tone'] == sample_inputs['tone']
        assert log['purpose'] == sample_inputs['purpose']
        assert sample_inputs['bullet_points'][0] in log['bullet_points']
        assert sample_subjects[0] in log['subjects']
        assert log['draft1'] == sample_drafts[0]
        assert log['draft2'] == sample_drafts[1]
        assert log['cost_estimate'] == 0.05


class TestGetEmailLogs:
    """Tests for get_email_logs function."""
    
    def test_get_email_logs_empty(self, temp_db):
        """Test getting logs from empty database."""
        from db import init_db, get_email_logs
        
        init_db()
        logs = get_email_logs()
        
        assert isinstance(logs, list)
        assert len(logs) == 0
        
    def test_get_email_logs_with_data(self, temp_db, sample_inputs, sample_subjects, sample_drafts):
        """Test getting logs with data in database."""
        from db import init_db, save_email_log, get_email_logs
        
        init_db()
        
        # Save multiple logs
        save_email_log(sample_inputs, sample_subjects, sample_drafts)
        save_email_log(sample_inputs, sample_subjects, sample_drafts)
        save_email_log(sample_inputs, sample_subjects, sample_drafts)
        
        logs = get_email_logs()
        
        assert len(logs) == 3
        assert all(isinstance(log, dict) for log in logs)
        
    def test_get_email_logs_with_limit(self, temp_db, sample_inputs, sample_subjects, sample_drafts):
        """Test getting logs with limit parameter."""
        from db import init_db, save_email_log, get_email_logs
        
        init_db()
        
        # Save 5 logs
        for _ in range(5):
            save_email_log(sample_inputs, sample_subjects, sample_drafts)
        
        logs = get_email_logs(limit=3)
        
        assert len(logs) == 3
        
    def test_get_email_logs_ordering(self, temp_db, sample_inputs, sample_subjects, sample_drafts):
        """Test that logs are ordered by timestamp descending."""
        from db import init_db, save_email_log, get_email_logs
        import time
        
        init_db()
        
        # Save logs with small delays
        id1 = save_email_log(sample_inputs, sample_subjects, sample_drafts)
        time.sleep(0.1)
        id2 = save_email_log(sample_inputs, sample_subjects, sample_drafts)
        time.sleep(0.1)
        id3 = save_email_log(sample_inputs, sample_subjects, sample_drafts)
        
        logs = get_email_logs()
        
        # Most recent should be first
        assert logs[0]['id'] == id3
        assert logs[1]['id'] == id2
        assert logs[2]['id'] == id1


class TestToggleFavorite:
    """Tests for toggle_favorite function."""
    
    def test_toggle_favorite_basic(self, temp_db, sample_inputs, sample_subjects, sample_drafts):
        """Test basic favorite toggling."""
        from db import init_db, save_email_log, toggle_favorite, get_email_log_by_id
        
        init_db()
        log_id = save_email_log(sample_inputs, sample_subjects, sample_drafts)
        
        # Initially should be 0 (not favorite)
        log = get_email_log_by_id(log_id)
        assert log['is_favorite'] == 0
        
        # Toggle to favorite
        result = toggle_favorite(log_id)
        assert result is True
        
        log = get_email_log_by_id(log_id)
        assert log['is_favorite'] == 1
        
        # Toggle back
        result = toggle_favorite(log_id)
        assert result is False
        
        log = get_email_log_by_id(log_id)
        assert log['is_favorite'] == 0
        
    def test_toggle_favorite_nonexistent(self, temp_db):
        """Test toggling favorite for non-existent log."""
        from db import init_db, toggle_favorite, DatabaseError
        
        init_db()
        
        with pytest.raises(DatabaseError):
            toggle_favorite(99999)


class TestDeleteEmailLog:
    """Tests for delete_email_log function."""
    
    def test_delete_email_log_basic(self, temp_db, sample_inputs, sample_subjects, sample_drafts):
        """Test basic log deletion."""
        from db import init_db, save_email_log, delete_email_log, get_email_log_by_id
        
        init_db()
        log_id = save_email_log(sample_inputs, sample_subjects, sample_drafts)
        
        # Delete the log
        delete_email_log(log_id)
        
        # Should not be found
        log = get_email_log_by_id(log_id)
        assert log is None
        
    def test_delete_email_log_nonexistent(self, temp_db):
        """Test deleting non-existent log."""
        from db import init_db, delete_email_log, DatabaseError
        
        init_db()
        
        with pytest.raises(DatabaseError):
            delete_email_log(99999)


class TestGetTotalCost:
    """Tests for get_total_cost function."""
    
    def test_get_total_cost_empty(self, temp_db):
        """Test getting total cost from empty database."""
        from db import init_db, get_total_cost
        
        init_db()
        total = get_total_cost()
        
        assert total == 0.0
        
    def test_get_total_cost_with_data(self, temp_db, sample_inputs, sample_subjects, sample_drafts):
        """Test calculating total cost with data."""
        from db import init_db, save_email_log, get_total_cost
        
        init_db()
        
        save_email_log(sample_inputs, sample_subjects, sample_drafts, cost_estimate=0.05)
        save_email_log(sample_inputs, sample_subjects, sample_drafts, cost_estimate=0.03)
        save_email_log(sample_inputs, sample_subjects, sample_drafts, cost_estimate=0.02)
        
        total = get_total_cost()
        
        assert total == pytest.approx(0.10, rel=1e-5)

