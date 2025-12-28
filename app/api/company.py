from fastapi import APIRouter, Header, HTTPException
from app.storage.memory import get_company_by_api_key

router = APIRouter(prefix="/company", tags=["Company"])


@router.get("/me")
def get_my_company(x_api_key: str = Header(...)):
    """
    API key ilə şirkəti tanıyır
    """
    company = get_company_by_api_key(x_api_key)

    if not company:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return company