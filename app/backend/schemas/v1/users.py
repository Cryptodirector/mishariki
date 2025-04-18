from pydantic import BaseModel


class UsersSchemas(BaseModel):
    ip: str


class ProdUserSchemas(BaseModel):
    id_products: int
    id_users: int


class UserFormSchemas(BaseModel):
    occasion: str
    date: str
    price: int | str
    number: str

