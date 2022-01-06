from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from db import db, generate_token
from fastapi import APIRouter, status, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class StudentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    course: str = Field(...)
    gpa: float = Field(..., le=4.0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }


class UpdateStudentModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    gpa: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }


@router.post("/", response_description="Add new student", response_model=StudentModel)
async def create_student(student: StudentModel):
    student = jsonable_encoder(student)
    ids = await db.insert_one(collection='students', data=student)
    content = await db.find_one(collection='students', query={'_id': ids})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)


@router.get("/{id}",
            response_description="Get a single student",
            response_model=StudentModel
            )
async def show_student(id: str):
    student = await db.find_one(collection='students', query={'_id': id})
    if student:
        return student
    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@router.put("/{id}", response_description="Update a student", response_model=StudentModel)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}
    if len(student) >= 1:
        update_result = await db["students"].update_one({"_id": id}, {"$set": student})
        if update_result.modified_count == 1:
            if (
                    updated_student := await db["students"].find_one({"_id": id})
            ) is not None:
                return updated_student
    if (existing_student := await db["students"].find_one({"_id": id})) is not None:
        return existing_student
    raise HTTPException(status_code=404, detail=f"Student {id} not found")
