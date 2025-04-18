from pydantic import BaseModel


class ProductsSchemas(BaseModel):
    name: str
    descriptions: str
    price: int
    url_photo: str
    old_price: int
    categories_id: int | None


class CategoriesSchemas(BaseModel):
    name: str
