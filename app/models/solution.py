# sim_post_cap_backend/app/models/solution.py
import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class SolutionTemplate(Base):  # Changed name
    __tablename__ = "solution_templates"  # Explicit table name
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)  # Template name should be unique
    description = Column(Text, nullable=False)
    base_cost = Column(JSONB, nullable=False, default=dict)
    base_effects = Column(JSONB, nullable=False, default=dict)
    requirements = Column(JSONB, nullable=False, default=dict)

    applied_instances = relationship("AppliedSolution", back_populates="solution_template")


class AppliedSolution(Base):
    __tablename__ = "applied_solutions"  # Explicit table name
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    turn_applied = Column(Integer, nullable=False)
    actual_outcome = Column(JSONB, nullable=False, default=dict)

    world_id = Column(UUID(as_uuid=True), ForeignKey("worlds.id"), nullable=False)
    solution_template_id = Column(UUID(as_uuid=True), ForeignKey("solution_templates.id"), nullable=False)
    target_problem_instance_id = Column(UUID(as_uuid=True), ForeignKey("problem_instances.id"), nullable=False)

    world = relationship("World", back_populates="applied_solutions_in_world", foreign_keys=[world_id])
    solution_template = relationship("SolutionTemplate", back_populates="applied_instances")
    target_problem_instance = relationship("ProblemInstance", back_populates="solutions_targeting_this")
