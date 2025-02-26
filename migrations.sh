#!/bin/bash
# -*- coding: utf-8 -*-

export $(grep -v '^#' .env | xargs)
alembic upgrade head