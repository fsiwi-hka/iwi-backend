import uuid

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class UserEntity(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)

    api_key: Mapped[str] = mapped_column(String, unique=True)