from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# ------------------------------------------------------------
# ENROLLMENT BASE
# ------------------------------------------------------------
class EnrollmentBase(BaseModel):
    course_id: int = Field(..., description="Course identifier")
    student_id: int = Field(..., description="Student identifier")
    inscription_date: Optional[datetime] = Field(
        None,
        description="Enrollment timestamp",
        examples=["2025-01-10T10:00:00"]
    )
    status: Optional[str] = Field("active", description="Enrollment status (e.g., active, dropped)")


# ------------------------------------------------------------
# ENROLLMENT CREATE
# ------------------------------------------------------------
class EnrollmentCreate(EnrollmentBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "course_id": 1,
                "student_id": 5,
                "inscription_date": "2025-01-10T10:00:00",
                "status": "active"
            }
        }
    )


# ------------------------------------------------------------
# ENROLLMENT READ
# ------------------------------------------------------------
class EnrollmentRead(EnrollmentBase):
    id: int = Field(..., description="Unique enrollment identifier")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 55,
                "course_id": 1,
                "student_id": 5,
                "inscription_date": "2025-01-10T10:00:00",
                "status": "active",
                "created_at": "2025-01-10T10:00:00",
                "updated_at": "2025-01-10T10:00:00"
            }
        }
    )