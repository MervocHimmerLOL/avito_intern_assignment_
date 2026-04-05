from pydantic import BaseModel, Field


# Валидация JSON - моделей
class Statistics(BaseModel):
    likes: int = Field(ge=1)
    viewCount: int = Field(ge=1)
    contacts: int = Field(ge=1)


class ItemResponse(BaseModel):
    id: str
    sellerId: int
    name: str
    price: int
    statistics: Statistics
    createdAt: str


class CreateItemRequest(BaseModel):
    sellerID: int
    name: str = Field(min_length=1)
    price: int = Field(ge=1)
    statistics: Statistics


class ErrorResponse(BaseModel):
    result: dict
    status: str

    @property
    def message(self) -> str:
        return self.result.get('message')
