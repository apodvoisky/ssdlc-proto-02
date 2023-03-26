from sqlalchemy.exc import IntegrityError


class EntityNotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(EntityNotFoundError):
    entity_name: str = "User"


class UserEmailAlreadyExists(Exception):
    ...


class CustomerFullNameAlreadyExists(Exception):
    ...


class CustomerShortNameAlreadyExists(Exception):
    ...


class ProductTitleAlreadyExists(Exception):
    ...


class ProductCodeAlreadyExists(Exception):
    ...

class ProductNotFoundError(EntityNotFoundError):
    entity_name: str = "Product"


class CustomerNotFoundError(EntityNotFoundError):
    entity_name: str = "Customer"
