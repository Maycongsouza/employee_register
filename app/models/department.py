try:
    from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
    from sqlalchemy.orm import relationship
    from app.database.base import Base
except Exception as error:
    raise ("Erro de biblioteca: %s" % error)


class Department(Base):
    __tablename__ = "department"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String,
        nullable=False,
        unique=True
    )
    leader_id = Column(
        Integer,
        ForeignKey("employee.id")
    )

    leader = relationship(
        "Employee",
        foreign_keys=[leader_id]
    )