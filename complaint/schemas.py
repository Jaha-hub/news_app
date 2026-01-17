from pydantic import BaseModel, Field



class ComplaintBase(BaseModel):
    body: str = Field(min_length=5, max_length=1024)

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintRead(ComplaintBase):
    id: int
    article_id: int