import json
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

    
class Client(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    ip: so.Mapped[str] = so.mapped_column(sa.String(39), index=True, unique=True)
    connection_count: so.Mapped[int] = so.mapped_column(sa.Integer(), default=1)

    def __init__(self, ip):
        self.ip = ip
        self.connection_count = 1

    def __repr__(self):
        return f"<Client: id={self.id}, ip='{self.ip}', connection_count={self.connection_count}>"

class Languages(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    language_name: so.Mapped[str] = so.mapped_column(sa.String(255), index=True, nullable=False)
    
    def __init__(self, language_name):
        self.language_name = language_name

    def __repr__(self):
        return f"<Languages: id={self.id}, language_name='{self.language_name}>"

class TextSection(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    text_section: so.Mapped[str] = so.mapped_column(sa.String(2000))
    text_hash: so.Mapped[int] = so.mapped_column(sa.Integer(), unique=True)
    language_id: so.Mapped[str] = so.mapped_column(sa.String(20))
    area_prominence: so.Mapped[str] = so.mapped_column(sa.String((2 + 10 + 100) * 10), index=True, nullable=True)

    def __init__(self, text_section, language_id=None, area_prominence=None):
        self.text_section = text_section
        self.language_id = language_id
        self.area_prominence = area_prominence
        self.text_hash = hash(text_section)

    def __repr__(self):
        return f"TextSection: id {self.id}, text_section '{self.text_section}', language_id '{self.language_id}', area_prominence '{self.area_prominence}'"
    
    def serializable(self):
        return {"id": self.id, "text_section": self.text_section}

class TypingSession(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    client_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Client.id), index=True, nullable=True)
    text_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(TextSection.id))
    completion_status: so.Mapped[bool] = so.mapped_column(sa.Integer(), default=0)
    completion_time: so.Mapped[int] = so.mapped_column(sa.Integer(), default=-1, nullable=True)

    def __init__(self, client_id, text_id):
        self.client_id = client_id
        self.text_id = text_id

    def __repr__(self):
        return f"<TypingSession: id={self.id}, client_id={self.client_id}, text_id='{self.text_id}', completion_time={self.completion_time}>"
    
class TypingSessionDeltas(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    typing_session_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(TypingSession.id), index=True, nullable=False)
    is_addition: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True)
    start: so.Mapped[int] = so.mapped_column(sa.Integer(), nullable=False)
    stop: so.Mapped[int] = so.mapped_column(sa.Integer(), nullable=False)
    characters: so.Mapped[str] = so.mapped_column(sa.String(2), nullable=False)
    timestamp: so.Mapped[int] = so.mapped_column(sa.Integer(), nullable=False)

    def __init__(self, typing_session_id: int, is_addition: bool, start: int, stop: int, timestamp: int):
        self.typing_session_id = typing_session_id
        self.is_addition = is_addition
        self.start = start
        self.stop = stop
        self.timestamp = timestamp
    
    def __repr__(self):
        return f"<TypingSessionDelta: {"+" if self.is_addition else "-"}{self.characters}, {self.start}-{self.stop}>"