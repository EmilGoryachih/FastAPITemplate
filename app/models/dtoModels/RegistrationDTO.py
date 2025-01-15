from app.models.dtoModels.Entity import Entity

class RegistrationDTO(Entity):
    name: str
    email: str
    password: str


