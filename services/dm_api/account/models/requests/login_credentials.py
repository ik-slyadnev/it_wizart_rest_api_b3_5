from pydantic import BaseModel, Field


class LoginCredentials(BaseModel):
    login: str = Field(description="User login")
    password: str = Field(description="User password")
    remember_me: bool = Field(default=True, alias="rememberMe")
