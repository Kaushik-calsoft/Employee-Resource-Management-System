from sqlalchemy import String , Text , Date
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

class Projects(Base):
    __tablename__ = "projects"
    __table_args__ = {"schema": "Employee_resource_management"}

    id:Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(100) , nullable=False)
    description:Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date:Mapped[date] = mapped_column(Date, nullable=False)
    end_date:Mapped[date | None] = mapped_column(Date, nullable=True)
    status:Mapped[str] = mapped_column(String(20),nullable=False)

    assignments:Mapped[list["Assignment"]] = relationship(back_populates="project")
