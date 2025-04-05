import io
import json

from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from pydantic import parse_obj_as
from starlette.requests import Request


router = APIRouter(prefix='/chat-items')
