from datetime import datetime, timezone

from pydantic import BaseConfig, BaseModel


class RWModel(BaseModel):
    class Config(BaseConfig):
        validate_by_name = True
        json_encoders = {
            datetime:
            lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace(
                "+00:00", "Z")
        }
