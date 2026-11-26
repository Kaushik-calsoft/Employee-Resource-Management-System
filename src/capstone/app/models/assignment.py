from datetime import date
from sqlalchemy import String, Date , ForeignKey
from sqlalchemy.orm import Mapped, mapped_column , relationship

from ..database import Base
from .employee import Employee
from .project import Projects
from .resource import Resource

class Assignment(Base):
    __tablename__ = "assignments"
    __table_args__ = {"schema": "Employee_resource_management"}
    

    id : Mapped[int] = mapped_column(primary_key=True,index=True, autoincrement=True)
    employee_id:Mapped[int] = mapped_column(ForeignKey("Employee_resource_management.employees.id"), nullable=False)
    project_id:Mapped[int] = mapped_column(ForeignKey("Employee_resource_management.projects.id"), nullable=False)
    resource_id:Mapped[int] = mapped_column(ForeignKey("Employee_resource_management.resources.id") ,nullable=False)
    assigned_dates:Mapped[date] = mapped_column(Date , nullable=False)
    status:Mapped[str] = mapped_column(String(20) , nullable=True)

    employee:Mapped["Employee"] = relationship(back_populates="assignments")
    project:Mapped["Projects"] = relationship(back_populates="assignments")
    resource:Mapped["Resource"] = relationship(back_populates="assignments")