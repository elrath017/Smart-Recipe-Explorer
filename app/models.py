import uuid
import json
from sqlalchemy import Column, String, Boolean, Integer, Text, TypeDecorator
from app.database import Base

class JSONEncodedList(TypeDecorator):
    """Custom SQLAlchemy type to store sets/lists as JSON strings."""
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return '[]'

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return []

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    cuisine = Column(String, index=True)
    is_vegetarian = Column(Boolean, default=False)
    prep_time_minutes = Column(Integer)
    ingredients = Column(JSONEncodedList)
    difficulty = Column(String)
    instructions = Column(Text)
    tags = Column(JSONEncodedList)
