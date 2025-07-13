import pandas as pd
from pydantic import BaseModel, ValidationError, validator


class CSVMetadata(BaseModel):
    image_path: str
    weight: int
    height: int
    prompt: str
    seed: int

    @validator("image_path", "prompt")
    def non_empty_strings(cls, v):
        if not v.strip():
            raise ValueError("String field is empty")
        return v

    @validator("weight", "height")
    def positive_dims(cls, v):
        if v <= 0:
            raise ValueError("Dimension must be positive")
        return v


def validate_csv_metadata(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    results = []
    for i, row in df.iterrows():
        try:
            CSVMetadata(**row.to_dict())
            results.append({"row": i, "status": "valid", "error": ""})
        except ValidationError as e:
            results.append({"row": i, "status": "invalid", "error": str(e)})
    return pd.DataFrame(results)