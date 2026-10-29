"""POE Backend — Base schemas."""

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseSchema):
    status: str = "ok"
    service: str = "poe-str-backend"