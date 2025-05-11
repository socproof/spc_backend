# sim_post_cap_backend/app/models/world.py
import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class World(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=False)
    initial_indicators = Column(JSONB, nullable=False, default=dict)

    problem_instances = relationship("ProblemInstance", back_populates="world", cascade="all, delete-orphan")
    applied_solutions_in_world = relationship("AppliedSolution", back_populates="world", cascade="all, delete-orphan", foreign_keys="[AppliedSolution.world_id]")
    # Added foreign_keys to applied_solutions_in_world to resolve potential ambiguity if more FKs to World existed in AppliedSolution