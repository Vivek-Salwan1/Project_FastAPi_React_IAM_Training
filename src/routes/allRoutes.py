from fastapi import APIRouter

from src.routes.productRoutes import router as product_router
from src.routes.userRoutes import router as user_router

router = APIRouter()
router.include_router(product_router)
router.include_router(user_router)