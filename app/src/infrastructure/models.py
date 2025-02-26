# -*- coding: utf-8 -*-

from typing import Optional
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Object(Base):
    __tablename__ = "objects"
    id: Mapped[str] = mapped_column("id", sa.Uuid, primary_key=True, index=True)
    active: Mapped[bool] = mapped_column("active", sa.Boolean, nullable=False)
    url: Mapped[bool] = mapped_column("url", sa.String(length=255), unique=True)
    title: Mapped[str] = mapped_column("title", sa.String(length=255))
    description: Mapped[Optional[str]] = mapped_column("description", sa.String(length=5000), nullable=True)
    region: Mapped[str] = mapped_column("region", sa.String(30))
    city: Mapped[str] = mapped_column("city", sa.String(30), index=True)
    street: Mapped[str] = mapped_column("street", sa.String(60), index=True)
    house_number: Mapped[str] = mapped_column("house_number", sa.String(5), index=True)
    city_region: Mapped[Optional[str]] = mapped_column("city_region", sa.String(60), nullable=True)
    micro_region: Mapped[Optional[str]] = mapped_column("micro_region", sa.String(60), nullable=True)
    latitude: Mapped[Decimal] = mapped_column("latitude", sa.Numeric(2,7))
    longitude: Mapped[Decimal] = mapped_column("longitude", sa.Numeric(2,7))
    price_byn: Mapped[Decimal] = mapped_column("price_byn", sa.Numeric(10,1))
    price_usd: Mapped[Decimal] = mapped_column("price_usd", sa.Numeric(10,1), index=True)
    price_m2: Mapped[Optional[Decimal]] = mapped_column("price_m2", sa.Numeric(5,4), index=True)
    build_type: Mapped[str] = mapped_column("build_type", sa.String(length=20))
    year_of_build: Mapped[int] = mapped_column("year_of_build", sa.Integer)
    floor: Mapped[Optional[int]] = mapped_column("floor", sa.Integer, nullable=True)
    floors_numb: Mapped[Optional[int]] = mapped_column("floors_numb", sa.Integer, nullable=True)
    rooms: Mapped[int] = mapped_column("rooms", sa.Integer)
    separated_rooms: Mapped[int] = mapped_column("separated_rooms", sa.Integer)
    all_separated_rooms: Mapped[str] = mapped_column("all_separated_rooms",sa.Boolean)
    area: Mapped[Decimal] = mapped_column("area", sa.Numeric(6,2), index=True)
    living_area: Mapped[Decimal] = mapped_column("living_area", sa.Numeric(4,2))
    kitchen_area: Mapped[Decimal] = mapped_column("kitchen_area", sa.Numeric(4,2))
    repair: Mapped[Optional[str]] = mapped_column("repair", sa.String(length=50), nullable=True)
    balcony: Mapped[Optional[str]] = mapped_column("balcony", sa.String(length=20), nullable=True)
    number_balcony: Mapped[Optional[str]] = mapped_column("number_balcony", sa.String(length=20), nullable=True)
    bath: Mapped[str] = mapped_column("bath", sa.String(length=20))


class Photos(Base):
    __tablename__ = "objects_photos"
    photo_id: Mapped[int] = mapped_column("photo_id_pk", sa.BigInteger, primary_key=True)
    object_id: Mapped[str] = mapped_column("object_id", sa.Uuid)
    url: Mapped[str] = mapped_column("url", sa.String(length=255))