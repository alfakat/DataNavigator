import os
import json
import pandas as pd
from typing import Optional
from pydantic import BaseModel, ValidationError, validator

class JSONMetadata(BaseModel):
    image_height: int
    image_width: int
    timestamp: str
    camera_owner_name: Optional[str]
    camera_model: Optional[str]
    lens_type: Optional[str]

    @validator("image_height", "image_width")
    def positive_resolution(cls, v):
        if v <= 0:
            raise ValueError("Image resolution must be positive")
        return v

def validate_json_metadata(path: str) -> pd.DataFrame:
    with open(path, 'r') as f:
        data = json.load(f)
    try:
        JSONMetadata(**data)
        return pd.DataFrame([{"file": os.path.basename(path), "status": "valid", "error": ""}])
    except ValidationError as e:
        return pd.DataFrame([{"file": os.path.basename(path), "status": "invalid", "error": str(e)}])
