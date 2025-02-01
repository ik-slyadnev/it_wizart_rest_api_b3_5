from pydantic import BaseModel, Field


class ChangeEmail(BaseModel):
    login: str = Field(description="User login")
    password: str = Field(description="User password")
    email: str = Field(description="New user email")
