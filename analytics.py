from database import get_connection
from datetime import datetime

def get_task_stats():
    conn = get_connection()
    stats = {}

    stats['total_tasks'] = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    stats['pending_tasks'] = conn.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'").fetchone()[0]
    stats['completed_tasks'] = conn.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'").fetchone()[0]

    now = datetime.utcnow().isoformat()
    stats['overdue_tasks'] = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'pending' AND due_date IS NOT NULL AND due_date < ?", (now,)
    ).fetchone()[0]

    category_counts = conn.execute(
        "SELECT category, COUNT(*) FROM tasks GROUP BY category"
    ).fetchall()
    stats['tasks_by_category'] = {cat: count for cat, count in category_counts if cat}

    return stats
