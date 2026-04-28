from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Назва книги")
    author: str = Field(..., min_length=1, description="Автор книги")
    isbn: str = Field(..., description="ISBN код")
    pages: int = Field(..., gt=0, description="Кількість сторінок")
    year: int = Field(..., description="Рік видання")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "isbn": "0132350882",
                "pages": 464,
                "year": 2008
            }
        }


class BookResponse(BaseModel):
    id: str = Field(alias="_id", description="ID книги в MongoDB")
    title: str
    author: str
    isbn: str
    pages: int
    year: int

    class Config:
        populate_by_name = True


# Функції валідації
def validate_book_create(data):
    required_fields = ["title", "author", "isbn", "pages", "year"]

    for field in required_fields:
        if field not in data:
            return False, f"Поле '{field}' є обов'язковим"

    if not isinstance(data["title"], str) or len(data["title"]) == 0:
        return False, "Назва книги повинна бути непустою строкою"

    if not isinstance(data["author"], str) or len(data["author"]) == 0:
        return False, "Автор повинен бути непустою строкою"

    if not isinstance(data["pages"], int) or data["pages"] <= 0:
        return False, "Кількість сторінок повинна бути позитивним числом"

    if not isinstance(data["year"], int):
        return False, "Рік видання повинен бути числом"

    return True, None


def validate_book_update(data):
    if "pages" in data and (not isinstance(data["pages"], int) or data["pages"] <= 0):
        return False, "Кількість сторінок повинна бути позитивним числом"

    return True, None