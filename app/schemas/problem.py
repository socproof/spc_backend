# sim_post_cap_backend/app/schemas/problem.py
import uuid
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from .core import BaseModelWithID

class ProblemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="Mass Unemployment")
    description_template: str = Field(..., max_length=500, example="The 'Red Progress' factory has laid off X% of its workforce.")
    # JSONB for parameters template or rules for how they are calculated/affected
    parameters_schema: Dict[str, Any] = Field(default_factory=dict, example={"unemployment_rate": "float", "affected_workers": "int"})

class ProblemCreate(ProblemBase):
    pass

class ProblemRead(BaseModelWithID, ProblemBase):
    pass

# This schema will represent a problem instance within a specific world
class ProblemInstanceBase(BaseModel):
    world_id: uuid.UUID
    problem_template_id: uuid.UUID # Links to a ProblemRead (template)
    current_parameters: Dict[str, Any] = Field(default_factory=dict, example={"unemployment_rate": 0.4, "affected_workers": 5000})
    # The many-to-many relationship will be handled by specific API endpoints or populated differently if needed.

class ProblemInstanceCreate(ProblemInstanceBase):
    pass

class ProblemInstanceRead(BaseModelWithID, ProblemInstanceBase):
    pass