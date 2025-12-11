from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

#Load database url from config file instead of inserting using settings function
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True) #Create a new SQLAlchemy engine instance which connects to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #SessionMaker instance used to create sessions read,insert,update,delete
Base = declarative_base() #Function to create a base class for your ORM models

# Dependency for routers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
create_engine is used to create a connection to your database. It’s like telling SQLAlchemy: “Here is the database I want to use.
sessionmaker: A factory for creating database sessions. A session is how you talk to the database (query, insert, update, delete).
declarative_base: A function that gives a base class for your ORM models (tables). All your models inherit from this base class.
pool_pre_ping=True ensures that SQLAlchemy checks if a database connection is alive before using it, avoiding errors from stale or disconnected connections.

"""