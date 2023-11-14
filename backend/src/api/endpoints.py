import fastapi

from src.api.routes.account_router import router as account_router

router = fastapi.APIRouter(
    prefix="/v1",
)

router.include_router(account_router)
