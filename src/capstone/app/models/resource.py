from sqlalchemy import String ,  Boolean
from sqlalchemy.orm import Mapped,mapped_column,relationship

from ..database import Base

class Resource(Base):
    __tablename__ = "resources"
    __table_args__ = {"schema": "Employee_resource_management"}

    id:Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type:Mapped[str] = mapped_column(String(100), nullable=False)
    availability:Mapped[bool] = mapped_column(Boolean,nullable=False)

    assignments: Mapped[list["Assignment"]] = relationship(back_populates="resource")
