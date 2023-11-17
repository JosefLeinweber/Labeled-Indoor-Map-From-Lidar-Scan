import fastapi

from src.api.routes.floorplan_router import router as floorplan_router
from src.api.routes.frame_router import router as frame_router
from src.api.routes.intersection_point_router import router as intersection_point_router
from src.api.routes.scan_router import router as scan_router

router = fastapi.APIRouter(
    prefix="/v1",
)

router.include_router(scan_router)
router.include_router(frame_router)
router.include_router(floorplan_router)
router.include_router(intersection_point_router)
