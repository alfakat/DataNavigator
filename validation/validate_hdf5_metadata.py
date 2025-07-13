import h5py
import pandas as pd
from pydantic import BaseModel, ValidationError, validator

class HDF5Metadata(BaseModel):
    path: str
    format: str
    mode: str
    width: int
    height: int

    @validator("path", "format", "mode")
    def non_empty(cls, v):
        if not v.strip():
            raise ValueError("Field must not be empty")
        return v

    @validator("width", "height")
    def positive_dims(cls, v):
        if v <= 0:
            raise ValueError("Width/height must be positive")
        return v

def validate_hdf5_metadata(path: str) -> pd.DataFrame:
    results = []
    with h5py.File(path, "r") as f:
        attrs = f["metadata"].attrs
        for key in attrs:
            if "/" not in key:
                continue
            idx, field = key.split("/")
            record = {"row": idx}
            entry = {k.split("/")[1]: v for k, v in attrs.items() if k.startswith(f"{idx}/")}
            try:
                HDF5Metadata(**entry)
                record.update({"status": "valid", "error": ""})
            except ValidationError as e:
                record.update({"status": "invalid", "error": str(e)})
            results.append(record)
    return pd.DataFrame(results)
