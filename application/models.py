from pydantic import BaseModel


class Campaign(BaseModel):
    id: str
    status: str
    quest: str
    chat: list
    users: dict


class User(BaseModel):
    id: str
    username: str
    current_campaign: str


class Chat(BaseModel):
    campaign_id: str
    user_id: str
    text: str
