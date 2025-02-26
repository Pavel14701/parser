# -*- coding: utf-8 -*-

from typing import Optional

from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.src.application import interfaces
from app.src.application import dto
from app.src.domain.entities import ObjectDm, SearchResultsDm


class ObjectsGateway(
    interfaces.SaveObject,
    interfaces.ReadObject,
    interfaces.FindObjects
):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, object: ObjectDm) -> None:
        query = text("""
            WITH inserted_object AS (
                INSERT INTO objects (
                    id, region, city, street, house_number, city_region, micro_region, latitude, longitude,
                    price_byn, price_usd, price_m2,
                    build_type, year_of_build, floor, floors_numb, rooms, separated_rooms, all_separated_rooms,
                    area, living_area, kitchen_area, repair, balcony, number_balcony, bath,
                    active, url, title, description
                ) VALUES (
                    :id, :region, :city, :street, :house_number, :city_region, :micro_region, :latitude, :longitude,
                    :price_byn, :price_usd, :price_m2,
                    :build_type, :year_of_build, :floor, :floors_numb, :rooms, :separated_rooms, :all_separated_rooms,
                    :area, :living_area, :kitchen_area, :repair, :balcony, :number_balcony, :bath,
                    :active, :url, :title, :description
                ) RETURNING id
            )
            INSERT INTO objects_photos (object_id, url)
            SELECT inserted_object.id, unnest(:pictures) FROM inserted_object;
        """)
        await self._session.execute(
            statement=query,
            params={
                "id": object.id,
                "region": object.region,
                "city": object.city,
                "street": object.street,
                "house_number": object.house_number,
                "city_region": object.city_region,
                "micro_region": object.micro_region,
                "latitude": object.latitude,
                "longitude": object.longitude,
                "price_byn": object.price_byn,
                "price_usd": object.price_usd,
                "price_m2": object.price_m2,
                "build_type": object.build_type,
                "year_of_build": object.year_of_build,
                "floor": object.floor,
                "floors_numb": object.floors_numb,
                "rooms": object.rooms,
                "separated_rooms": object.separated_rooms,
                "all_separated_rooms": object.all_separated_rooms,
                "area": object.area,
                "living_area": object.living_area,
                "kitchen_area": object.kitchen_area,
                "repair": object.repair,
                "balcony": object.balcony,
                "number_balcony": object.number_balcony,
                "bath": object.bath,
                "active": object.active,
                "url": object.url,
                "title": object.title,
                "description": object.description,
                "pictures": object.pictures
            }
        )

    async def read_by_id(self, id: int) -> Optional[ObjectDm]:
        query = text("""
            SELECT 
                object.*, 
                ARRAY_AGG(photos.url) AS photo_urls
            FROM objects object
            LEFT JOIN objects_photos photos ON object.id = photos.object_id
            WHERE object.id = :id
            GROUP BY object.id;
        """)
        result = await self._session.execute(
            statement=query,
            params={"id": id}
        )
        row = result.fetchone()
        return (
            ObjectDm(
                build_type=row.build_type,
                year_of_build=row.year_of_build,
                floor=row.floor,
                floors_numb=row.floors_numb,
                rooms=row.rooms,
                separated_rooms=row.separated_rooms,
                all_separated_rooms=row.all_separated_rooms,
                area=row.area,
                living_area=row.living_area,
                repair=row.repair,
                balcony=row.balcony,
                number_balcony=row.number_balcony,
                bath=row.bath,
                price_byn=row.price_byn,
                price_usd=row.price_usd,
                price_m2=row.price_m2,
                region=row.region,
                city=row.city,
                street=row.street,
                house_number=row.house_number,
                city_region=row.city_region,
                micro_region=row.micro_region,
                latitude=row.latitude,
                longitude=row.longitude,
                active=row.active,
                id=row.id,
                url=row.url,
                title=row.title,
                description=row.description,
                pictures=row.photo_urls
            ) if row else None
        )

    async def update_by_url(self, url: str, object: ObjectDm) -> None:
        query = text("""
            WITH updated_object AS (
                UPDATE objects
                SET
                    region = :region,
                    city = :city,
                    street = :street,
                    house_number = :house_number,
                    city_region = :city_region,
                    micro_region = :micro_region,
                    latitude = :latitude,
                    longitude = :longitude,
                    price_byn = :price_byn,
                    price_usd = :price_usd,
                    price_m2 = :price_m2,
                    build_type = :build_type,
                    year_of_build = :year_of_build,
                    floor = :floor,
                    floors_numb = :floors_numb,
                    rooms = :rooms,
                    separated_rooms = :separated_rooms,
                    all_separated_rooms = :all_separated_rooms,
                    area = :area,
                    living_area = :living_area,
                    kitchen_area = :kitchen_area,
                    repair = :repair,
                    balcony = :balcony,
                    number_balcony = :number_balcony,
                    bath = :bath,
                    active = :active,
                    title = :title,
                    description = :description
                WHERE url = :url
                RETURNING id
            )
            DELETE FROM objects_photos
            WHERE object_id = (SELECT id FROM updated_object);

            INSERT INTO objects_photos (object_id, url)
            SELECT (SELECT id FROM updated_object), unnest(:pictures);
        """)
        await self._session.execute(
            statement=query,
            params={
                "region": object.region,
                "city": object.city,
                "street": object.street,
                "house_number": object.house_number,
                "city_region": object.city_region,
                "micro_region": object.micro_region,
                "latitude": object.latitude,
                "longitude": object.longitude,
                "price_byn": object.price_byn,
                "price_usd": object.price_usd,
                "price_m2": object.price_m2,
                "build_type": object.build_type,
                "year_of_build": object.year_of_build,
                "floor": object.floor,
                "floors_numb": object.floors_numb,
                "rooms": object.rooms,
                "separated_rooms": object.separated_rooms,
                "all_separated_rooms": object.all_separated_rooms,
                "area": object.area,
                "living_area": object.living_area,
                "kitchen_area": object.kitchen_area,
                "repair": object.repair,
                "balcony": object.balcony,
                "number_balcony": object.number_balcony,
                "bath": object.bath,
                "active": object.active,
                "title": object.title,
                "description": object.description,
                "url": url,
                "pictures": object.pictures
            }
        )

    async def delete_by_url(self, url: str) -> None:
        query = text("""
            WITH deleted_object AS (
                DELETE FROM objects 
                WHERE url = :url
                RETURNING id
            )
            DELETE FROM objects_photos
            WHERE object_id = (SELECT id FROM deleted_object);
        """)
        await self._session.execute(statement=query, params={"url": url})

    async def search_objects(self, filters: dto.DbSearchFilters) -> list[SearchResultsDm]:
        query = text("""
            SELECT 
                id, title, price_usd, region, city, street, house_number,
                area, living_area, kitchen_area, floor, floors_numb
            FROM objects
            WHERE
                (:min_price_usd IS NULL OR price_usd >= :min_price_usd)
                AND (:max_price_usd IS NULL OR price_usd <= :max_price_usd)
                AND (:build_type IS NULL OR build_type = :build_type)
                AND (:year_of_build IS NULL OR year_of_build = :year_of_build)
                AND (:floor IS NULL OR floor = :floor)
                AND (:floors_numb IS NULL OR floors_numb = :floors_numb)
                AND (:rooms IS NULL OR rooms = :rooms)
                AND (:separated_rooms IS NULL OR separated_rooms = :separated_rooms)
                AND (:all_separated_rooms IS NULL OR all_separated_rooms = :all_separated_rooms)
                AND (:area IS NULL OR area = :area)
                AND (:living_area IS NULL OR living_area = :living_area)
                AND (:kitchen_area IS NULL OR kitchen_area = :kitchen_area)
                AND (:repair IS NULL OR repair = :repair)
                AND (:balcony IS NULL OR balcony = :balcony)
                AND (:number_balcony IS NULL OR number_balcony = :number_balcony)
                AND (:bath IS NULL OR bath = :bath)
                AND (:region IS NULL OR region = :region)
                AND (:city IS NULL OR city = :city)
                AND (:street IS NULL OR street = :street)
                AND (:house_number IS NULL OR house_number = :house_number)
                AND (:city_region IS NULL OR city_region = :city_region)
                AND (:micro_region IS NULL OR micro_region = :micro_region)
        """)

        params = {
            "min_price_usd": filters.min_price_usd,
            "max_price_usd": filters.max_price_usd,
            "build_type": filters.build_type,
            "year_of_build": filters.year_of_build,
            "floor": filters.floor,
            "floors_numb": filters.floors_numb,
            "rooms": filters.rooms,
            "separated_rooms": filters.separated_rooms,
            "all_separated_rooms": filters.all_separated_rooms,
            "area": filters.area,
            "living_area": filters.living_area,
            "kitchen_area": filters.kitchen_area,
            "repair": filters.repair,
            "balcony": filters.balcony,
            "number_balcony": filters.number_balcony,
            "bath": filters.bath,
            "region": filters.region,
            "city": filters.city,
            "street": filters.street,
            "house_number": filters.house_number,
            "city_region": filters.city_region,
            "micro_region": filters.micro_region
        }
        result = await self._session.execute(query, params)
        rows = result.fetchall()
        return [SearchResultsDm(
            id=row.id,
            title=row.title,
            price_usd=row.price_usd,
            region=row.region,
            city=row.city,
            street=row.street,
            house_number=row.house_number,
            area=row.area,
            living_area=row.living_area,
            kitchen_area=row.kitchen_area,
            floor=row.floor,
            floors_numb=row.floors_numb
        ) for row in rows]