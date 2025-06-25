from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    DateTime,
    SmallInteger,
    CheckConstraint,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    sso_id = Column(Text, nullable=False, unique=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True, index=True)

    # Single role field
    role = Column(Text, nullable=False, default="Student")
    __table_args__ = (
        CheckConstraint(
            "role IN ('Admin', 'Student', 'Instructor')",
            name="chk_users_role",
        ),
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    choices = relationship("ChoiceModel", back_populates="user")


class ElectiveModel(Base):
    __tablename__ = "electives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(Text, nullable=False, unique=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    max_seats = Column(Integer, nullable=False, default=0)

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    choices = relationship("ChoiceModel", back_populates="elective")


class ChoiceModel(Base):
    __tablename__ = "choices"
    __table_args__ = (
        UniqueConstraint("user_id", "elective_id", name="uq_user_elective"),
        UniqueConstraint("user_id", "priority", name="uq_user_priority"),
        CheckConstraint("priority BETWEEN 1 AND 5", name="chk_priority_range"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    elective_id = Column(
        UUID(as_uuid=True),
        ForeignKey("electives.id", ondelete="CASCADE"),
        nullable=False,
    )
    priority = Column(SmallInteger, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    user = relationship("UserModel", back_populates="choices")
    elective = relationship("ElectiveModel", back_populates="choices")
