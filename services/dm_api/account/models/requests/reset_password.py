from pydantic import BaseModel, Field


class ResetPassword(BaseModel):
    login: str = Field(description="Login")
    email: str = Field(description="Email")
