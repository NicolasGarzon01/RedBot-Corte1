from pydantic import BaseModel
from typing import Any, Dict

# Este es el esquema base, con los campos comunes.
class TaskBase(BaseModel):
    type: str
    config_json: Dict[str, Any]

# Este es el esquema para CREAR una tarea. No necesita 'status'.
class TaskCreate(TaskBase):
    account_id: int

# Este es el esquema para MOSTRAR una tarea en la respuesta de la API.
# Aquí es donde se necesita el campo 'status'.
class Task(TaskBase):
    id: int
    account_id: int
    status: str  # <--- Este es el campo que faltaba

    class Config:
        from_attributes = True # <--- Esta es la versión actualizada de orm_mode