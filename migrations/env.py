import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from migrations.base import Base
from src.config.database.db_config import settings_db

config = context.config

section = config.config_ini_section
config.set_section_option(section, "POSTGRES_HOST", settings_db.HOST)
config.set_section_option(section, "POSTGRES_PORT", str(settings_db.PORT))
config.set_section_option(section, "POSTGRES_USER", settings_db.USER)
config.set_section_option(section, "POSTGRES_DB", settings_db.DB)
config.set_section_option(section, "POSTGRES_PASSWORD", settings_db.PASSWORD)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url", settings_db.database_url + "?async_fallback=True")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    url = config.get_main_option("sqlalchemy.url", settings_db.database_url + "?async_fallback=True")
    connectable = create_async_engine(url, pool_pre_ping=True)
    async with connectable.connect() as conn:
        await conn.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata
            )
        )
        async with conn.begin():
            await conn.run_sync(lambda sync_conn: context.run_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
