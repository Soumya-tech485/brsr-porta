import sys
import os

# Add the backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.database import engine, Base
# Import all models so Base knows about them
from app.models import core, entry, ml, review

print("Creating tables via SQLAlchemy...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Tables created.")

# Now we need to insert the demo data.
# It's easier to just execute the INSERT statements from the SQL files.
# We will read seed_indicators.sql and seed_demo.sql, extract INSERT INTO lines, and execute them.

import sqlite3

conn = sqlite3.connect('../esgraph.db')
cur = conn.cursor()

def run_inserts(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # split by semicolon
    statements = content.split(';')
    for stmt in statements:
        stmt = stmt.strip()
        if stmt.upper().startswith('INSERT INTO'):
            try:
                cur.execute(stmt)
            except Exception as e:
                print(f"Error inserting: {e}\n{stmt[:100]}")

print("Inserting data...")
run_inserts('../database/seed_indicators.sql')
run_inserts('../database/seed_demo.sql')

conn.commit()
conn.close()
print("Database re-initialized successfully!")
