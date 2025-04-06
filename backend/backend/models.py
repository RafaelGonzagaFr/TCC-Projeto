from datetime import datetime
from enum import Enum

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()

class Tipo(str, Enum):
    professor = 'professor'
    aluno = 'aluno'
    adm = 'adm'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    matricula: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    tipo: Mapped[Tipo]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        onupdate=func.now(),
        nullable=True,
        server_default=func.now(),
    )
