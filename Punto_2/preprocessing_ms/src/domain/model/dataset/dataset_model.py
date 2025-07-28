from typing import Dict, List, Optional
from pydantic import BaseModel, HttpUrl


class RawDataset(BaseModel):
    file_path: str
