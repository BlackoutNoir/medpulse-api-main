from fastapi.security import HTTPBearer
from typing import Annotated

class AccessTokenBearer(HTTPBearer):
    pass


access_token_bearer = Annotated[dict, AccessTokenBearer()]