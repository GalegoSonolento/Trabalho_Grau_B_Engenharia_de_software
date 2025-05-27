from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    password: str  # Hashed password
    created_at: datetime = datetime.utcnow()
    deleted_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "_id": ObjectId(self.id) if self.id else None,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "deleted_at": self.deleted_at
        }

    @staticmethod
    def from_dict(data):
        return User(
            id=str(data["_id"]) if data.get("_id") else None,
            username=data["username"],
            email=data["email"],
            password=data["password"],
            created_at=data["created_at"],
            deleted_at=data.get("deleted_at")
        )