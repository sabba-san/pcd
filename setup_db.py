import sqlite3
import os

# Calculate path to ensure it goes in the same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'app.db')

def reset_database():
    print(f"--- DATABASE RESET TOOL ---")
    print(f"Target Database: {DB_PATH}")
    
    # 1. Connect (This creates the file if it doesn't exist)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("✓ Connected to database")
    except Exception as e:
        print(f"X Error connecting: {e}")
        return

    # 2. Drop Old Tables (Clean Slate)
    print("... Deleting old tables")
    cursor.execute("DROP TABLE IF EXISTS defects")
    cursor.execute("DROP TABLE IF EXISTS users")
    
    # 3. Create Tables (With CORRECT Columns)
    print("... Creating new schema")
    
    # Users Table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            project_name TEXT
        )
    ''')
    
    # Defects Table (With user_id link)
    cursor.execute('''
        CREATE TABLE defects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            project_name TEXT,
            unit_no TEXT,
            description TEXT,
            status TEXT DEFAULT 'draft',
            severity TEXT DEFAULT 'Low',
            filename TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # 4. Insert Default Users
    print("... Seeding default users")
    
    users = [
        ('abbas@student.uum.edu.my', 'password123', 'Abbas Abu Dzarr', 'user', 'ASMARINDA12'),
        ('developer@ecoworld.com', 'dev123', 'EcoWorld Contractor', 'developer', 'ALL'),
        ('lawyer@firm.com', 'law123', 'Pn. Zulaikha', 'lawyer', 'ALL'),
        ('admin@uum.edu.my', 'admin123', 'System Administrator', 'admin', 'ALL')
    ]
    
    for email, pwd, name, role, proj in users:
        cursor.execute("INSERT INTO users (email, password, full_name, role, project_name) VALUES (?, ?, ?, ?, ?)", 
                       (email, pwd, name, role, proj))

    # 5. Insert Sample Defect for Abbas
    print("... Adding sample defect for Abbas")
    cursor.execute("SELECT id FROM users WHERE email = 'abbas@student.uum.edu.my'")
    abbas_id = cursor.fetchone()[0]
    
    cursor.execute('''
        INSERT INTO defects (user_id, project_name, unit_no, description, status, severity, filename)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (abbas_id, 'ASMARINDA12', 'A-85', 'Cracked Wall in Master Bedroom', 'in_progress', 'Medium', 'sisiranRendered.glb'))

    conn.commit()
    conn.close()
    print("SUCCESS: Database has been reset and populated!")
    print("You can now run 'python run.py'")

if __name__ == "__main__":
    reset_database()