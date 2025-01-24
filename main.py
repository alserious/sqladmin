import logging
import asyncio

logging.basicConfig(level="INFO")

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage


Base = declarative_base()
# engine = create_engine(
engine = create_async_engine(
    "sqlite+aiosqlite:///example.db",
    connect_args={"check_same_thread": False},
)
storage = FileSystemStorage(path="/")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    file = Column(FileType(storage=storage))
    addresses = relationship("Address", back_populates="user")

    def __str__(self) -> str:
        return f"User {self.id}"

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")

    def __str__(self) -> str:
        return f"Address {self.id}"


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Base.metadata.create_all(engine)  # Create tables

import sys

sys.path.append("/home/alex/dev/sqladmin_fork")

from sqladmin import Admin, ModelView
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


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
    column_list = [User.id, User.name, User.addresses]
    # column_list = [User.id, User.name, User.file, User.addresses]
    column_import_list = [User.name, User.addresses]
    can_import = True


class AddressAdmin(ModelView, model=Address):
    column_list = [Address.id, Address.user_id]
    # column_list = [Address.id, Address.user_id, Address.user]
    can_import = True


admin.add_view(UserAdmin)
admin.add_view(AddressAdmin)

import uvicorn

if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

