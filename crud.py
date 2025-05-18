from database import get_connection
from datetime import datetime

def create_task(data):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute('''
        INSERT INTO tasks (title, description, created_at, due_date, status, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data.title, data.description, now, 
          data.due_date.isoformat() if data.due_date else None,
          "pending", data.category))
    conn.commit()
    task_id = cursor.lastrowid
    return get_task_by_id(task_id)

def get_all_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    return [dict(zip([col[0] for col in conn.description], row)) for row in rows]

def get_task_by_id(task_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row:
        return dict(zip([col[0] for col in conn.description], row))
    return None

# Similarly, add update_task, delete_task functions
