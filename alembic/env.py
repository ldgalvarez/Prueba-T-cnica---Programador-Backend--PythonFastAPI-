from __future__ import annotations
import os, sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from alembic import context
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# Asegurar que el path de la app esté disponible
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

config = context.config

# Construir DATABASE_URL manualmente desde variables de entorno
if config.get_main_option("sqlalchemy.url") is None:
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB")
    
    if not all([db_user, db_password, db_host, db_port, db_name]):
        raise RuntimeError("Faltan variables de entorno de PostgreSQL")
    
    # Construir URL síncrona para Alembic
    sync_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    print(f"Using database URL: {sync_url}")
    config.set_main_option("sqlalchemy.url", sync_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.db.base import Base  # noqa
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:  # type: Connection
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()