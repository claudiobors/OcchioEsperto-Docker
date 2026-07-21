"""
OcchioEsperto.it — SQLAlchemy ORM models for the application database.
Users, payments, leads, and user garages.
"""
import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey,
    create_engine, Enum as SAEnum, text as sa_text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import enum

from .config import DATABASE_URL

Base = declarative_base()


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class UserPlan(str, enum.Enum):
    FREE = "free"
    INTERMEDIO = "intermedio"
    AVANZATO = "avanzato"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), default="")
    role = Column(SAEnum(UserRole), default=UserRole.USER, nullable=False)
    plan = Column(SAEnum(UserPlan), default=UserPlan.FREE, nullable=False)
    stripe_customer_id = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    vespe = relationship("UserVespa", back_populates="user", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


class UserVespa(Base):
    """Vespa saved in user's digital garage."""
    __tablename__ = "user_vespe"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    display_name = Column(String(255), nullable=True)
    model_id = Column(Integer, nullable=True)
    model_name = Column(String(255), nullable=False)
    model_slug = Column(String(255), nullable=True)
    year = Column(Integer, nullable=True)
    frame_number = Column(String(100), nullable=True)
    engine_number = Column(String(100), nullable=True)
    color_name = Column(String(100), nullable=True)
    color_hex = Column(String(7), nullable=True)
    notes = Column(Text, nullable=True)
    photo_path = Column(String(500), nullable=True)
    analysis_level = Column(String(50), default="basic")
    pro_report_path = Column(String(500), nullable=True)
    analysis_json = Column(Text, nullable=True)  # JSON with full analysis
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="vespe")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    stripe_session_id = Column(String(255), unique=True, nullable=True)
    stripe_payment_intent = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="EUR")
    plan = Column(String(50), nullable=False)
    status = Column(String(50), default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="payments")


class Lead(Base):
    """Lead generated from 'Vendi' button."""
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    model_name = Column(String(255), nullable=False)
    year = Column(Integer, nullable=True)
    condition = Column(String(50), nullable=True)
    price_asked = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=True)
    photo_path = Column(String(500), nullable=True)
    status = Column(String(50), default="new")  # new, contacted, completed, archived
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="leads")


# Database engine and session
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite needs this
    echo=False,
)


def _enable_wal_mode():
    """Enable WAL mode on SQLite for better concurrent read performance."""
    with engine.connect() as conn:
        conn.execute(sa_text("PRAGMA journal_mode=WAL;"))
        conn.execute(sa_text("PRAGMA busy_timeout=5000;"))
        conn.execute(sa_text("PRAGMA synchronous=NORMAL;"))
        conn.commit()


# Enable WAL mode on startup
_enable_wal_mode()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create all tables in the app database."""
    Base.metadata.create_all(bind=engine)
    _ensure_user_vespe_columns()


def _ensure_user_vespe_columns():
    """Lightweight SQLite migration for garage features on existing installs."""
    with engine.connect() as conn:
        columns = {row[1] for row in conn.execute(sa_text("PRAGMA table_info(user_vespe);"))}
        migrations = {
            "display_name": "ALTER TABLE user_vespe ADD COLUMN display_name VARCHAR(255)",
            "analysis_level": "ALTER TABLE user_vespe ADD COLUMN analysis_level VARCHAR(50) DEFAULT 'basic'",
            "pro_report_path": "ALTER TABLE user_vespe ADD COLUMN pro_report_path VARCHAR(500)",
        }
        for column, sql in migrations.items():
            if column not in columns:
                conn.execute(sa_text(sql))
        conn.commit()


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()