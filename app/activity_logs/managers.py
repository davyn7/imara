# app/activity_logs/managers.py

from app.activity_logs.schemas import ActivityLogBase
from app.activity_logs.db import (
    get_activity_logs_db,
    get_activity_log_db,
    add_activity_log_db,
)

class ActivityLogManager:
    def __init__(self, activity_log: ActivityLogBase):
        self.activity_log = activity_log

    async def get_activity_logs(self):
        return await get_activity_logs_db()

    async def get_activity_log(self, activity_log_id: int):
        return await get_activity_log_db(activity_log_id)

    async def add_activity_log(self):
        return await add_activity_log_db(self.activity_log)
