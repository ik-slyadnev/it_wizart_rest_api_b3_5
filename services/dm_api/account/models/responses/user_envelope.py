from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class Rating(BaseModel):
    enabled: bool = Field(description="Rating participation flag")
    quality: int = Field(description="Quality rating")
    quantity: int = Field(description="Quantity rating")


class RegistrationStatus(BaseModel):
    """Модель статуса регистрации"""
    confirmed: Optional[bool] = None
    confirmed_at: Optional[datetime] = None
    sent: Optional[bool] = None
    sent_at: Optional[datetime] = None


class User(BaseModel):
    login: Optional[str] = Field(description="Login")
    roles: Optional[List[UserRole]] = Field(default=None, description="Roles")
    medium_picture_url: Optional[str] = Field(None, alias="mediumPictureUrl", description="Profile picture URL M-size")
    small_picture_url: Optional[str] = Field(None, alias="smallPictureUrl", description="Profile picture URL S-size")
    status: Optional[str] = Field(None, description="User defined status")
    rating: Rating
    online: Optional[datetime] = Field(None, description="Last seen online moment")
    name: Optional[str] = Field(None, description="User real name")
    location: Optional[str] = Field(None, description="User real location")
    registration: Optional[datetime] = Field(None, description="User registration moment")


class UserEnvelope(BaseModel):
    resource: User
    registration: Optional[RegistrationStatus] = Field(default=None)
    metadata: Optional[dict] = Field(default=None, description="Additional metadata")
