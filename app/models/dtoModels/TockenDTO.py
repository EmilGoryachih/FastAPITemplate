from app.models.dtoModels.Entity import Entity



class TokenDTO(Entity):
    access_token: str
    token_type: str
