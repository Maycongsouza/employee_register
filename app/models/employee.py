try:
    from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Enum
    from sqlalchemy.orm import relationship
    from sqlalchemy import event
    from sqlalchemy.orm import Session, validates
    from sqlalchemy.exc import IntegrityError
    from app.database.base import Base
    from app.models.job import Job
    import enum
except Exception as error:
    raise ("Erro de biblioteca: %s" % error)

class StateEnum(enum.Enum):
    active = "Active"
    archived = "Archived"


class Employee(Base):
    __tablename__ = "employee"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String,
        nullable=False
    )
    last_name = Column(
        String,
        nullable=False
    )
    register_number = Column(
        String,
        unique=True,
        nullable=False
    )
    job_id = Column(
        Integer,
        ForeignKey("job.id"),
        nullable=False
    )
    department_id = Column(
        Integer,
        ForeignKey("department.id")
    )
    salary = Column(
        Float,
        nullable=False
    )
    status = Column(
        Enum(StateEnum),
        default=StateEnum.active
    )

    job = relationship(
        "Job",
        foreign_keys=[job_id]
    )
    department = relationship(
        "Department",
        foreign_keys=[department_id]
    )
