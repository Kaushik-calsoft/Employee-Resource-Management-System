from sqlalchemy import String,Integer
from sqlalchemy.orm import Mapped,mapped_column,relationship

from ..database import Base

class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {"schema": "Employee_resource_management"}

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    name:Mapped[str] = mapped_column(String(100), nullable=False)
    email:Mapped[str] = mapped_column(String(100) , nullable=False)
    designation:Mapped[str] = mapped_column(String(50), nullable=False)
    department:Mapped[str] = mapped_column(String(30), nullable=False)

    assignments: Mapped[list["Assignment"]] = relationship(back_populates="employee")
