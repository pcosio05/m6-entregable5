from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict
from typing import List

from app.domain.task import Task

class Tasks(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tasks: List[Task]