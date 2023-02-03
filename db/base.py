import databases
import sqlalchemy

from config import DB_URI

# DB_URI = "sqlite:///./sql_app.db"

database = databases.Database(DB_URI)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DB_URI, connect_args={"check_same_thread": False})
