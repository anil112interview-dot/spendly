import sqlite3
import os
from werkzeug.security import generate_password_hash

def get_db():
    """Open a new database connection."""
    # Database file in project root
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spendly.db')
    db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db

def init_db():
    """Initialize the database schema if it doesn't exist yet."""
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    db.commit()

def seed_db():
    """Insert demo data if the database is empty."""
    db = get_db()
    # Check if users table already has entries
    existing_user = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if existing_user > 0:
        return  # Already seeded

    # Insert demo user
    password_hash = generate_password_hash('demo123')
    db.execute('''
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
    ''', ('Demo User', 'demo@spendly.com', password_hash))

    # Insert sample expenses
    db.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
               (1, 45.20, 'Food', '2026-06-01', 'Lunch at downtown cafe'))
    db.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
               (1, 12.50, 'Transport', '2026-06-02', 'Bus pass'))
    db.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
               (1, 78.00, 'Bills', '2026-06-03', 'Monthly electricity bill'))
    db.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
               (1, 23.99, 'Health', '2026-06-04', 'Gym membership'))
    db.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
               (1, 150.00, 'Shopping', '2026-06-05', 'New shoes'))
    db.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
               (1, 30.00, 'Entertainment', '2026-06-06', 'Streaming service subscription'))
    db.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
               (1, 100.00, 'Other', '2026-06-07', 'Donation to charity'))
    db.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
               (1, 60.00, 'Food', '2026-06-08', 'Groceries'))
    db.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
               (1, 250.00, 'Bills', '2026-06-09', 'Internet service bill'))

    db.commit()