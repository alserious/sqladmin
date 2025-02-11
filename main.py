import asyncio
import logging

logging.basicConfig(level="INFO")

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, relationship

Base = declarative_base()
# engine = create_engine(
engine = create_async_engine(
    "postgresql+asyncpg://username:password@172.17.0.2:5432/test_db",
    # "sqlite+aiosqlite:///example.db",
    # connect_args={"check_same_thread": False},
)
storage = FileSystemStorage(path="/home/alex/dev")

association_table = Table(
    "association_table",
    Base.metadata,
    Column("users_id", ForeignKey("users.id")),
    Column("addresses_id", ForeignKey("addresses.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    idd = Column(Integer)
    name = Column(String)
    file = Column(FileType(storage=storage))
    addresses: Mapped[list["Address"] | None] = relationship(
        "Address", secondary=association_table
    )

    def __str__(self) -> str:
        return f"{self.id}"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer, ForeignKey("users.id"))

    # user = relationship("User", back_populates="addresses")

    def __str__(self) -> str:
        return f"Address {self.id}"


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Base.metadata.create_all(engine)  # Create tables

import sys

sys.path.append("/home/alex/dev/sqladmin_fork")

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from sqladmin import Admin, ModelView


async def homepage(request):
    return JSONResponse({"hello": "world"})


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
    ],
)

# app = Starlette()
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    pass
    # column_list = [User.id, User.name, User.addresses]
    # form_columns = [User.name, User.mail]
    # form_columns = [User.name, User.mail]
    form_columns = [User.id, User.idd, User.name, User.file, User.addresses]
    # column_list = [User.id, User.name, User.file, User.addresses]
    # column_import_list = [User.id,User.idd, User.name, User.addresses]
    # column_import_list = [User.id, User.name, User.addresses]
    can_import = True


class AddressAdmin(ModelView, model=Address):
    pass
    # column_list = [Address.id, Address.user_id]
    # column_list = [Address.id, Address.user_id, Address.user]
    # can_import = True


admin.add_view(UserAdmin)
admin.add_view(AddressAdmin)

import uvicorn

if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

