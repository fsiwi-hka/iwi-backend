from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID  # Oder sqlalchemy.UUID je nach DB
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from src.models.base import Base


class ContentEntity(Base):
    __tablename__ = "content"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    filename: Mapped[str] = mapped_column(String(255), nullable=False)

    markdown_content: Mapped[str] = mapped_column(Text, nullable=False)