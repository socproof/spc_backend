# sim_post_cap_backend/app/schemas/world.py
from typing import Dict, Any
from pydantic import BaseModel, Field
from .core import BaseModelWithID # Import from the same package

class WorldBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, example="Zarechye")
    description: str = Field(..., max_length=500, example="A monotown focused on the 'Red Progress' factory.")
    # We'll use JSONB in PostgreSQL for flexible parameters, represented as Dict in Pydantic
    initial_indicators: Dict[str, Any] = Field(default_factory=dict, example={"happiness_level": 3, "economic_stability": 2})

class WorldCreate(WorldBase):
    pass # Inherits all fields from WorldBase

class WorldRead(BaseModelWithID, WorldBase): # Inherits ID from BaseModelWithID and fields from WorldBase
    # Any additional fields specific to reading a world can be added here later
    pass