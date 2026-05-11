#!/bin/bash
# Quick start script for development
cd "$(dirname "$0")"
source .venv/bin/activate
python manage.py runserver
