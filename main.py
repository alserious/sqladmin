import logging


logging.basicConfig(level="DEBUG")

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage


Base = declarative_base()
engine = create_engine(
    "sqlite:///example.db",
    connect_args={"check_same_thread": False},
)
storage = FileSystemStorage(path="/")

class User(Base):
    __tablename__ = "users"



    id = Column(Integer, primary_key=True)
    name = Column(String)
    file = Column(FileType(storage=storage))


Base.metadata.create_all(engine)  # Create tables

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
    column_list = [User.id, User.name]
    can_import=True

admin.add_view(UserAdmin)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
