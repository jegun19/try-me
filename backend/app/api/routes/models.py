from fastapi import APIRouter, UploadFile
from app.api.models.models import UploadModelResponse, PredictionPayload
from app.api.controllers.models import upload_model_controller, predict

router = APIRouter()


@router.post("/upload-model", response_model=UploadModelResponse)
async def upload_model(file: UploadFile):

    upload_model_response = await upload_model_controller(file=file)

    return upload_model_response


@router.post("/predict")
async def get_prediction_result(payload: PredictionPayload):
    predict_response = await predict(payload=payload)
    return predict_response
