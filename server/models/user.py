"""

model for routers.users.py
for Database MongoDB Query Data from frontend to save Database

"""

from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    ID: Optional[int] = None
    Year_Birth: Optional[int] = None
    Education: Optional[str] = None
    Marital_Status: Optional[str] = None
    Income: Optional[int] = None
    Age: Optional[int] = None
    Gen: Optional[str] = None
