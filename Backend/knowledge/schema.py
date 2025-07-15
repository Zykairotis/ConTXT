"""
Database schema management for PostgreSQL.
"""
import asyncpg
from Backend.config.settings import settings


class PostgresSchemaManager:
    """Manager for PostgreSQL schema operations."""
    
    async def initialize_schema(self):
        """
        Initialize the PostgreSQL schema with tables for job tracking and metadata.
        """
        conn = await asyncpg.connect(str(settings.POSTGRES_DSN))
        try:
            # Create jobs table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id UUID PRIMARY KEY,
                    status VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data JSONB
                )
            """)
            
            # Create index for status
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)
            """)
            
            # Create metadata table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    key VARCHAR(255) PRIMARY KEY,
                    value JSONB NOT NULL
                )
            """)
        finally:
            await conn.close()
