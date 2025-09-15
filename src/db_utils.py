import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

def get_engine():
    """
    Loads environment variables and returns a SQLAlchemy engine for MySQL.
    """
    load_dotenv()
    DB_USER = os.environ.get('MYSQL_USER')
    DB_PASS = os.environ.get('MYSQL_PASSWORD')
    DB_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    DB_PORT = os.environ.get('MYSQL_PORT', '3306')
    DB_NAME = os.environ.get('MYSQL_DB')
    conn_str = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(conn_str)
