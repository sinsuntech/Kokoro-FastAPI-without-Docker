#! /bin/bash

PYTHONPATH=:/home/wxy/projects/Kokoro-FastAPI:/home/wxy/projects/Kokoro-FastAPI/api/src uvicorn api.src.main:app --port 50880 --host 0.0.0.0
