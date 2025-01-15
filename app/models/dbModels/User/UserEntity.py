from app.models.dbModels.EntityDB import EntityDB
from sqlalchemy import Column, String, UUID

class UserEntity(EntityDB):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    hashed_password = Column(String(200), nullable=False)

    def __init__(self, id=None, username=None, email=None, hashed_password=None):
        self.id = id
        self.name = username
        self.email = email
        self.hashed_password = hashed_password


    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password
        }

