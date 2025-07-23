from pydantic import BaseModel, Field


class ProcessCategoryRequest(BaseModel):
    collection_name: str = Field(..., min_length=1, description="Название коллекции MongoDB")

class ProcessCategoryResponse(BaseModel):
    status: str
    message: str
    processed_count: int = 0