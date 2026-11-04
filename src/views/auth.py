from pydantic import BaseModel  # type: ignore


class LoginOut(BaseModel):
    access_token: str
