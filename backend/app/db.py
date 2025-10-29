from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Date, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from passlib.hash import bcrypt

engine = create_engine(settings.database_url, pool_pre_ping=True)
metadata = MetaData()

labels = Table(
    "labels", metadata,
    Column("id", Integer, primary_key=True),
    Column("class_idx", Integer, nullable=False),
    Column("label_name", String, nullable=False),
    Column("folder_name", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now())
)

samples = Table(
    "samples", metadata,
    Column("id", Integer, primary_key=True),
    Column("label_id", Integer),
    Column("file_path", String, nullable=False),
    Column("user", String),
    Column("session_id", String),
    Column("frames", Integer),
    Column("duration", String),
    Column("meta", JSON),
    Column("created_at", DateTime, server_default=func.now())
)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gender = Column(String)
    birthdate = Column(Date)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def init_db():
    metadata.create_all(engine)
    Base.metadata.create_all(engine) # type: ignore
    create_default_admin()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def create_default_admin():
    db = SessionLocal()
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if not existing_admin:
        admin = User(
            username="admin",
            email="admin@example.com",
            password=bcrypt.hash("123456"),
            role="admin",
            gender="unknown"
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created!")
    else:
        print("ℹ️ Admin user already exists!")
    db.close()