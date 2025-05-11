# sim_post_cap_backend/app/db/base_class.py
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # to generate table name from class_name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s" # e.g. World -> worlds