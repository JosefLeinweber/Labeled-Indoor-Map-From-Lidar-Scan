import fastapi

from src.api.routes.account_router import router as account_router
from src.api.routes.scan_processing_router import router as scan_processing_router

router = fastapi.APIRouter(
    prefix="/v1",
)

router.include_router(account_router)
router.include_router(scan_processing_router)
