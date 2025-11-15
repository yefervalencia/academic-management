from datetime import datetime, date
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
# ------------------------------------------------------------
# STUDENT BASE
# ------------------------------------------------------------
class StudentBase(BaseModel):
    name: str = Field(..., description="Student full name")
    email: EmailStr = Field(..., description="Student valid email")
    birthdate: Optional[date] = Field(None, description="Birthdate in YYYY-MM-DD format", examples=["2002-06-15"])
    degree: Optional[str] = Field(None, description="Degree or program the student is enrolled in")


# ------------------------------------------------------------
# STUDENT CREATE
# ------------------------------------------------------------
class StudentCreate(StudentBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john.doe@university.com",
                "birthdate": "2002-01-15",
                "degree": "Software Engineering"
            }
        }
    )


# ------------------------------------------------------------
# STUDENT READ
# ------------------------------------------------------------
class StudentRead(StudentBase):
    id: int = Field(..., description="Unique student identifier")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 5,
                "name": "John Doe",
                "email": "john.doe@university.com",
                "birthdate": "2002-01-15",
                "degree": "Software Engineering",
                "created_at": "2025-01-10T18:35:00",
                "updated_at": "2025-01-10T18:35:00"
            }
        }
    )
