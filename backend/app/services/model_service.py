import os
from fastapi import UploadFile
import xgboost as xgb


class ModelService:
    def __init__(self) -> None:
        self.UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
        self.FILE_NAME = ""
        self.model = None
        pass

    async def upload_model(self, file: UploadFile):
        if not os.path.exists(self.UPLOAD_DIR):
            self.create_upload_folder()
        file_path = os.path.join(self.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        self.FILE_NAME = file.filename

        return file.filename

    def load_model(self):
        self.model = xgb.XGBRegressor()

        self.model.load_model(os.path.join(self.UPLOAD_DIR, self.FILE_NAME))

    def get_model(self):
        if self.model is None:
            self.load_model()
        return self.model

    def create_upload_folder(self):
        os.makedirs(self.UPLOAD_DIR)
