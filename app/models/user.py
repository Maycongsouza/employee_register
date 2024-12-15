try:
    from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
    from sqlalchemy.orm import relationship
    from app.database.base import Base
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)


class User(Base):
    __tablename__ = "user"
    _description = "Instância do modelo que se refere aos cadastros dos usuários"

    id = Column(
        Integer,
        primary_key=True,
        index=True)
    login = Column(
        String,
        nullable=False,
        unique=True
    )
    passw = Column(
        String,
        nullable=False
    )
    employee_id = Column(
        Integer,
        ForeignKey("employee.id"),
        unique=True
    )

    employee = relationship(
        "Employee",
        foreign_keys=[employee_id]
    )