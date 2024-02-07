from pydantic import BaseModel

class CreateFuncRequest(BaseModel):
    content: str

class ExecFuncRequest(BaseModel):
    params: list
    target: str # a file that contains the function
    
class ModifyFuncRequest(BaseModel):
    content: str
    target: str
    
class DelFuncRequest(BaseModel):
    target: str