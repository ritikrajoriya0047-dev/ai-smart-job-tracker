import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # SQLAlchemy strictly requires 'postgresql://' instead of 'postgres://'. 
    # Many cloud providers (like Render or Heroku) still inject 'postgres://' into environment variables.
    # This silent `.replace` saves us from frustrating crash loops in production.
    DB_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(
        DB_URL,
        connect_args={
            "sslmode": "require",
            # We set a hard connect timeout so the app fails fast if the database goes down,
            # rather than hanging requests endlessly.
            "connect_timeout": 10,
        },
        # pool_pre_ping checks if the DB connection is still alive before using it, 
        # preventing "MySQL server has gone away"-style errors on stale connections.
        pool_pre_ping=True,
        pool_recycle=300,
    )
else:
    # Local development — no SSL needed
    DB_URL = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(
        DB_URL,
        pool_pre_ping=True,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency generator that yields a database session and ensures
    the session is cleanly closed after the request is complete.
    """
    # We yield the session instead of returning it so FastAPI can inject it into the 
    # route handler, execute the request, and then cleanly hit the `finally` block 
    # to close the connection back to the connection pool. This prevents memory leaks.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()