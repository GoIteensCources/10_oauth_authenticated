import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes import route_user, route_auth

app = FastAPI()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


app.include_router(route_user, prefix="/users", tags=["users"])
app.include_router(route_auth, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)