from sqlalchemy import MetaData, Table
from app.db.database import engine

metadata = MetaData()

category_table = Table("categories", metadata, autoload_with=engine)