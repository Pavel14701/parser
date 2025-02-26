# -*- coding: utf-8 -*-

from typing import Annotated, Optional
from uuid import UUID
from http import HTTPStatus
from decimal import Decimal

from dishka.integrations.base import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query, Response
from fastapi.exceptions import HTTPException
from fastapi.params import Body

from app.src.application.interactors import (
    GetObjectInteractor,
    FindObjectsInteractor,
    DataParserInteractor,
    SaveObjectInteractor,
    UpdateObjectInteractor,
    DeleteObjectInteractor
)
from app.src.controllers.schemas import ObjectSchema, SearchObjectSchema
from app.src.application.dto import DbSearchFilters


class Controllers:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/{object_id:uuid}", self.get_object, methods=["GET"])
        self.router.add_api_route("/search", self.search_objects, methods=["GET"])
        self.router.add_api_route("/", self.save_object, methods=["POST"])

    @inject
    async def get_object(
        self,
        object_id: Annotated[UUID, Body(description="Object ID", title="Object ID")],
        interactor: Depends[GetObjectInteractor],
    ) -> Response:
        object_dm = await interactor(uuid=str(object_id))
        if not object_dm:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Object not found")
        return Response(ObjectSchema.from_dataclass(object_dm), status_code=200)

    @inject
    async def save_object(
        self,
        url: Annotated[str, Query(None, description="Url of object", title="Url of object")],
        parser_interactor: Depends[DataParserInteractor],
        save_interactor: Depends[SaveObjectInteractor]
    ) -> Response:
        try:
            data = await parser_interactor(url)
            await save_interactor(data)
        except Exception as e:
            return Response(e, status_code=400)
        return Response("Success", status_code=200)

    @inject
    async def update_object(
        self,
        url: Annotated[str, Query(None, description="Url of object", title="Url of object")],
        parser_interactor: Depends[DataParserInteractor],
        update_interactor: Depends[UpdateObjectInteractor]
    ) -> Response:
        try:
            data = await parser_interactor(url)
            await update_interactor(data, url)
        except Exception as e:
            return Response(e, status_code=400)
        return Response("Success", status_code=200)

    @inject
    async def delete_object(
        self,
        url: Annotated[str, Query(None, description="Url of object", title="Url of object")],
        delete_interactor: Depends[DeleteObjectInteractor]
    ) -> Response:
        try:
            await delete_interactor(url)
        except Exception as e:
            return Response(e, status_code=400)
        return Response("Success", status=200)

    @inject
    async def search_objects(
        self,
        min_price_usd: Annotated[Optional[int], Query(None, description="Min object price", title="Min object price")],
        max_price_usd: Annotated[Optional[int], Query(None, description="Max object price", title="Max object price")],
        build_type: Annotated[Optional[str], Query(None, description="Build type", title="Build type")],
        year_of_build: Annotated[Optional[int], Query(None, description="Year of build", title="Year of build")],
        floor: Annotated[Optional[int], Query(None, description="Floor", title="Floor")],
        floors_numb: Annotated[Optional[int], Query(None, description="Number of floors", title="Number of floors")],
        rooms: Annotated[Optional[int], Query(None, description="Number of rooms", title="Number of rooms")],
        separated_rooms: Annotated[Optional[int], Query(None, description="Number of separated rooms", title="Number of separated rooms")],
        all_separated_rooms: Annotated[Optional[bool], Query(None, description="All rooms are separated", title="All rooms are separated")],
        area: Annotated[Optional[Decimal], Query(None, description="Total area", title="Total area")],
        living_area: Annotated[Optional[Decimal], Query(None, description="Living area", title="Living area")],
        kitchen_area: Annotated[Optional[Decimal], Query(None, description="Kitchen area", title="Kitchen area")],
        repair: Annotated[Optional[str], Query(None, description="Repair type", title="Repair type")],
        balcony: Annotated[Optional[str], Query(None, description="Balcony type", title="Balcony type")],
        number_balcony: Annotated[Optional[str], Query(None, description="Number of balconies", title="Number of balconies")],
        bath: Annotated[Optional[str], Query(None, description="Bath type", title="Bath type")],
        region: Annotated[Optional[str], Query(None, description="Region", title="Region")],
        city: Annotated[Optional[str], Query(None, description="City", title="City")],
        street: Annotated[Optional[str], Query(None, description="Street", title="Street")],
        house_number: Annotated[Optional[str], Query(None, description="House number", title="House number")],
        city_region: Annotated[Optional[str], Query(None, description="City region", title="City region")],
        micro_region: Annotated[Optional[str], Query(None, description="Micro region", title="Micro region")],
        search_interactor: Depends[FindObjectsInteractor]
    ) -> Response:
        filters = DbSearchFilters(
            min_price_usd=min_price_usd,
            max_price_usd=max_price_usd,
            build_type=build_type,
            year_of_build=year_of_build,
            floor=floor,
            floors_numb=floors_numb,
            rooms=rooms,
            separated_rooms=separated_rooms,
            all_separated_rooms=all_separated_rooms,
            area=area,
            living_area=living_area,
            kitchen_area=kitchen_area,
            repair=repair,
            balcony=balcony,
            number_balcony=number_balcony,
            bath=bath,
            region=region,
            city=city,
            street=street,
            house_number=house_number,
            city_region=city_region,
            micro_region=micro_region,
        )
        object_dms = await search_interactor(filters)
        if object_dms:
            result = [SearchObjectSchema.from_dataclass(object_dm) for object_dm in object_dms]
            return Response(result, status_code=200)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Objects not found")


