import sqlite3, pathlib, json, datetime, os, re

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

DB = pathlib.Path(__file__).parent / "resilinc.db"
if DB.exists(): DB.unlink()

def log_step(msg, data=None):
    timestamp = datetime.datetime.now().isoformat()
    with open("logs/run_log.txt", "a") as f:
        log_entry = f"\n[{timestamp}] {msg}"
        if data:
            log_entry += f"\n{json.dumps(data, indent=2)}"
        f.write(log_entry + "\n")

log_step("Creating new SQLite database")

# Create and populate database
con = sqlite3.connect(DB.as_posix())
script_path = pathlib.Path(__file__).parent / "resilinc_db_data_script.txt"
raw = script_path.read_text()
# Normalize boolean literals in INSERTs only, preserve schema
normalized = re.sub(r'(?i)\btrue\b', '1', raw)
normalized = re.sub(r'(?i)\bfalse\b', '0', normalized)
con.executescript(normalized)

# Get table info
tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
counts = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}
con.close()

# Log results
log_step("Database created with tables", {"tables": tables, "row_counts": counts})

print("TABLES:", tables)
print("COUNTS:", counts)

# Update README with schema info
readme = pathlib.Path(__file__).parent / "README.md"
content = readme.read_text()
schema_info = "\n## Database Schema\n\n"
schema_info += "### Tables\n\n"
for table in sorted(tables):
    schema_info += f"- `{table}`: {counts[table]} rows\n"

content = content.replace("Tables will be populated after database creation.", schema_info)
readme.write_text(content)