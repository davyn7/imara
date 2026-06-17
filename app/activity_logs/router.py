# app/activity_logs/router.py

from fastapi import APIRouter
from app.activity_logs.managers import ActivityLogManager

router = APIRouter(prefix="/activity_logs", tags=["Activity Logs"])

@router.get("/activity_logs")
async def get_activity_logs():
    try:
        manager = ActivityLogManager(None)
        return await manager.get_activity_logs()
    except Exception as e:
        raise e

@router.get("/activity_logs/{activity_log_id}")
async def get_activity_log(activity_log_id: int):
    try:
        manager = ActivityLogManager(None)
        return await manager.get_activity_log(activity_log_id)
    except Exception as e:
        raise e
