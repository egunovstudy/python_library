"""3nd commit

Revision ID: fc9751dd1645
Revises: 5ca36a28de78
Create Date: 2024-10-26 16:33:46.886534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc9751dd1645'
down_revision: Union[str, None] = '5ca36a28de78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_title_author_uc', 'books', ['title', 'author'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_title_author_uc', 'books', type_='unique')
    # ### end Alembic commands ###
