import sqlite3

def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # 1. Create USERS Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'user', -- 'user', 'developer', 'lawyer', 'admin'
            project_name TEXT -- Assigned project for Homeowners/Developers
        )
    ''')

    # 2. Create DEFECTS Table (Added user_id column)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS defects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, -- Links defect to a specific user
            project_name TEXT,
            unit_no TEXT,
            description TEXT,
            status TEXT DEFAULT 'draft', -- 'draft', 'locked', 'in_progress', 'completed'
            severity TEXT DEFAULT 'Low', -- 'High', 'Medium', 'Low'
            filename TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # 3. Insert Default Users (So you can still log in)
    users = [
        ('admin@uum.edu.my', 'admin123', 'System Administrator', 'admin', 'ALL'),
        ('lawyer@firm.com', 'law123', 'Pn. Zulaikha', 'lawyer', 'ALL'),
        ('developer@ecoworld.com', 'dev123', 'EcoWorld Contractor', 'developer', 'ALL'),
        ('abbas@student.uum.edu.my', 'password123', 'Abbas Abu Dzarr', 'user', 'ASMARINDA12')
    ]

    for email, pwd, name, role, proj in users:
        try:
            cursor.execute('INSERT INTO users (email, password, full_name, role, project_name) VALUES (?, ?, ?, ?, ?)', 
                           (email, pwd, name, role, proj))
        except sqlite3.IntegrityError:
            pass # User already exists

    conn.commit()
    conn.close()
    print("Database initialized with Users and Linked Defects.")

if __name__ == '__main__':
    init_db()