from pydantic import BaseModel, Field, ConfigDict


class ChangePassword(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    old_password: str = Field(alias='oldPassword')
    new_password: str = Field(alias='newPassword')
    reset_token: str | None = Field(default=None, alias='resetToken')
