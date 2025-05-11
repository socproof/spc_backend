# sim_post_cap_backend/app/schemas/core.py
import uuid
from pydantic import BaseModel, Field

class BaseModelWithID(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")

    class Config:
        allow_population_by_field_name = True # Allows using alias `_id` for population
        orm_mode = True # To support ORM models if needed later for responses