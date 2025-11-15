from datetime import datetime, date
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional

# ------------------------------------------------------------
# PROFESSOR BASE
# ------------------------------------------------------------
class ProfessorBase(BaseModel):
    name: str = Field(..., description="Full name of the professor")
    email: EmailStr = Field(..., description="Valid email address")
    title: Optional[str] = Field(None, description="Professional or academic title", examples=["PhD in AI"])
    contratation_date: Optional[date] = Field(
        None,
        description="Hiring date of the professor in YYYY-MM-DD format",
        examples=["2024-03-10"]
    )


# ------------------------------------------------------------
# PROFESSOR CREATE
# ------------------------------------------------------------
class ProfessorCreate(ProfessorBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Dr. Alice Smith",
                "email": "alice.smith@university.com",
                "title": "PhD in Computer Science",
                "contratation_date": "2023-04-15"
            }
        }
    )


# ------------------------------------------------------------
# PROFESSOR READ
# ------------------------------------------------------------
class ProfessorRead(ProfessorBase):
    id: int = Field(..., description="Unique professor identifier")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Dr. Alice Smith",
                "email": "alice.smith@university.com",
                "title": "PhD in Computer Science",
                "contratation_date": "2023-04-15",
                "created_at": "2025-01-10T12:30:00",
                "updated_at": "2025-01-10T12:30:00"
            }
        }
    )
