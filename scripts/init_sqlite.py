import sqlite3
import re
import os

def clean_sql(sql):
    # Remove SET FOREIGN_KEY_CHECKS
    sql = re.sub(r'SET FOREIGN_KEY_CHECKS\s*=\s*\d+;', '', sql)
    # Replace AUTO_INCREMENT with AUTOINCREMENT
    sql = sql.replace('AUTO_INCREMENT', 'AUTOINCREMENT')
    # For SQLite, AUTOINCREMENT must be on an INTEGER PRIMARY KEY
    sql = sql.replace('INT AUTOINCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
    # Replace ENUM(...) with TEXT
    sql = re.sub(r'ENUM\([^)]+\)', 'TEXT', sql)
    # Remove UNIQUE KEY constraints (just simple ones)
    # We will just leave them or let sqlite handle them if valid
    sql = re.sub(r'UNIQUE KEY\s*\([^)]+\),?', '', sql)
    
    # In site_entry, the trailing comma before UNIQUE KEY needs to be removed
    sql = re.sub(r',\s*\)', '\n)', sql)
    
    # Remove ON UPDATE CURRENT_TIMESTAMP
    sql = sql.replace('ON UPDATE CURRENT_TIMESTAMP', '')
    
    return sql

db_path = '../esgraph.db'
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

def run_script(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Remove USE esgraph;
    sql = sql.replace('USE esgraph;', '')
    
    # Clean up for sqlite
    sql = clean_sql(sql)
    
    # Execute statements
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    for stmt in statements:
        try:
            cur.execute(stmt)
        except Exception as e:
            print(f"Error executing: {stmt[:100]}...\nError: {e}")

run_script('../database/schema.sql')
run_script('../database/seed_indicators.sql')
run_script('../database/seed_demo.sql')

conn.commit()
conn.close()
print("SQLite database initialized successfully.")
