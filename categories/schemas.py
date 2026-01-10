from pydantic import Field, BaseModel

class CategoryBase(BaseModel):
    name: str = Field(min_length=3,max_length=256)
    description: str = Field(max_length=2048)


class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    pass

class CategoryDelete(CategoryBase):
    pass