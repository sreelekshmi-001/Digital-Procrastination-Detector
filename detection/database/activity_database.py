import sqlite3
from datetime import datetime


DATABASE_NAME = "productivity.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Activity table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            window_title TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    # Check existing columns
    cursor.execute("PRAGMA table_info(activity_log)")

    columns = [column[1] for column in cursor.fetchall()]

    # Add duration column if missing
    if "duration" not in columns:

        cursor.execute("""
            ALTER TABLE activity_log
            ADD COLUMN duration INTEGER DEFAULT 0
        """)

        print("Duration column added successfully.")

    # Settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            daily_goal INTEGER NOT NULL
        )
    """)

    # Create default goal if it doesn't exist
    cursor.execute("""
        SELECT COUNT(*)
        FROM settings
    """)

    count = cursor.fetchone()[0]

    if count == 0:

        cursor.execute("""
            INSERT INTO settings
            (id, daily_goal)
            VALUES (1, 7200)
        """)

        print("Default daily goal set to 2 hours.")

    connection.commit()
    connection.close()


def save_activity(window_title, category, duration=0):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO activity_log
        (timestamp, window_title, category, duration)
        VALUES (?, ?, ?, ?)
    """, (
        timestamp,
        window_title,
        category,
        duration
    ))

    connection.commit()
    connection.close()


def get_daily_goal():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT daily_goal
        FROM settings
        WHERE id = 1
    """)

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return 7200


def set_daily_goal(minutes):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    goal_seconds = minutes * 60

    cursor.execute("""
        UPDATE settings
        SET daily_goal = ?
        WHERE id = 1
    """, (goal_seconds,))

    connection.commit()
    connection.close()


if __name__ == "__main__":

    create_database()

    print("Database setup completed successfully!")