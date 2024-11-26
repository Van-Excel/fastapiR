from datetime import datetime
from pydantic import BaseModel


class PostsResponse(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: datetime
    

class PostsRequest(BaseModel):
    title: str
    content: str
    published: bool = True
    