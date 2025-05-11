# sim_post_cap_backend/app/models/problem.py
import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Table  # Added Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Association table for the many-to-many relationship between ProblemInstance and itself
# This table will link a problem instance to other problem instances that it influences or is influenced by.
problem_instance_links = Table(
    "problem_instance_links",
    Base.metadata,
    Column("source_problem_id", UUID(as_uuid=True), ForeignKey("problem_instances.id"), primary_key=True),
    Column("linked_problem_id", UUID(as_uuid=True), ForeignKey("problem_instances.id"), primary_key=True),
)


# 'source_problem_id' can be thought of as 'this problem instance'
# 'linked_problem_id' can be thought of as 'another problem instance related to this one'
# The nature of the link (e.g. "causes", "is aggravated by") would need to be defined by business logic
# or potentially another field in this association table if the link type is important.

class ProblemTemplate(Base):
    __tablename__ = "problem_templates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description_template = Column(Text, nullable=False)
    parameters_schema = Column(JSONB, nullable=False, default=dict)

    # Relationship to instances created from this template
    problem_instances = relationship("ProblemInstance", back_populates="problem_template")


class ProblemInstance(Base):
    __tablename__ = "problem_instances"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    current_parameters = Column(JSONB, nullable=False, default=dict)

    world_id = Column(UUID(as_uuid=True), ForeignKey("worlds.id"), nullable=False)
    problem_template_id = Column(UUID(as_uuid=True), ForeignKey("problem_templates.id"), nullable=False)

    world = relationship("World", back_populates="problem_instances")
    problem_template = relationship("ProblemTemplate", back_populates="problem_instances")

    # Relationship to solutions that target this specific problem instance
    solutions_targeting_this = relationship("AppliedSolution", back_populates="target_problem_instance",
                                            cascade="all, delete-orphan",
                                            foreign_keys="[AppliedSolution.target_problem_instance_id]")
    # --- Many-to-many relationship with itself ---
    # This defines relationships to other ProblemInstance records that this instance links to.
    # e.g. Problem A causes Problem B. This would be a link from A to B.
    linked_to = relationship(
        "ProblemInstance",  # The class name of the related model
        secondary=problem_instance_links,  # The association table
        primaryjoin=(problem_instance_links.c.source_problem_id == id),
        # Join from this table's id to association table
        secondaryjoin=(problem_instance_links.c.linked_problem_id == id),
        # Join from association table to other table's id
        backref="linked_from"  # Creates a 'linked_from' attribute on the "other" ProblemInstance
        # to see which problems link TO it.
    )
    # Removed: linked_problem_ids_store = Column(JSONB, name="linked_problem_ids", nullable=True, default=list)
