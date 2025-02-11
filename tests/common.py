import os
from typing import Any, List

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

# TEST_DATABASE_URI_SYNC = (
#     "postgresql+psycopg2://username:password@localhost:5432/test_db"
# )
# TEST_DATABASE_URI_ASYNC = (
#     "postgresql+asyncpg://username:password@localhost:5432/test_db"
# )

test_database_uri_sync = os.environ.get(
    "TEST_DATABASE_URI_SYNC", 
    # "sqlite:///test.db?check_same_thread=False"
    "postgresql+psycopg2://username:password@172.17.0.2:5432/test_db"
)
test_database_uri_async = os.environ.get(
    "TEST_DATABASE_URI_ASYNC",
    # "sqlite+aiosqlite:///test.db",
    "postgresql+asyncpg://username:password@172.17.0.2:5432/test_db",
)


# docker run --name postgres -e POSTGRES_USER=username -e POSTGRES_PASSWORD=password -e POSTGRES_DB=test_db -d postgres -p 5432

sync_engine = create_engine(test_database_uri_sync)
async_engine = create_async_engine(test_database_uri_async)


class DummyData(dict):  # pragma: no cover
    def getlist(self, key: str) -> List[Any]:
        v = self[key]
        if not isinstance(v, (list, tuple)):
            v = [v]
        return v
