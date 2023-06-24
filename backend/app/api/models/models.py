from pydantic import BaseModel
from typing import Dict, Union


class UploadModelResponse(BaseModel):
    path: str
    status: str


class PredictionPayload(BaseModel):
    feature: Dict[str, Union[float, int, str]]

    class Config:
        smart_union = True


class DataItem(BaseModel):
    data: Union[float, int, str]

    class Config:
        smart_union = True


class PredictionResponse(BaseModel):
    result: str
