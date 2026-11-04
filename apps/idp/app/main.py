import logging

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from starlette.middleware.base import RequestResponseEndpoint

app = FastAPI(title="OIDC")
logger = logging.getLogger("uvicorn.error")


@app.middleware("http")
async def log_request(request: Request, call_next: RequestResponseEndpoint) -> Response:
    response = await call_next(request)
    # Route patterns avoid logging URLs that may later contain tokens or codes.
    route = request.scope.get("route")
    logger.info(
        "%s %s -> %s",
        request.method,
        getattr(route, "path", "(unmatched)"),
        response.status_code,
    )
    return response


@app.get("/", response_class=HTMLResponse)
async def home() -> str:
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>OIDC</title>
  </head>
  <body>
    <main>
      <h1>Our identity server is running.</h1>
      <p>Your browser requested this page. FastAPI sent this HTML back.</p>
      <p><a href="/health/live">Check that the server is alive</a></p>
    </main>
  </body>
</html>"""


@app.get("/health/live")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}
