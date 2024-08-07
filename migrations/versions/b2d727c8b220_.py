"""empty message

Revision ID: b2d727c8b220
Revises: 52b69b4bd5a5
Create Date: 2024-07-13 10:35:51.585175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2d727c8b220'
down_revision = '52b69b4bd5a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('text_section', schema=None) as batch_op:
        batch_op.add_column(sa.Column('text_hash', sa.Integer()))
        batch_op.drop_index('ix_text_section_language_id')
        batch_op.drop_index('ix_text_section_text_section')
        batch_op.create_unique_constraint(None, ['text_hash'])

    with op.batch_alter_table('typing_session', schema=None) as batch_op:
        batch_op.drop_index('ix_typing_session_completion_time')
        batch_op.drop_index('ix_typing_session_text_id')

    with op.batch_alter_table('typing_session_deltas', schema=None) as batch_op:
        batch_op.drop_index('ix_typing_session_deltas_characters')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('typing_session_deltas', schema=None) as batch_op:
        batch_op.create_index('ix_typing_session_deltas_characters', ['characters'], unique=False)

    with op.batch_alter_table('typing_session', schema=None) as batch_op:
        batch_op.create_index('ix_typing_session_text_id', ['text_id'], unique=False)
        batch_op.create_index('ix_typing_session_completion_time', ['completion_time'], unique=False)

    with op.batch_alter_table('text_section', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('ix_text_section_text_section', ['text_section'], unique=False)
        batch_op.create_index('ix_text_section_language_id', ['language_id'], unique=False)
        batch_op.drop_column('text_hash')

    # ### end Alembic commands ###
