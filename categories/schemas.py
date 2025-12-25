from pydantic import Field, EmailStr, field_validator, model_validator, BaseModel

class UserBase(BaseModel):
    title: str = Field(min_length=3, max_length=320)
    result = ''.join(char for char in title if not char.isdigit())
    print(result)
