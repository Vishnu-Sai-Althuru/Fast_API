# from fastapi import APIRouter

# router = APIRouter()


# @router.get("/test")
# def test_admin():
#     return {"msg": "Admin working"}


from fastapi import APIRouter, Depends
from app.core.security import require_admin

router = APIRouter()


@router.get("/dashboard")
def admin_dashboard(user=Depends(require_admin)):
    return {"msg": "Welcome Admin"}
