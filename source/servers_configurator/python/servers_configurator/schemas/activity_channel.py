from pydantic import BaseModel


class ActivityChannel(BaseModel):
    activity_channel_id: int
    name: str
    server_id: int
    activity_type: str
