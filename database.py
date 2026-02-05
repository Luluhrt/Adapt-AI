"""
Database configuration and session management.

This module handles the PostgreSQL/PostGIS database connection using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Connection string format: postgresql+driver://user:password@host:port/database
DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/pci_1"

# Create engine with echo=True for SQL logging (set to False in production)
engine = create_engine(DATABASE_URL, echo=True)

# Session factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy models
Base = declarative_base()


# =============================================================================
# DEPENDENCY INJECTION
# =============================================================================

def get_db():
    """
    Database session dependency for FastAPI.
    
    Creates a new database session for each request and ensures it's closed
    after the request is completed (even if an error occurs).
    
    Usage in FastAPI:
        @app.get("/endpoint")
        def my_endpoint(db: Session = Depends(get_db)):
            ...
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
