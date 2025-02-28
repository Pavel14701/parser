#!/bin/bash
# -*- coding: utf-8 -*-

export $(grep -v '^#' .env | xargs)
uvicorn --factory app.src.main:get_fastapi_app --reload