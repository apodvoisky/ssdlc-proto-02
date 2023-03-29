"""Инфраструктура протоколирования."""

from fastapi import HTTPException, Response, Request
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse
from fastapi.routing import APIRoute
from typing import Callable
import logging


def log_info(request: Request, req_body, res_body):
    log_data = f"{request.method} {request.url}"
    logging.info(log_data)
    logging.info(req_body)
    logging.info(res_body)


class SSDLCRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            result_exception: Exception = None

            req_body = await request.body()

            response = None
            error_info = 'ok'
            try:
                response = await original_route_handler(request)
            except HTTPException as httpex:
                error_info = f"{httpex}: {httpex.detail}"
                result_exception = httpex
            except Exception as e:
                error_info = str(e)
                result_exception = e

            if isinstance(response, StreamingResponse):
                res_body = b''
                async for item in response.body_iterator:
                    res_body += item

                task = BackgroundTask(log_info, req_body, res_body)
                return Response(content=res_body, status_code=response.status_code,
                                headers=dict(response.headers), media_type=response.media_type, background=task)
            else:
                if response is not None:
                    res_body = response.body

                    response.background = BackgroundTask(log_info, request, req_body, res_body)
                    return response
                else:
                    log_info(request, req_body, '')
                    logging.error(error_info)
                    raise result_exception

        return custom_route_handler
