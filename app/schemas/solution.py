# sim_post_cap_backend/app/schemas/solution.py
import uuid
from typing import Dict, Any
from pydantic import BaseModel, Field
from .core import BaseModelWithID

class SolutionBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="Attract External Investor")
    description: str = Field(..., max_length=500, example="Offer tax breaks and land to a new factory.")
    # JSONB for cost structure: e.g. {"budget": 100, "admin_resource": 50}
    base_cost: Dict[str, Any] = Field(default_factory=dict)
    # JSONB to define effects, probabilities, buffs/debuffs
    # Example: {"target_problem_parameter": "unemployment_rate", "effect_value": -0.1, "probability": 0.4}
    base_effects: Dict[str, Any] = Field(default_factory=dict)
    # JSONB for conditions to apply: e.g. {"world_indicator_X": {"operator": ">", "value": 5}}
    requirements: Dict[str, Any] = Field(default_factory=dict)

class SolutionCreate(SolutionBase):
    pass

class SolutionRead(BaseModelWithID, SolutionBase):
    pass

# Schema for when a solution is applied in a scenario (linking it to a world/problem)
class AppliedSolutionBase(BaseModel):
    world_id: uuid.UUID
    solution_template_id: uuid.UUID # Links to a SolutionRead (template)
    target_problem_instance_id: uuid.UUID # Which specific problem instance this solution addresses
    turn_applied: int = Field(..., gt=0, example=1) # Game turn when applied
    actual_outcome: Dict[str, Any] = Field(default_factory=dict) # To store results of "dice roll" and applied effects

class AppliedSolutionCreate(AppliedSolutionBase):
    # Outcome is usually determined by the simulation engine, not directly created by user
    pass

class AppliedSolutionRead(BaseModelWithID, AppliedSolutionBase):
    pass