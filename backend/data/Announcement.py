from pydantic import BaseModel

class Announcement(BaseModel):
    title: str
    content: str
    aid: str | None = None
    is_active: bool | None = True