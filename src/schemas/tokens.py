from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = {"from_attributes": True}  # Add this
    
class TokenData(BaseModel):
    username: str | None = None
        
    model_config = {"from_attributes": True}