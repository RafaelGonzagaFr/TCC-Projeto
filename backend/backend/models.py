from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


class Tipo(str, Enum):
    professor = 'professor'
    aluno = 'aluno'
    adm = 'adm'

class Status(str, Enum):
    analise = 'analise'
    aprovado = 'aprovado'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
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

@table_registry.mapped_as_dataclass
class Video:
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    url: Mapped[str]
    status: Mapped[Status]

    # Relacionamento
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )