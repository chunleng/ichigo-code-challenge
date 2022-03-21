from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic.main import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])


class Foo(BaseModel):
    name: str


@app.get(
    "/GetFoo",
    operation_id="GetFoo",
    response_class=JSONResponse,
    response_model=Foo,
    tags=[""],
)
async def get_foo():
    return {"name": "A"}
