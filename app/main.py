import uvicorn

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from collections.connection.database____ import return_databases
from collections.noticia import Noticia
from routers import notica

app = FastAPI()
app.include_router(notica.router)

database = return_databases()

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


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    Noticia()
    return RedirectResponse(url='/docs')


if __name__ == "__main__":
    uvicorn.run(app, log_level="info")
