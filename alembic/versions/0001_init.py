from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
import uuid

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Crear extensión si no existe
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    
    # Crear tabla users si no existe
    conn = op.get_bind()
    result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')"))
    exists = result.scalar()
    
    if not exists:
        op.create_table('users',
            sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('hashed_password', sa.String(length=255), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        )
    
    # Crear índice solo si no existe
    op.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email)')
    
    # Crear tabla tasks si no existe
    result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'tasks')"))
    exists = result.scalar()
    
    if not exists:
        op.create_table('tasks',
            sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        )
    
    # Crear índices solo si no existen
    op.execute('CREATE INDEX IF NOT EXISTS ix_tasks_title ON tasks (title)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_tasks_status ON tasks (status)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_tasks_created_at ON tasks (created_at)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_tasks_user_id ON tasks (user_id)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_tasks_user_status_created ON tasks (user_id, status, created_at)')

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')