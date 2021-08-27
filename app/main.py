import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from routers import notica, usuario, auth

app = FastAPI()
app.include_router(notica.router)
app.include_router(usuario.router)
app.include_router(auth.router)


origins = [
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event('startup')
# async def startup():
#     await database.connect()
#
#
# @app.on_event('shutdown')
# async def shutdown():
#     await database.disconnect()


@app.get("/")
async def root():
    return RedirectResponse(url='/docs')


if __name__ == "__main__":
    uvicorn.run(app, log_level="info")
