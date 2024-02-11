from pydantic import BaseModel
from typing import List, Any


class CreateFuncRequest(BaseModel):
    content: str


class ExecFuncRequest(BaseModel):
    params: List[Any]
    target: str  # a file that contains the function


class ModifyFuncRequest(BaseModel):
    content: str
    target: str


class DelFuncRequest(BaseModel):
    target: str


class LibInstallRequest(BaseModel):
    libs: List[str]
