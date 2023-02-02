import sqlalchemy 
from .base import metadata, engine

user: sqlalchemy.Table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        name="id",
        type_= sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    ),
    sqlalchemy.Column("name", sqlalchemy.String),
    extend_existing=True
)


region: sqlalchemy.Table = sqlalchemy.Table(
    "region",
    metadata,
    sqlalchemy.Column(
        name="id",
        type_= sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    ),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("region_id", sqlalchemy.String),
    extend_existing=True
)


city: sqlalchemy.Table = sqlalchemy.Table(
    "city",
    metadata,
    sqlalchemy.Column(
        name="id",
        type_= sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    ),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("city_id", sqlalchemy.String),
    sqlalchemy.Column("latitude", sqlalchemy.DECIMAL),
    sqlalchemy.Column("longitude", sqlalchemy.DECIMAL),
    extend_existing=True
)

metadata.create_all(engine)
