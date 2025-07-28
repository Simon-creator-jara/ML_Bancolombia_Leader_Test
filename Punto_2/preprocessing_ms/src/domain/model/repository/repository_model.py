from typing import Dict, Optional
from pydantic import BaseModel


class GetJson(BaseModel):
    """Get Json S3"""
    s3_path: str


class SaveJson(BaseModel):
    """Save Json S3"""
    bucket: str
    key: str
    data: Optional[Dict]
