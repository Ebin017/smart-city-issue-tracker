import os
import shutil #for copy image
import sqlite3
from datetime import datetime

from unicodedata import category

conn = sqlite3.connect('issues.db')
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    category TEXT,
    location TEXT,
    image_path TEXT,
    status TEXT,
    date_reported TEXT
)
""")

conn.commit()
conn.close() #close connection


def add_issue(name, description, category, location, image_file):

    #Copy the image to uploads folder
    image_path = os.path.join("uploads", os.path.basename(image_file))
    shutil.copy(image_file, image_path)  # copies the image file

    #Get current date & time
    date_reported = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #Insert into database
    conn = sqlite3.connect('issues.db')
    c = conn.cursor()

    c.execute("""
        INSERT INTO issues (name, description, category, location, image_path, status, date_reported)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, description, category, location, image_path, "Pending", date_reported))

    conn.commit()
    conn.close()

    print("Issue added successfully!")



def view_issues():
    conn = sqlite3.connect('issues.db')
    c = conn.cursor()

    c.execute("""select * from issues""")
    rows = c.fetchall()  #fetch all results

    conn.close()

    for row in rows:
        print(row)


def update_status(issue_id, new_status):
    conn = sqlite3.connect('issues.db')
    c = conn.cursor()

    # Update the status
    c.execute("""
        UPDATE issues
        SET status = ?
        WHERE id = ?
    """, (new_status, issue_id))

    conn.commit()
    conn.close()

    print(f"Issue {issue_id} status updated to '{new_status}'")


def delete_issue(issue_id):
    conn = sqlite3.connect('issues.db')
    c = conn.cursor()

    # Delete the issue
    c.execute("""
        DELETE FROM issues
        WHERE id = ?
    """, (issue_id,))

    conn.commit()
    conn.close()

    print(f"Issue {issue_id} has been deleted successfully!")

if __name__ == "__main__":
    add_issue(
        "Ebin",
        "Broken streetlight near park",
        "Streetlight",
        "MG Road",
        r"C:\Users\Ebin raj\OneDrive\Desktop\errr.jpg" # path to your image
    )

    view_issues()  # optional: see all issues in the console



