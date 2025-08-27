from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DB_URL") + "?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def run_migrations():
    with engine.connect() as conn:
        # Check if constraint already exists
        result = conn.execute(text("""
            SELECT 1
            FROM information_schema.table_constraints
            WHERE table_name = 'news'
              AND constraint_name = 'news_url_key';
        """)).fetchone()

        if not result:  # If no constraint exists, add it
            conn.execute(text(
                "ALTER TABLE news ADD CONSTRAINT news_url_key UNIQUE (url);"
            ))
            conn.commit()
            print("✅ Added UNIQUE constraint on news.url")
        else:
            print("⚡ Constraint already exists, skipping.")

# Run migrations at startup
run_migrations()
