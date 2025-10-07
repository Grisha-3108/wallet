from fastapi import FastAPI
import uvicorn

from api.api_router import api_main_router



app = FastAPI()
app.include_router(api_main_router)


if __name__ == '__main__':
    uvicorn.run('main:app', 
                reload=True, 
                host='localhost',
                port=8000)