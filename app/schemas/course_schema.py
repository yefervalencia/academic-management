from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# ------------------------------------------------------------
# COURSE BASE
# ------------------------------------------------------------
class CourseBase(BaseModel):
    code: str = Field(..., description="Internal course code, must be unique", examples=["CS101"])
    name: str = Field(..., description="Course name")
    description: Optional[str] = Field(None, description="Brief course description")
    professor_id: Optional[int] = Field(None, description="Identifier of the professor teaching the course")
    maximum_capacity: Optional[int] = Field(None, description="Maximum number of students allowed in the course")


# ------------------------------------------------------------
# COURSE CREATE
# ------------------------------------------------------------
class CourseCreate(CourseBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "CS101",
                "name": "Introduction to Programming",
                "description": "Fundamental programming concepts",
                "professor_id": 1,
                "maximum_capacity": 30
            }
        }
    )


# ------------------------------------------------------------
# COURSE READ
# ------------------------------------------------------------
class CourseRead(CourseBase):
    id: int = Field(..., description="Unique course identifier")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 10,
                "code": "CS101",
                "name": "Introduction to Programming",
                "description": "Fundamental programming concepts",
                "professor_id": 1,
                "maximum_capacity": 30,
                "created_at": "2025-03-01T14:20:00",
                "updated_at": "2025-03-01T14:20:00"
            }
        }
    )
