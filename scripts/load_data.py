import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")

print(f"Connecting to database...")

try:
    engine = create_engine(db_url)
    df = pd.read_csv("data/synthetic_projects.csv")
    
    print(f"Loading {len(df)} projects...")
    df.to_sql("projects_backlog", engine, if_exists="append", index=False)
    
    print(f"✅ Loaded {len(df)} projects")
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) as count FROM projects_backlog"))
        row = result.fetchone()
        print(f"✅ Total in database: {row[0]}")
    
except Exception as e:
    print(f"❌ Error: {e}")