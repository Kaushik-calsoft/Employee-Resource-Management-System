"""initial schema

Revision ID: 4b28259bce4d
Revises: 
Create Date: 2026-11-26 14:29:01.788302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4b28259bce4d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column('assignments', 'status',
               existing_type=sa.VARCHAR(length=20),
               nullable=True,
               schema='Employee_resource_management')
    op.alter_column('employees', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=False,
               schema='Employee_resource_management')
    op.alter_column('projects', 'status',
               existing_type=sa.VARCHAR(length=20),
               nullable=False,
               schema='Employee_resource_management')



def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column('projects', 'status',
               existing_type=sa.VARCHAR(length=20),
               nullable=True,
               schema='Employee_resource_management')
    op.alter_column('employees', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=True,
               schema='Employee_resource_management')
    op.alter_column('assignments', 'status',
               existing_type=sa.VARCHAR(length=20),
               nullable=False,
               schema='Employee_resource_management')
    
