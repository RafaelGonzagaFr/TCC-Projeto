from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, registry, mapped_column

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename = 'users'

    id: Mapped[int]
    name: Mapped[str]
    matricula: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        onupdate=func.now(),
        nullable=True,
        server_default=func.now(),
    )