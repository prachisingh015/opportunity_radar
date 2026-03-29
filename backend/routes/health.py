from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    return {"status": "ok", "service": "Opportunity Radar API", "version": "1.0.0"}
