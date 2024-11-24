from fastapi import FastAPI
# from fastapi_pagination import add_pagination

from app.api import router



app = FastAPI(docs_url="/swagger")
# add_pagination(app)
app.include_router(router)
