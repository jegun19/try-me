from fastapi import UploadFile
from app.services.model_service import ModelService
from app.api.models.models import UploadModelResponse, PredictionPayload
from app.api.utils.data_utils import parse_json_to_dataframe, serialize_dataframe_to_json, numpy_list_to_json_list
from pydantic import parse_obj_as

model_service = ModelService()


async def upload_model_controller(file: UploadFile):
    filename = await model_service.upload_model(file=file)

    model_data = {
        "path": filename,
        "status": "OK"
    }

    return UploadModelResponse(**model_data)


async def predict(payload: PredictionPayload):
    # Extract features from the payload
    prediction_payload = parse_obj_as(PredictionPayload, payload)
    features = prediction_payload.feature
    input_df = parse_json_to_dataframe(features)

    # Load model instance
    model = model_service.get_model()
    prediction_result = model.predict(input_df)

    # Return inference result
    json_str = numpy_list_to_json_list(prediction_result)
    print(json_str)
    prediction_response = {
        "result": json_str
    }
    return prediction_response
