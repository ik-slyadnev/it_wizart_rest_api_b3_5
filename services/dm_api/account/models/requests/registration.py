from pydantic import BaseModel, Field


class Registration(BaseModel):
    login: str = Field(description="Login")
    email: str = Field(description="Email")
    password: str = Field(description="Password")
