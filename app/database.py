from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="/SQLiteisMy146/",
    host="localhost",
    port=3306,
    database="url_shortener"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# url_db = {}