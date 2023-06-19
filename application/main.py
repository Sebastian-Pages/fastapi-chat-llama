from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from .llm import LlamaModel_llama_cpp
from .models import Campaign, Chat, User
from .utils import VerifyToken, create_error_response
from .chat import compute_chat_response

app = FastAPI()
token_auth_scheme = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Database
campaigns = {
    "default_campaign": {
        "status": "open",
        "quest": "Magical Forest",
        "chat": [],
        "users": [],
    },
}
# TODO
users = {
    "183938193": {"username": "Paul", "current_campaign": "Jhon's Campaign"},
    "171939913": {"username": "Ben", "current_campaign": "Jack's Campaign"},
}
input_str = """You are a creative Game Master in DND. Give just one very short sentence presenting a situation for the player to solve.\n
    GM:"""

model_llm = LlamaModel_llama_cpp(model_path="models/ggml-vic7b-uncensored-q5_1.bin")

###########################  GET ###############################


@app.get("/api/public/user/{user_id}", response_model=User)
async def get_user(user_id: str):
    user_data = users.get(user_id)
    if user_data:
        return User(id=user_id, **user_data)
    else:
        return create_error_response(404, "User not found")


@app.get("/api/public/users", response_model=List[User])
def get_all_users():
    user_list = []
    for user_id, user_data in users.items():
        user = User(user_id=user_id, **user_data)
        user_list.append(user)
    return user_list


@app.get("/api/public/campaigns/{campaign_id}", response_model=Campaign)
def get_campaign(campaign_id: str):
    campaign_data = campaigns.get(campaign_id)
    if campaign_data:
        return Campaign(id=campaign_id, **campaign_data)
    else:
        raise create_error_response(404, "Campaign not found")


@app.get("/api/public/campaigns", response_model=List[Campaign])
def get_all_campaigns():
    campaign_list = []
    for campaign_id, campaign_data in campaigns.items():
        campaign = Campaign(id=campaign_id, **campaign_data)
        campaign_list.append(campaign)
    return campaign_list


###########################  POST  ###############################


@app.post("/api/private/campaign")
def create_campaign(campaign: Campaign, token: str = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        return create_error_response(400, "Invalid token")

    if campaign.id in campaigns:
        return create_error_response(400, "Campaign already exists")

    campaigns[campaign.id] = {
        "status": campaign.status,
        "quest": campaign.quest,
        "chat": campaign.chat,
        "users": campaign.users,
    }

    return {"message": "Campaign created successfully"}


@app.post("/api/private/campaigns/{campaign_id}/chat")
def add_to_campaign_chat(
    campaign_id: str, chat: Chat, token: str = Depends(token_auth_scheme)
):
    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        return create_error_response(400, "Invalid token")

    campaign_data = campaigns.get(campaign_id)
    if not campaign_data:
        print("DEBUG", campaigns, campaign_data)
        return create_error_response(404, "Campaign not found")

    user_data = users.get(chat.user_id)
    if not user_data:
        return create_error_response(404, "User not found")

    new_chat_entry = {
        "user_id": chat.user_id,
        "username": user_data.get("username"),
        "text": chat.text,
    }
    campaign_data["chat"].append(new_chat_entry)

    return {"message": "Value added to campaign chat successfully"}


###########################  CHAT  ###############################


@app.get(
    "/api/private/campaigns/{campaign_id_}/chat/{chat_type}", response_model=List[dict]
)
def get_campaign_chat(
    campaign_id_: str,
    chat_type: str,
    token: str = Depends(token_auth_scheme),
):
    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        raise HTTPException(status_code=401, detail="Invalid token")

    campaign_data = campaigns.get(campaign_id_)
    if not campaign_data:
        raise HTTPException(status_code=404, detail="Campaign not found")

    chat = campaign_data["chat"]
    chat_data = ""
    if chat_type == "situation":
        chat_data = model_llm.compute_text(
            "You are a creative Game Master in DND. Give just one very short sentence presenting a situation for the player to solve, no dialogue.\nGM:"
        )
    else:
        input_str = (
            "You are a creative Game Master in DND. you will answer just one very short sentence saying if the player text solves the situation\nSituation: "
            + chat[-2].get("text")
            + "\nPlayer: "
            + chat[-1].get("text")
            + "GM: "
        )
        print("Prompt: " + input_str)
        chat_data = model_llm.compute_text(input_str)

    print(chat_data)

    chat_entry = {
        "campaign_id": campaign_id_,
        "username": "Game_Master",
        "text": chat_data,
    }
    chat.append(chat_entry)

    return chat
