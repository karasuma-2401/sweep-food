from fastapi import APIRouter, FastAPI 

app = FastAPI() 

v1_router = APIRouter(
    prefix = '/api'
) 

@v1_router.get('/health') 
async def health_liveness(): 
    return "Hello. Build with Cloudian 💙 Cloud"

app.include_router(v1_router)