from pydantic import BaseModel, Field
from typing import List, Any


class CreateFuncRequest(BaseModel):
    content: str
    username: str = Field('admin')
    password: str = Field('admin')


class ExecFuncRequest(BaseModel):
    params: List[Any]
    target: str  # a file that contains the function
    username: str = Field('admin')
    password: str = Field('admin')


class ModifyFuncRequest(BaseModel):
    content: str
    target: str


class DelFuncRequest(BaseModel):
    target: str


class LibInstallRequest(BaseModel):
    libs: List[str]
