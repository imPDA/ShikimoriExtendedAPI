from datetime import timedelta, datetime
from typing import Optional, Self, Any

from pydantic import BaseModel, model_validator, field_validator


class ShikimoriToken(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: timedelta
    expires_at: Optional[datetime] = None

    @model_validator(mode='after')
    def set_expires_at(self) -> Self:
        if not self.expires_at:
            self.expires_at = datetime.now() + self.expires_in
        return self

    @property
    def expired(self):
        return datetime.now() > self.expires_at

    @field_validator('access_token', mode='before')  # noqa
    @classmethod
    def validate_access_token(cls, v: Any) -> str:
        # I had it in previously, IDK why can it be list of tuple, probably server error?
        # Need to check if this problem is still an issue
        if not isinstance(v, str):
            raise ValueError(f'`access_token` is not `str` but {type(v)}: {v}!')

        return v if isinstance(v, str) else v[0]
