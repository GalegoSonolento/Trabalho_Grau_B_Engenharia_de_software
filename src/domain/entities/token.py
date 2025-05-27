from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4
from bson import ObjectId

class Token(BaseModel):
    id: Optional[str] = None
    user_id: str
    token: str = str(uuid4())
    created_at: datetime = datetime.utcnow()
    expires_at: datetime = datetime.utcnow() + timedelta(days=1)

    def to_dict(self):
        return {
            "_id": ObjectId(self.id) if self.id else None,
            "user_id": ObjectId(self.user_id),
            "token": self.token,
            "created_at": self.created_at,
            "expires_at": self.expires_at
        }

    @staticmethod
    def from_dict(data):
        return Token(
            id=str(data["_id"]) if data.get("_id") else None,
            user_id=str(data["user_id"]),
            token=data["token"],
            created_at=data["created_at"],
            expires_at=data["expires_at"]
        )