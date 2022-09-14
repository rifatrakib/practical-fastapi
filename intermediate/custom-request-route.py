import time
import gzip
from typing import Callable, List
from fastapi import FastAPI, Request, Response, HTTPException, Body
from fastapi.routing import APIRoute
from fastapi.exceptions import RequestValidationError


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress()
            self._body = body
        return self._body


class CustomRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        
        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            try:
                before = time.time()
                response: Response = await original_route_handler(request)
                duration = time.time() - before
                response.headers["X-Response-Time"] = str(duration)
                return response
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)
        
        return custom_route_handler


app = FastAPI()
app.router.route_class = CustomRoute


@app.post("/sum/")
async def sum_numbers(numbers: List[int] = Body()):
    return {"sum": sum(numbers)}
