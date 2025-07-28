"""Module with useful functions for the project"""
import os
import json
from functools import lru_cache
from typing import Union, Dict, Any
from pathlib import Path
from fastapi import Request, HTTPException, Depends
import jwt
import os


@lru_cache()
def load_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Function to load a JSON file.

    :param file_path: String with the path of the file
    :return: Dictionary with the contents of the JSON file
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8-sig") as file:
            return json.load(file)
    raise FileNotFoundError(f"File {file_path} not found")


def verify_jwt(request: Request):
    from src.applications.settings.container import get_deps_container
    container = get_deps_container()
    JWT_SECRET = container.jwt
    secret = JWT_SECRET
    ALGORITHM = "HS256"
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")