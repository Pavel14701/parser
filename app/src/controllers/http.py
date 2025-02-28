# -*- coding: utf-8 -*-

import traceback
from typing import Annotated, Optional, Any
from uuid import UUID
from http import HTTPStatus
from decimal import Decimal

from dishka.integrations.base import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, FastAPI, Query, Path, Response
from fastapi.exceptions import HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse

from app.src.application.interactors import (
    GetObjectInteractor,
    FindObjectsInteractor,
    DataParserInteractor,
    SaveObjectInteractor,
    UpdateObjectInteractor,
    DeleteObjectInteractor
)
from app.src.application import dto
from app.src.config import AppConfig
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
        self.router.add_api_route("/swagger", self.custom_swagger_ui_html, include_in_schema=False, methods=["GET"])

    @inject
    async def get_object(
        self,
        object_id: Annotated[UUID, Path(description="Object ID", title="Object ID")],
        interactor: Depends[GetObjectInteractor],
    ) -> JSONResponse:
        try:
            object_dm = await interactor(uuid=str(object_id))
            if not object_dm:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Object not found")
            return JSONResponse(ObjectSchema.from_dataclass(object_dm), status_code=200)
        except Exception as e:
            error_message = f"Exception occurred: {str(e)}"
            traceback_message = "".join(traceback.format_exception(None, e, e.__traceback__))
            full_error_message = f"{error_message}\n\nTraceback:\n{traceback_message}"
            return JSONResponse(full_error_message, status_code=400)

    @inject
    async def save_object(
        self,
        url: Annotated[str, Query(description="Url of object", title="Url of object")],
        parser_interactor: Depends[DataParserInteractor],
        save_interactor: Depends[SaveObjectInteractor]
    ) -> JSONResponse:
        try:
            request_params = dto.RequestParam(url=url, headers=None)
            data = await parser_interactor(request_params, None, None)
            await save_interactor(data)
        except Exception as e:
            error_message = f"Exception occurred: {str(e)}"
            #traceback_message = "".join(traceback.format_exception(None, e, e.__traceback__))
            #full_error_message = f"{error_message}\n\nTraceback:\n{traceback_message}"
            return JSONResponse(error_message, status_code=400)
        return JSONResponse("Success", status_code=200)

    @inject
    async def update_object(
        self,
        url: Annotated[str, Query(description="Url of object", title="Url of object")],
        parser_interactor: Depends[DataParserInteractor],
        update_interactor: Depends[UpdateObjectInteractor]
    ) -> JSONResponse:
        try:
            data = await parser_interactor(url)
            await update_interactor(data, url)
        except Exception as e:
            error_message = f"Exception occurred: {str(e)}"
            traceback_message = "".join(traceback.format_exception(None, e, e.__traceback__))
            full_error_message = f"{error_message}\n\nTraceback:\n{traceback_message}"
            return JSONResponse(full_error_message, status_code=400)
        return JSONResponse("Success", status_code=200)

    @inject
    async def delete_object(
        self,
        url: Annotated[str, Query(None, description="Url of object", title="Url of object")],
        delete_interactor: Depends[DeleteObjectInteractor]
    ) -> JSONResponse:
        try:
            await delete_interactor(url)
        except Exception as e:
            error_message = f"Exception occurred: {str(e)}"
            traceback_message = "".join(traceback.format_exception(None, e, e.__traceback__))
            full_error_message = f"{error_message}\n\nTraceback:\n{traceback_message}"
            return JSONResponse(full_error_message, status_code=400)
        return JSONResponse("Success", status=200)

    @inject
    async def search_objects(
        self,
        search_interactor: Depends[FindObjectsInteractor],
        min_price_usd: Annotated[Optional[int], Query(description="Min object price", title="Min object price")] = None,
        max_price_usd: Annotated[Optional[int], Query(description="Max object price", title="Max object price")] = None,
        build_type: Annotated[Optional[str], Query(description="Build type", title="Build type")] = None,
        year_of_build: Annotated[Optional[int], Query(description="Year of build", title="Year of build")] = None,
        floor: Annotated[Optional[int], Query(description="Floor", title="Floor")] = None,
        floors_numb: Annotated[Optional[int], Query(description="Number of floors", title="Number of floors")] = None,
        rooms: Annotated[Optional[int], Query(description="Number of rooms", title="Number of rooms")] = None,
        separated_rooms: Annotated[Optional[int], Query(description="Number of separated rooms", title="Number of separated rooms")] = None,
        all_separated_rooms: Annotated[Optional[bool], Query(description="All rooms are separated", title="All rooms are separated")] = None,
        area: Annotated[Optional[Decimal], Query(description="Total area", title="Total area")] = None,
        living_area: Annotated[Optional[Decimal], Query(description="Living area", title="Living area")] = None,
        kitchen_area: Annotated[Optional[Decimal], Query(description="Kitchen area", title="Kitchen area")] = None,
        repair: Annotated[Optional[str], Query(description="Repair type", title="Repair type")] = None,
        balcony: Annotated[Optional[str], Query(description="Balcony type", title="Balcony type")] = None,
        number_balcony: Annotated[Optional[str], Query(description="Number of balconies", title="Number of balconies")] = None,
        bath: Annotated[Optional[str], Query(description="Bath type", title="Bath type")] = None,
        region: Annotated[Optional[str], Query(description="Region", title="Region")] = None,
        city: Annotated[Optional[str], Query(description="City", title="City")] = None,
        street: Annotated[Optional[str], Query(description="Street", title="Street")] = None,
        house_number: Annotated[Optional[str], Query(description="House number", title="House number")] = None,
        city_region: Annotated[Optional[str], Query(description="City region", title="City region")] = None,
        micro_region: Annotated[Optional[str], Query(description="Micro region", title="Micro region")] = None
    ) -> JSONResponse:
        try:
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
                return JSONResponse(result, status_code=200)
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Objects not found")
        except Exception as e:
            error_message = f"Exception occurred: {str(e)}"
            traceback_message = "".join(traceback.format_exception(None, e, e.__traceback__))
            full_error_message = f"{error_message}\n\nTraceback:\n{traceback_message}"
            return JSONResponse(full_error_message, status_code=400)

    @inject
    async def custom_swagger_ui_html(self, config: Depends[AppConfig]) -> HTMLResponse:
        return get_swagger_ui_html(
            swagger_js_url="http://127.0.0.1:8000/static/swagger-ui-bundle.js",
            swagger_css_url="http://127.0.0.1:8000/static/swagger-ui.css",
            openapi_url=config.openapi_url, title=f"{config.title} - Swagger UI"
        )