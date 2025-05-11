# alembic/env.py
import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

# --- Import your application's settings and Base for models ---
from app.config import settings as app_settings # Your application settings
from app.db.base_class import Base         # Your SQLAlchemy declarative base
from app.models import *                   # Import all your models to register them with Base.metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the metadata for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use the synchronous DSN from our application settings for offline mode
    url = str(app_settings.SQLALCHEMY_DATABASE_URI)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """
    Helper function to run migrations.
    This is called by run_migrations_online.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Get the Alembic configuration section
    alembic_config_section = config.get_section(config.config_ini_section)
    if alembic_config_section is None:
        alembic_config_section = {} # Ensure it's a dict

    alembic_config_section["sqlalchemy.url"] = str(app_settings.ASYNC_SQLALCHEMY_DATABASE_URI)


    connectable = async_engine_from_config(
        alembic_config_section, # Use the modified configuration
        prefix="sqlalchemy.",   # Standard prefix for SQLAlchemy settings in .ini
        poolclass=pool.NullPool,
        future=True,            # Use SQLAlchemy 2.0 features
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())