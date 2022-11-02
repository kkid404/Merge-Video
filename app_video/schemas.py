from pydantic import BaseModel
from typing import List


class Video(BaseModel):
    link: List


class PlayList(BaseModel):
    link: List
