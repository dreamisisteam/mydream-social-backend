from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(16) NOT NULL UNIQUE,
    "telegram_link" VARCHAR(128) NOT NULL UNIQUE,
    "name" VARCHAR(16) NOT NULL,
    "surname" VARCHAR(32),
    "password" VARCHAR(128),
    "interests" JSONB NOT NULL
    );
    COMMENT ON TABLE "user" IS 'Пользователь.';
    CREATE TABLE IF NOT EXISTS "aerich" (
        "id" SERIAL NOT NULL PRIMARY KEY,
        "version" VARCHAR(255) NOT NULL,
        "app" VARCHAR(100) NOT NULL,
        "content" JSONB NOT NULL
    );
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
