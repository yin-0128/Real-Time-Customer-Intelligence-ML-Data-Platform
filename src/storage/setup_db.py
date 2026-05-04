import psycopg2
from psycopg2 import sql

def get_connection():
    # Setup PostgreSQL connection
    # Values would normally come from environment variables
    return psycopg2.connect(
        dbname="ml_platform",
        user="user",
        password="password",
        host="localhost",
        port="5432"
    )

def setup_schema():
    conn = get_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    print("Setting up PostgreSQL schema...")

    # Create dimension table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_users (
            user_id SERIAL PRIMARY KEY,
            signup_date TIMESTAMP,
            plan_type VARCHAR(50),
            is_active BOOLEAN DEFAULT TRUE
        );
    """)

    # Create fact table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_user_events (
            event_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES dim_users(user_id),
            event_type VARCHAR(50),
            timestamp BIGINT,
            value DOUBLE PRECISION
        );
    """)

    print("Schema created successfully (fact + dimension tables).")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_schema()
