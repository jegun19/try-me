import json
import pandas as pd
from pandas import json_normalize


def parse_json_to_dataframe(json_data):
    df = json_normalize(json_data)
    return df


def serialize_dataframe_to_json(data):
    df = pd.DataFrame(data, columns=["data"])
    json_data = df.to_json(orient="records")
    return json_data


def numpy_list_to_json_list(numpy_list):
    json_list = []
    for element in numpy_list:
        # Assuming the NumPy list contains scalar values
        json_obj = {"data": element.item()}
        json_list.append(json_obj)
    return json.dumps(json_list)
