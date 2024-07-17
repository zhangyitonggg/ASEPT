from pydantic import BaseModel

class Announcement(BaseModel):
    title: str
    content: str