from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from strawberry.fastapi import GraphQLRouter


from core.graphql import schema
from api.api_router import api_main_router
from core.database import async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()


app = FastAPI()
graphql = GraphQLRouter(
    schema, allow_queries_via_get=False, graphql_ide="apollo-sandbox"
)

app.include_router(api_main_router)
app.include_router(graphql, prefix="/graphql", tags=["graphql api"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
